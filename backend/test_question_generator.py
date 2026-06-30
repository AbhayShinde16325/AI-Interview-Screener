from app.parsers.pdf_parser import PDFParser

from app.ai.resume_parser.analyzer import (
    ResumeAnalyzer,
)

from app.ai.retrieval.retriever import (
    Retriever,
)

from app.ai.retrieval.context_builder import (
    ContextBuilder,
)

from app.ai.interview.generator import (
    QuestionGenerator,
)

# Change this to one of your uploaded resumes
pdf_path = "uploads/96d8c9e8-d8ba-47d4-a6ff-3b2ae912b1a3.pdf"

resume_text = PDFParser.extract_text(
    pdf_path
)

resume = ResumeAnalyzer().analyze(
    resume_text
)

retriever = Retriever()

results = retriever.search(
    "Python",
)

context = ContextBuilder().build(
    results
)

generator = QuestionGenerator()

questions = generator.generate(
    resume=resume,
    skill="Python",
    knowledge_context=context,
    question_count=2,
)

print(
    questions.model_dump_json(
        indent=2,
    )
)