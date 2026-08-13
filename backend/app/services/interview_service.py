import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.ai.interview.generator import QuestionGenerator
from app.ai.interview.planner import InterviewPlanner
from app.ai.retrieval.context_builder import ContextBuilder
from app.ai.retrieval.retriever import QueryBuilder, get_retriever
from app.ai.resume_parser.schemas import ParsedResume
from app.constants.interview import InterviewStatus
from app.core.exceptions import (
    InterviewNotFoundError,
    QuestionNotFoundError,
    ResumeNotFoundError,
)
from app.models.interview import Interview
from app.models.interview_question import InterviewQuestion
from app.models.interview_result import InterviewResult
from app.models.user import User
from app.repositories.interview_question_repository import (
    InterviewQuestionRepository,
)
from app.repositories.interview_repository import InterviewRepository
from app.repositories.resume_repository import ResumeRepository
from app.ai.evaluation.evaluator import Evaluator

logger = logging.getLogger(__name__)


class InterviewService:

    def __init__(self, db: Session):
        self.db = db

        # Repositories
        self.resume_repository = ResumeRepository(db)
        self.interview_repository = InterviewRepository(db)
        self.question_repository = InterviewQuestionRepository(db)

        # AI components
        self.planner = InterviewPlanner()
        # Singleton: the FAISS index + embedding service are loaded once per
        # process, not once per request.
        self.retriever = get_retriever()
        self.context_builder = ContextBuilder()
        self.generator = QuestionGenerator()
        self.evaluator = Evaluator()

    # ------------------------------------------------------------------
    # Resume
    # ------------------------------------------------------------------
    def load_candidate_resume(self, current_user: User) -> ParsedResume:
        """Loads the latest parsed resume for the user."""
        resume = self.resume_repository.get_latest_by_user(current_user.id)

        if resume is None:
            raise ResumeNotFoundError(
                "No resume found for this user. Upload a resume first."
            )

        if resume.parsed_resume is None:
            raise ResumeNotFoundError(
                "Resume has not been analyzed yet. Please re-upload it."
            )

        return ParsedResume.model_validate(resume.parsed_resume)

    # ------------------------------------------------------------------
    # Planning + retrieval
    # ------------------------------------------------------------------
    def build_plan(self, resume: ParsedResume) -> dict:
        """Deterministic interview plan derived from the candidate's skills."""
        return self.planner.create_plan(resume)

    def retrieve_knowledge(
        self,
        plan: dict,
        resume: ParsedResume,
    ) -> str:
        """
        Retrieves grounded knowledge for every skill in the plan.

        Queries are built from the skill + resume signals, then converted
        into a single prompt-ready context block with duplicates removed.
        """
        sections = []

        for item in plan["plan"]:
            skill = item["skill"]

            query = QueryBuilder.for_skill(skill, resume)
            results = self.retriever.search(query, k=5)

            if not results:
                logger.warning("No knowledge retrieved for skill: %s", skill)
                continue

            context = self.context_builder.build(results)

            if context:
                sections.append(f"SKILL: {skill}\n\n{context}")

        knowledge_context = "\n\n".join(sections)

        if not knowledge_context:
            logger.warning(
                "Knowledge base returned no chunks — questions may be less "
                "grounded. Run scripts/build_index.py if this is unexpected."
            )

        return knowledge_context

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------
    def generate_questions(
        self,
        current_user: User,
        role: str,
    ):
        parsed_resume = self.load_candidate_resume(current_user)
        plan = self.build_plan(parsed_resume)
        knowledge_context = self.retrieve_knowledge(plan, parsed_resume)

        generated = self.generator.generate(
            resume=parsed_resume,
            role=role,
            interview_plan=plan,
            knowledge_context=knowledge_context,
        )

        return generated.questions

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def save_interview(
        self,
        current_user: User,
        role: str,
        questions,
    ) -> Interview:
        """Saves the interview and all generated questions atomically."""
        interview = Interview(
            user_id=current_user.id,
            role=role,
            status=InterviewStatus.CREATED.value,
        )

        question_models = [
            InterviewQuestion(
                question_order=order,
                skill=question.skill,
                difficulty=question.difficulty,
                question_type=question.type,
                question=question.question,
                expected_topics=question.expected_topics,
                knowledge_source=question.knowledge_source,
                options=question.options,
                correct_answer=question.correct_answer,
            )
            for order, question in enumerate(questions, start=1)
        ]

        return self.interview_repository.create_with_questions(
            interview,
            question_models,
        )

    def create_interview(
        self,
        current_user: User,
        role: str,
    ) -> Interview:
        """
        Creates a complete interview.

        Steps:
        1. Load latest parsed resume
        2. Build the interview plan
        3. Retrieve grounding knowledge (RAG)
        4. Generate all questions in one Gemini call
        5. Persist interview + questions
        """
        questions = self.generate_questions(
            current_user=current_user,
            role=role,
        )

        return self.save_interview(
            current_user=current_user,
            role=role,
            questions=questions,
        )

    # ------------------------------------------------------------------
    # Ownership helpers
    # ------------------------------------------------------------------
    def _get_owned_interview(
        self,
        interview_id,
        user_id,
    ) -> Interview:
        interview = self.interview_repository.get_by_id_and_user(
            interview_id,
            user_id,
        )

        if interview is None:
            raise InterviewNotFoundError(
                "Interview not found or not owned by this user."
            )

        return interview

    # ------------------------------------------------------------------
    # Reading
    # ------------------------------------------------------------------
    def get_questions(
        self,
        interview_id,
        user_id,
    ):
        self._get_owned_interview(interview_id, user_id)

        return self.question_repository.get_by_interview_id(interview_id)

    def get_interview_with_questions(
        self,
        interview_id,
        user_id,
    ) -> tuple[Interview, list]:
        """Returns the owned interview alongside its questions."""
        interview = self._get_owned_interview(interview_id, user_id)
        questions = self.question_repository.get_by_interview_id(interview_id)
        return interview, questions

    def list_interviews(
        self,
        user_id,
    ) -> list[Interview]:
        return self.interview_repository.list_by_user(user_id)

    # ------------------------------------------------------------------
    # Answer submission
    # ------------------------------------------------------------------
    def submit_answer(
        self,
        interview_id,
        question_id,
        answer: str,
        user_id,
    ):
        """
        Save the candidate's answer for a question.

        Ownership is enforced: the interview must belong to the user and
        the question must belong to the interview.
        """
        self._get_owned_interview(interview_id, user_id)

        question = self.question_repository.get_by_id(question_id)

        if question is None:
            raise QuestionNotFoundError("Question not found.")

        if question.interview_id != interview_id:
            raise QuestionNotFoundError(
                "Question does not belong to this interview."
            )

        question.candidate_answer = answer

        return self.question_repository.update(question)

    # ------------------------------------------------------------------
    # Evaluation (Phase 7)
    # ------------------------------------------------------------------
    def complete_interview(
        self,
        interview_id,
        user_id,
    ) -> tuple[InterviewResult, Interview]:
        """
        Evaluates the candidate's answers and stores an InterviewResult.

        - Questions without an answer are scored 0 with a note.
        - The interview is marked COMPLETED with its overall score.
        """
        interview = self._get_owned_interview(interview_id, user_id)

        # Idempotent: re-completing an already-evaluated interview returns the
        # stored result instead of duplicating it.
        if interview.result is not None:
            return interview.result, interview

        questions = self.question_repository.get_by_interview_id(interview_id)

        evaluation = self.evaluator.evaluate(
            role=interview.role,
            questions=questions,
        )

        # Persist per-question scores + feedback
        by_order = {q.question_order: q for q in questions}

        for question_eval in evaluation.question_evaluations:
            question = by_order.get(question_eval.question_order)
            if question is None:
                logger.warning(
                    "Evaluation referenced unknown order %s",
                    question_eval.question_order,
                )
                continue
            question.score = question_eval.score
            question.feedback = question_eval.feedback

        self.question_repository.commit_all()

        result = InterviewResult(
            interview_id=interview.id,
            overall_score=evaluation.overall_score,
            recommendation=evaluation.recommendation,
            strengths=evaluation.strengths,
            improvements=evaluation.improvements,
            summary=evaluation.summary,
        )

        interview.result = result
        interview.status = InterviewStatus.COMPLETED.value
        interview.score = evaluation.overall_score
        interview.completed_at = datetime.now(timezone.utc)

        self.db.add(result)
        self.interview_repository.update(interview)

        return result, interview

    def get_interview_result(
        self,
        interview_id,
        user_id,
    ) -> InterviewResult:
        interview = self._get_owned_interview(interview_id, user_id)

        if interview.result is None:
            raise InterviewNotFoundError(
                "This interview has not been evaluated yet. "
                "Complete the interview first."
            )

        return interview.result
