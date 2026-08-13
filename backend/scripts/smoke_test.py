"""
End-to-end smoke test for the AI Interview Screener API.

Runs the full user journey against the real backend stack:
local PostgreSQL DB + real Gemini API (RAG retrieval, question
generation, resume parsing, answer evaluation).

Usage:
    cd backend
    python scripts/smoke_test.py

Exit code 0 = everything passed. Any failure prints the failing step.
"""
import sys
import uuid
from pathlib import Path

# Make the backend root importable when run as `python scripts/smoke_test.py`
BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv()

from fastapi.testclient import TestClient  # noqa: E402

from app.core.database import SessionLocal  # noqa: E402
from app.main import app  # noqa: E402
from app.models.user import User  # noqa: E402

SUPPORTED_ROLE = "AI/ML Engineer"


def find_sample_pdf() -> Path:
    """Pick a previously uploaded PDF that is known to parse into skills."""
    from app.core.database import SessionLocal
    from app.models.resume import Resume

    db = SessionLocal()
    try:
        rows = (
            db.query(Resume)
            .filter(Resume.parsed_resume.isnot(None))
            .all()
        )
    finally:
        db.close()

    for row in rows:
        skills = (row.parsed_resume or {}).get("skills") or []
        path = Path(row.file_path)
        if skills and path.exists():
            return path

    raise SystemExit(
        "No sample PDF that parses into skills found in backend/uploads/. "
        "Upload one via the app first, then re-run this smoke test."
    )


def cleanup_user(email: str) -> None:
    """Remove the test user so the dev DB stays tidy."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user is not None:
            db.delete(user)
            db.commit()
            print(f"  cleaned up test user {email}")
    finally:
        db.close()


def main() -> int:
    suffix = uuid.uuid4().hex[:8]
    email = f"smoke+{suffix}@example.com"
    password = "SmokeTestPass123!"
    full_name = "Smoke Test Candidate"

    client = TestClient(app)

    steps = []

    def run(label: str, fn):
        steps.append(label)
        fn()
        print(f"  PASS  {label}")

    # --- 1. Health check -------------------------------------------------
    def step_health():
        r = client.get("/health")
        assert r.status_code == 200, r.text
        assert r.json()["status"] == "ok"

    # --- 2. Register ------------------------------------------------------
    def step_register():
        r = client.post(
            "/api/v1/auth/register",
            json={
                "full_name": full_name,
                "email": email,
                "password": password,
            },
        )
        assert r.status_code == 201, r.text
        assert r.json()["email"] == email

    # --- 3. Login ---------------------------------------------------------
    def step_login():
        r = client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": password},
        )
        assert r.status_code == 200, r.text
        token = r.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})

    # --- 4. Resume upload -------------------------------------------------
    def step_upload_resume():
        pdf = find_sample_pdf()
        with open(pdf, "rb") as f:
            r = client.post(
                "/api/v1/resumes/upload",
                files={"file": (pdf.name, f, "application/pdf")},
            )
        assert r.status_code == 201, r.text

    # --- 5. Latest resume -------------------------------------------------
    def step_latest_resume():
        r = client.get("/api/v1/resumes/latest")
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["skills"], "no skills extracted from resume"

    # --- 6. Start interview (real RAG + Gemini generation, ~30s) ----------
    def step_start_interview():
        r = client.post(
            "/api/v1/interviews/start",
            json={"role": SUPPORTED_ROLE},
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["questions"], "no questions generated"
        assert len(body["questions"]) >= 1
        globals()["interview_id"] = body["interview_id"]

    # --- 7. Fetch questions ------------------------------------------------
    def step_get_questions():
        r = client.get(f"/api/v1/interviews/{globals()['interview_id']}/questions")
        assert r.status_code == 200, r.text
        questions = r.json()["questions"]
        assert questions
        globals()["question_id"] = questions[0]["id"]

    # --- 8. Submit an answer ------------------------------------------------
    def step_submit_answer():
        r = client.post(
            f"/api/v1/interviews/{globals()['interview_id']}/answer",
            json={"question_id": globals()["question_id"], "answer": "Sample answer."},
        )
        assert r.status_code == 200, r.text

    # --- 9. Complete interview (real Gemini evaluation, ~30s) -------------
    def step_complete():
        r = client.post(f"/api/v1/interviews/{globals()['interview_id']}/complete")
        assert r.status_code == 200, r.text
        body = r.json()
        assert "overall_score" in body
        assert "recommendation" in body

    # --- 10. Fetch result ---------------------------------------------------
    def step_result():
        r = client.get(f"/api/v1/interviews/{globals()['interview_id']}/result")
        assert r.status_code == 200, r.text
        assert r.json()["overall_score"] is not None

    # --- 11. List interviews -------------------------------------------------
    def step_list():
        r = client.get("/api/v1/interviews")
        assert r.status_code == 200, r.text
        ids = [i["id"] for i in r.json()["interviews"]]
        assert globals()["interview_id"] in ids

    # --- 12. Unauthorized access is rejected ----------------------------------
    def step_unauthorized():
        r = client.get("/api/v1/interviews")
        assert r.status_code == 401, f"expected 401, got {r.status_code}"

    checks = [
        ("health check", step_health),
        ("register", step_register),
        ("login", step_login),
        ("resume upload + parse", step_upload_resume),
        ("latest resume", step_latest_resume),
        ("start interview (RAG + generation)", step_start_interview),
        ("fetch questions", step_get_questions),
        ("submit answer", step_submit_answer),
        ("complete interview (evaluation)", step_complete),
        ("fetch result", step_result),
        ("list interviews", step_list),
        ("reject unauthenticated request", step_unauthorized),
    ]

    try:
        for label, fn in checks:
            run(label, fn)
        print(f"\nALL {len(checks)} SMOKE CHECKS PASSED ✅")
        return 0
    except AssertionError as exc:
        failed = steps[-1] if steps else "?"
        print(f"\nFAILED at step '{failed}': {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        failed = steps[-1] if steps else "?"
        print(f"\nERROR at step '{failed}': {exc!r}", file=sys.stderr)
        return 1
    finally:
        client.headers.pop("Authorization", None)
        cleanup_user(email)


if __name__ == "__main__":
    sys.exit(main())
