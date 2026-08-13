# Project Report — AI-Powered Role-Based Candidate Screening System

Status as of this report, then the plan derived from it. Each module is reviewed against
the assignment requirements (RAG, clean architecture, deployability, documentation).

Legend: ✅ working · 🟡 partial / fragile · ❌ missing / broken

---

## 1. Backend Foundation (FastAPI / config / auth)

| Module | Current | Expected |
|---|---|---|
| `app/core/config.py` | 🟡 `gemini_api_key` declared twice; all DB fields required even though `database_url` is what's used; no CORS settings | Single source of truth: `database_url` (or build from parts), `gemini_api_key`, JWT settings, `cors_origins` |
| `app/core/database.py` | ✅ engine + session + `get_db` | ✅ |
| `app/core/security.py` | ✅ JWT (python-jose) + password hashing via `pwdlib` (argon2) | ✅ (argon2 is a defensible upgrade over bcrypt) |
| `app/core/dependencies.py` | 🟡 creates a new `InterviewService` per request; the retriever (embedding model + FAISS index) is loaded per request | Heavy components become process-wide singletons |
| `app/core/exceptions.py` | 🟡 only 3 bare exceptions; **no handlers registered in `main.py`** | Full hierarchy + FastAPI exception handlers (404/409/400) |
| `app/core/logging.py` | ❌ empty file | Structured logging config |
| `app/main.py` | 🟡 no CORS middleware, no exception handlers, no lifespan | CORS, handlers, router registration for evaluation, health route |
| `requirements.txt` | ❌ **missing `google-genai`, `faiss-cpu`, `numpy`, `PyMuPDF`, `python-multipart`** — a fresh `pip install -r` cannot run the app | Regenerated to match the working venv |

## 2. Authentication (Phase 2)

| Module | Current | Expected |
|---|---|---|
| `app/api/v1/auth.py` | 🟡 register: duplicate-email raises `ValueError` → **HTTP 500** (only login catches it) | register returns 409 on duplicate; login returns token + user |
| `app/services/auth_service.py` | ✅ register/login/me logic | ✅ |
| `app/schemas/auth.py`, `users.py` | ✅ pydantic validation | ✅ |

## 3. Resume Processing (Phase 3)

| Module | Current | Expected |
|---|---|---|
| `app/api/v1/resumes.py` | ✅ upload endpoint | ✅ |
| `app/services/resume_service.py` | 🟡 no file-size limit, empty-PDF guard, CWD-relative `uploads/` path; **parses the resume synchronously inside the request** (acceptable for MVP) | Add size/empty validation; make upload dir configurable |
| `app/parsers/pdf_parser.py` | ✅ PyMuPDF text extraction | ✅ |
| `app/ai/resume_parser/analyzer.py` + `schemas.py` | ✅ Gemini → validated `ParsedResume` | ✅ |
| `app/ai/prompts/resume_prompt.py` | ✅ strict JSON schema prompt | ✅ |

## 4. Knowledge Base & Embeddings (Phase 4)

| Module | Current | Expected |
|---|---|---|
| `app/ai/retrieval/loader.py` | ✅ loads `*.md` from `knowledge_base/` | ✅ |
| `app/ai/retrieval/chunker.py` | ✅ markdown-aware chunker (headings → paragraphs → sentences) | ✅ |
| `app/ai/embeddings/embedding_service.py` | ✅ Gemini `gemini-embedding-001` (3072 dims) | ✅ (deliberate deviation from `bge-small-en-v1.5`: one API key, no local model download — see README design decisions) |
| `app/ai/embeddings/faiss_store.py` | ✅ FlatL2 index + metadata JSON | ✅ |
| `app/ai/embeddings/index_builder.py` | ✅ builds + saves index | ✅ but no CLI entry point |
| `scripts/` | ❌ **no build script exists** | `scripts/build_index.py` |
| `knowledge_base/` content | ❌ **only `backend/python.md`; `ai_ml/` and `data_engineering/` are empty**; committed index has 1 chunk | Sample AI/ML docs committed + rebuild instructions |
| `knowledge_base/index/` | ✅ committed to git (faiss.index + metadata.json) | ✅ (no rebuild needed on deploy) |

## 5. RAG Pipeline (Phase 5)

| Module | Current | Expected |
|---|---|---|
| `app/ai/retrieval/retriever.py` | 🟡 loads index in `__init__` (per-request cost); crashes if index missing; **query is the bare skill name** | Singleton; tolerant load; richer query (skill + resume keywords) |
| `app/ai/retrieval/context_builder.py` | 🟡 dedupe is done by the service on **exact string**, not by chunk id | Dedupe by `filename + chunk_number` from metadata |
| `InterviewService` context assembly | 🟡 empty retrieval result silently produces empty context | Guard + log; never call Gemini with zero grounding |

## 6. Interview Engine (Phase 6) — the in-progress refactor

| Module | Current | Expected |
|---|---|---|
| `app/services/interview_service.py` | 🟡 **`submit_answer` defined 3×** (only last is live — dead-code landmine); no ownership checks (**IDOR**: any user can read/answer another user's interview); bare `ValueError` → 500; resume loaded twice; `status="created"` hardcoded; hand-rolled commit instead of repository | Single method, ownership checks, domain exceptions, one resume load, status constant, atomic repository save |
| `app/ai/interview/planner.py` | ✅ deterministic plan (4 skills × 2 + 2 project questions = 10) | ✅ |
| `app/ai/interview/generator.py` | 🟡 **debug `print`s of raw Gemini response left in**; no JSON retry; no fence stripping | Remove prints; strip ```json fences; retry once; validate question count |
| `app/ai/interview/normalizer.py` | ✅ defaults + type/difficulty mapping | ✅ |
| `app/ai/interview/prompt_builder.py` | ✅ single-request prompt with role/resume/plan/context | ✅ |
| `app/ai/prompts/interview_questions.py` | ✅ full-interview prompt | ✅ |
| `app/api/v1/interviews.py` | 🟡 routes don't enforce ownership; inline response construction | Use mapper; ownership enforced in service |
| `app/mappers/interview_mapper.py` | ✅ | ✅ |

## 7. Evaluation (Phase 7)

| Module | Current | Expected |
|---|---|---|
| `app/ai/evaluation/` | ❌ **directory empty** | Evaluator + prompt |
| `app/models/interview_result.py` | ✅ model exists | ✅ |
| Alembic migration for `interview_results` | ❌ **not created** (head migration creates `interviews`/`interview_questions` only) | New migration |
| `app/api/v1/evaluation.py` | ❌ empty file | Complete + result endpoints |
| Service methods | ❌ none | `complete_interview`, `get_interview_result` |

## 8. Frontend (Phase 8)

| Module | Current | Expected |
|---|---|---|
| `frontend/` | ❌ **empty** (no package.json, no src) | Full React app (login, register, dashboard, upload, interview, result) |
| Deployment config | ❌ none | `vercel.json` |

## 9. Data Layer / Schema

| Module | Current | Expected |
|---|---|---|
| `app/models/interview.py`, `interview_question.py` | ✅ | ✅ |
| `app/models/answer.py` | ❌ orphaned (references deleted `questions` table) | Delete |
| `app/models/__init__.py` | ✅ imports current models | ✅ |
| Migration chain | 🟡 works on fresh DB; head doesn't create `interview_results`; new table FKs lack `ondelete=CASCADE` | Add `interview_results` migration |

## 10. Dead / empty files to remove or fill

- `app/api/v1/questions.py` (empty) → remove
- `app/api/users.py` (empty) → remove
- `app/schemas/interview_session.py` (old, unused) → remove
- `app/models/answer.py` (orphan) → remove
- `test_faiss.PY` (broken filename) → remove
- `app/api/v1/evaluation.py` (empty) → implement
- `core/logging.py` (empty) → implement

## 11. Documentation & Deployment

| Item | Current | Expected |
|---|---|---|
| `README.md` (root) | ❌ empty | Full README (scope, run, file-by-file, deploy) |
| `docs/` | ❌ empty dirs | This report + architecture notes |
| `render.yaml` / `vercel.json` | ❌ | Deployment blueprints |
| `.env.example` | ❌ | Committed template |
| `.gitignore` | 🟡 no `node_modules/`, `frontend/dist`, `.env` variants | Update |

---

## Critical gaps (must fix for a working, deployable submission)

1. **`requirements.txt` is missing 5 packages** — app cannot be installed on Render.
2. **No CORS** — the Vercel frontend cannot call the API.
3. **No `interview_results` migration** — evaluation will crash on a fresh DB.
4. **Ownership (IDOR) + triple `submit_answer`** — security/correctness.
5. **Bare `ValueError` → HTTP 500** — no error handling layer wired up.
6. **Frontend doesn't exist** — no way to demo the system.
7. **Knowledge base has 1 chunk** — RAG is technically "working" but retrieves almost nothing; needs sample docs + rebuild script.
8. **No README / deployment config** — required deliverables.

## Resolution (applied in this pass)

Every item below has been implemented, verified, and documented:

- ✅ `requirements.txt` regenerated (was missing 5 packages); `.env.example` added
- ✅ CORS middleware + global exception handlers + logging in `main.py`; config cleaned
- ✅ `InterviewService` rewritten: single `submit_answer`, ownership checks
  (IDOR fixed), domain exceptions, singleton retriever, atomic save, status constant
- ✅ Question generator: debug prints removed, JSON fence stripping, retry,
  count validation
- ✅ Retrieval: richer queries (skill + resume keywords), tolerant index load,
  chunk-id dedupe
- ✅ Phase 7 evaluation: `Evaluator` + prompt + `complete`/`result` endpoints
- ✅ `interview_results` migration added (and the `9c0a9747acca` migration fixed —
  its DROP statements ran at import time, which would break a fresh deploy)
- ✅ `GET /resumes/latest`, `GET /interviews` endpoints; resume upload validation
- ✅ Frontend built: Vite + React + Tailwind + Zustand + Router + Axios
  (login, register, dashboard, upload, interview, result)
- ✅ Deployment: `render.yaml`, `vercel.json`, `.gitignore`, README with full
  run + deploy guide
- ✅ 20 unit tests pass (`python -m unittest discover -s tests`); backend
  boots and serves `/health` + full OpenAPI surface

## Implementation plan (original, for reference)

1. Config/exceptions/CORS/logging/main.py
2. InterviewService + repositories + generator hardening
3. Retrieval: singleton, tolerant load, query builder, chunk-id dedupe
4. Evaluation module + migration + routes
5. Resume/auth fixes, dead-file cleanup, `scripts/build_index.py`, sample KB, `requirements.txt`, `.env.example`
6. Frontend (full app)
7. Deployment configs + `.gitignore`
8. Verification (compile + import checks + tests)
9. README
