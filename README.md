# AI Interview Screener

**AI-Powered Role-Based Candidate Screening System using Retrieval-Augmented Generation (RAG).**

Upload a resume (PDF), and the system dynamically generates a structured technical
interview grounded in a role-specific knowledge base — then evaluates the
candidate's answers and produces a hiring recommendation.

Built as an AI/ML & Backend Engineering internship assignment. It is designed,
structured, and deployable like a real startup MVP, not a tutorial project.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Current Scope](#current-scope)
- [Future Scope](#future-scope)
- [System Architecture](#system-architecture)
- [How the RAG Pipeline Works](#how-the-rag-pipeline-works)
- [Tech Stack](#tech-stack)
- [Folder Structure — What Each File Does](#folder-structure--what-each-file-does)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Running Locally](#running-locally)
- [Environment Variables](#environment-variables)
- [Tests](#tests)
- [Deployment](#deployment)
- [Demo Video Plan](#demo-video-plan)
- [Key Design Decisions & Lessons Learned](#key-design-decisions--lessons-learned)

---

## Project Overview

The system simulates a structured technical interview where questions are **not
predefined**. Instead, every interview is generated at runtime from three inputs:

1. **The candidate's resume** — parsed and normalized into skills, projects,
   education, and experience.
2. **The selected job role** — one of five supported roles: `AI/ML Engineer`,
   `Backend Engineer`, `Data Engineer`, `Python Developer`, or
   `Full Stack Developer`.
3. **A role-specific knowledge base** — a set of markdown documents that are
   chunked, embedded, and indexed in FAISS (a vector store).

The interview lifecycle:

```
Register / Login
      │
      ▼
Upload resume (PDF) ──► PyMuPDF text extraction ──► Gemini parses into structured JSON
      │
      ▼
Start interview (role selected) ──► Interview plan built from resume skills
      │
      ▼
RAG retrieval ──► knowledge chunks retrieved per skill
      │
      ▼
Gemini generates the COMPLETE interview in one call (grounded in retrieved context)
      │
      ▼
Candidate answers question by question (persisted after each answer)
      │
      ▼
Evaluation ──► per-question scores, strengths, improvements, recommendation
      │
      ▼
Summary page shown to the candidate
```

Every generated question is **traceable** to the knowledge base: each question
stores its `knowledge_source` (the file/chunk it was grounded on) and the
`expected_topics` the answer should cover.

---

## Current Scope

| Feature | Status |
|---|---|
| JWT authentication (register / login / me) | ✅ |
| Resume upload (PDF) + Gemini-based parsing | ✅ |
| Skill / project / education extraction | ✅ |
| Knowledge base ingestion (chunk → embed → FAISS) | ✅ (script + sample docs) |
| RAG retrieval with resume-aware queries | ✅ |
| Complete interview generation in one Gemini call | ✅ |
| Mixed multiple-choice + written questions | ✅ |
| Multi-role support (5 roles selectable) | ✅ |
| Interview persistence (sessions + questions + answers) | ✅ |
| Answer submission with ownership checks | ✅ |
| Evaluation + hiring recommendation | ✅ |
| React frontend (landing, auth, dashboard, resume, interview, results) | ✅ |
| Deployment configs (Render + Vercel + Neon) | ✅ |
| README + project report + tests | ✅ |

**Knowledge base caveat:** the committed FAISS index is a small sample.
To make the system shine, add the assigned textbook content
(e.g. *Machine Learning — Tom Mitchell*, *The Hundred-Page Machine Learning Book*)
as markdown in `backend/knowledge_base/` and rebuild the index (see
[Deployment → Rebuilding the index](#rebuilding-the-knowledge-base-index)).

---

## Future Scope

Ideas that are intentionally **not** implemented (good candidates for the
"Creativity & Extensions" section of the assignment, or a v2):

- **Deeper role knowledge** — the knowledge base is structured per role
  category (`knowledge_base/ai_ml`, `knowledge_base/backend`, …); add more
  markdown content under `knowledge_base/backend/` and
  `knowledge_base/data_engineering/` to make those roles even stronger.
- **Adaptive follow-up questions** — a second Gemini pass that asks a deeper
  question based on the previous answer.
- **Answer evaluation streaming** — show partial results instead of waiting for
  the whole evaluation.
- **Alternative embedding models** — swap `gemini-embedding-001` for a local
  model (e.g. `BAAI/bge-small-en-v1.5` + `sentence-transformers`).
- **More question formats** — fill-in-the-blank, code execution sandbox, and
  other non-MCQ interactive formats.
- **Rate limiting + async background jobs** for long-running generations.
- **Admin analytics dashboard** — aggregate scores across candidates.
- **Audio/video interview capture** (out of scope for a 48h assignment).

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                            FRONTEND (Vercel)                         │
│   React + Vite + Tailwind + Zustand + Axios + React Router           │
│   Login · Register · Dashboard · Upload · Interview · Result         │
└───────────────────────────────┬──────────────────────────────────────┘
                                │  HTTPS + JWT (Bearer token)
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         BACKEND (Render / FastAPI)                   │
│                                                                      │
│  api/v1 (routes)                                                     │
│    auth ──► AuthService ──► UserRepository ──► users table            │
│    resumes ─► ResumeService ─► PDFParser + ResumeAnalyzer ─► resumes │
│    interviews ─► InterviewService ──► (orchestrator)                  │
│    evaluation ─► Evaluator (Gemini) ─► interview_results             │
│                                                                      │
│  InterviewService pipeline:                                          │
│    ParsedResume ──► InterviewPlanner ──► skill plan                   │
│                        │                                             │
│                        ▼                                             │
│    QueryBuilder ──► Retriever (FAISS) ──► ContextBuilder             │
│                        │                                             │
│                        ▼                                             │
│    PromptBuilder ──► Gemini (one call) ──► QuestionNormalizer        │
│                        │                                             │
│                        ▼                                             │
│    InterviewRepository ──► interviews + interview_questions          │
└───────┬──────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐        ┌──────────────────────────────┐
│   PostgreSQL (Neon)         │        │  Knowledge base (FAISS)      │
│   users · resumes ·         │        │  knowledge_base/*.md ──►      │
│   interviews ·              │        │  index/faiss.index +          │
│   interview_questions ·     │        │  metadata.json (committed)    │
│   interview_results         │        └──────────────────────────────┘
└─────────────────────────────┘
```

### Separation of concerns

- **API routes** (`app/api/v1/`) — HTTP layer only: parse requests, call a
  service, return a schema. No business logic.
- **Services** (`app/services/`) — orchestration / use cases.
- **Repositories** (`app/repositories/`) — all database access.
- **AI components** (`app/ai/`) — parsers, retrieval, generation, evaluation.
- **Schemas** (`app/schemas/`) — request/response contracts (Pydantic).
- **Models** (`app/models/`) — SQLAlchemy ORM models.
- **Mappers** (`app/mappers/`) — ORM → response schema conversion.
- **Core** (`app/core/`) — config, database, security, exceptions, logging.

---

## How the RAG Pipeline Works

The RAG pipeline is the heart of this project. Every step has a reason.

### 1. Ingestion (offline, via `scripts/build_index.py`)

```
knowledge_base/*.md
   │  KnowledgeBaseLoader (reads all markdown)
   ▼
DocumentChunker (heading-aware, ~1000 chars, 150 overlap)
   │
   ▼
EmbeddingService (Gemini embeddings, 3072-dim)
   │
   ▼
FAISSStore (IndexFlatL2) ──► index/faiss.index + index/metadata.json
```

**Why markdown-aware chunking?** Splitting naively by character count breaks
concepts in half. The chunker first splits on `#` headings, then paragraphs,
then sentences — preserving semantic boundaries. The small overlap stops an
idea from being cut between two chunks.

**Why this embedding model?** The assignment suggests `bge-small-en-v1.5`, but
using **Gemini's embedding API** (`gemini-embedding-001`) keeps everything
under one API key and avoids downloading a local model on Render — a deliberate,
documented tradeoff. Swapping back to a local model is a one-file change
(see Future Scope).

**Why commit the index?** The built index is committed to the repo, so the
deployed backend has retrieval **without** re-embedding the whole book at
startup (saves time and API cost on every deploy).

### 2. Retrieval (online, per interview)

```
InterviewPlanner: up to 4 skills × 2 questions + 2 project questions = ~10
   │
   ▼
QueryBuilder: skill + candidate's related keywords
   e.g. "Python Django FastAPI"  (not just "Python")
   │
   ▼
Retriever: embed query ──► FAISS top-k (k=5) ──► chunks with metadata
   │
   ▼
ContextBuilder: dedupe by (filename, chunk_number) ──► prompt-ready context
```

**Why not just the skill name as the query?** A bare skill name ("Python")
retrieves generic chunks. Combining it with keywords from the candidate's own
resume makes retrieval candidate-specific — a core assignment requirement.

**Why dedupe by chunk id?** Two skills often retrieve the same source chunk.
Deduplicating by `(filename, chunk_number)` — not by exact text — stops the
same chunk from inflating the prompt and costing tokens.

### 3. Generation (one Gemini call per interview)

```
PromptBuilder ──► role + resume (JSON) + plan + retrieved context
   │
   ▼
Gemini (gemini-2.5-flash) ──► JSON: the complete question list
   │
   ▼
QuestionNormalizer ──► fixes types/difficulty, fills defaults
   │
   ▼
InterviewQuestionList validated + count checked (retry once on bad JSON)
```

**Why one call instead of per-question calls?** Generating the whole interview
in one request keeps the interview coherent (no repeated questions, natural
difficulty progression) and keeps latency/cost predictable.

### 4. Evaluation (one Gemini call)

```
All questions + candidate answers (JSON)
   │
   ▼
Gemini ──► per-question score (0–10) + feedback,
            overall score (0–100), strengths, improvements,
            summary, recommendation (Strong Hire / Hire / Borderline / No Hire)
   │
   ▼
Persisted: interview_results + per-question score/feedback
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite 5, Tailwind CSS 3, React Router 6, Zustand, Axios |
| Backend | Python 3.11, FastAPI, Uvicorn, SQLAlchemy 2, Alembic |
| Database | PostgreSQL (Neon), psycopg2 |
| Auth | JWT (python-jose), argon2 password hashing (pwdlib) |
| AI | Google Gemini (`gemini-2.5-flash` + `gemini-embedding-001`) |
| Vector store | FAISS (IndexFlatL2) |
| Resume parsing | PyMuPDF |
| Deployment | Render (backend) · Vercel (frontend) · Neon (DB) |

---

## Folder Structure — What Each File Does

```
.
├── README.md                  ← this file
├── render.yaml                ← Render blueprint for the backend
├── docs/
│   └── PROJECT_REPORT.md      ← module-by-module audit + build plan
├── backend/
│   ├── .env.example           ← template for backend env vars
│   ├── requirements.txt       ← pinned Python dependencies
│   ├── alembic.ini / alembic/ ← migration config + version scripts
│   ├── app/
│   │   ├── main.py            ← FastAPI app: CORS, exception handlers, routers
│   │   ├── core/
│   │   │   ├── config.py      ← Settings (env vars, DB URL builder, CORS)
│   │   │   ├── database.py    ← engine + SessionLocal + get_db dependency
│   │   │   ├── security.py    ← JWT create/decode, argon2 hash/verify
│   │   │   ├── dependencies.py← auth + service DI helpers
│   │   │   ├── exceptions.py  ← domain exceptions (→ proper HTTP status codes)
│   │   │   └── logging.py     ← shared logging setup
│   │   ├── api/v1/
│   │   │   ├── auth.py        ← POST /auth/register, /login, GET /auth/me
│   │   │   ├── resumes.py     ← POST /resumes/upload, GET /resumes/latest
│   │   │   ├── interviews.py  ← start, list, questions, answer
│   │   │   └── evaluation.py  ← POST …/complete, GET …/result
│   │   ├── services/
│   │   │   ├── auth_service.py       ← register/login use cases
│   │   │   ├── resume_service.py     ← PDF validation, storage, parsing
│   │   │   └── interview_service.py  ← orchestrator: plan → retrieve → generate → save → evaluate
│   │   ├── repositories/
│   │   │   ├── user_repository.py
│   │   │   ├── resume_repository.py  (incl. get_latest_by_user)
│   │   │   ├── interview_repository.py (incl. ownership + atomic save)
│   │   │   └── interview_question_repository.py
│   │   ├── models/            ← SQLAlchemy models: user, resume, interview,
│   │   │                        interview_question, interview_result
│   │   ├── schemas/           ← Pydantic request/response models
│   │   ├── mappers/           ← interview_mapper (ORM → response)
│   │   ├── parsers/           ← pdf_parser (PyMuPDF)
│   │   ├── constants/         ← role / status / difficulty enums
│   │   └── ai/
│   │       ├── gemini/client.py        ← thin Gemini wrapper
│   │       ├── resume_parser/          ← analyzer + ParsedResume schema
│   │       ├── retrieval/              ← loader, chunker, retriever (FAISS),
│   │       │                              context_builder, query builder
│   │       ├── embeddings/             ← embedding_service, faiss_store, index_builder
│   │       ├── interview/              ← planner, prompt_builder, generator, normalizer
│   │       ├── evaluation/             ← evaluator + result schemas
│   │       └── prompts/                ← interview + resume + evaluation prompts
│   ├── scripts/
│   │   └── build_index.py     ← rebuild the FAISS index from the knowledge base
│   ├── knowledge_base/        ← markdown docs (ai_ml/, backend/, data_engineering/)
│   │   └── index/             ← committed faiss.index + metadata.json
│   ├── tests/                 ← unit tests (unittest, no DB/API needed)
│   └── uploads/               ← uploaded PDFs (gitignored)
└── frontend/
    ├── package.json           ← React app manifest
    ├── vite.config.js         ← dev server + /api proxy to localhost:8000
    ├── tailwind.config.js     ← design system (brand palette, Inter, radius)
    ├── index.html             ← fonts, meta, favicon
    ├── vercel.json            ← SPA rewrites for Vercel
    ├── .env.example           ← VITE_API_URL template
    └── src/
        ├── main.jsx / app.jsx ← entry + router (public + /app protected routes)
        ├── index.css          ← Tailwind base styles + focus rings
        ├── api/client.js      ← Axios instance (auth header, 401 → session-expired)
        ├── store/authStore.js ← Zustand auth state (persisted to localStorage)
        ├── services/          ← auth.js, resumes.js, interviews.js (API calls)
        ├── utils/             ← errors.js (friendly messages), validation.js
        ├── components/
        │   ├── ui/            ← Button, Input, Select, Badge, Modal, Skeleton,
        │   │                    EmptyState, Spinner, Alert, Logo
        │   ├── layout/        ← AppShell (sidebar + top bar + mobile bottom nav)
        │   ├── auth/          ← AuthLayout (split-screen), PasswordInput
        │   ├── dashboard/     ← InterviewTable (shared list/table)
        │   └── interview/     ← InterviewProgress, InterviewExitModal
        └── pages/
            ├── Landing.jsx    ← marketing page (hero + product preview + how it works)
            ├── Login.jsx / Register.jsx
            └── app/           ← Dashboard, Resume, InterviewSetup, Interview,
                                 InterviewHistory, Results, Settings
```

---

## Database Schema

```
users
├── id (uuid, PK)
├── full_name (varchar)
├── email (varchar, unique)
├── password_hash (varchar)
└── created_at / updated_at

resumes
├── id (uuid, PK)
├── user_id (FK → users, cascade)
├── filename / file_path
├── extracted_text (text)
├── parsed_resume (jsonb — the Gemini-extracted structure)
└── created_at / updated_at

interviews
├── id (uuid, PK)
├── user_id (FK → users)
├── role (varchar)
├── status (varchar: CREATED / COMPLETED)
├── score (int, nullable — set after evaluation)
├── started_at / completed_at

interview_questions
├── id (uuid, PK)
├── interview_id (FK → interviews, cascade)
├── question_order (int)
├── skill / difficulty / question_type / question (text)
├── expected_topics (jsonb)
├── knowledge_source (varchar — traceability back to the KB)
├── options (jsonb, nullable — MCQ choices; the correct answer is stored
│   in correct_answer and never exposed to the candidate)
├── correct_answer (text, nullable — used only for evaluation)
├── candidate_answer (text, nullable — written answer or chosen option)
├── score (int, nullable — per-question after evaluation)
└── feedback (text, nullable)

interview_results
├── id (uuid, PK)
├── interview_id (FK → interviews, unique, cascade)
├── overall_score (int)
├── recommendation (text)
├── strengths / improvements (jsonb)
├── summary (text)
└── created_at
```

Migrations live in `backend/alembic/versions/` and are applied with
`alembic upgrade head`. On a fresh database the full chain runs in order and
ends at `interview_results`.

---

## API Endpoints

Base URL: `/api/v1` — all endpoints except `register`/`login` require
`Authorization: Bearer <token>`.

| Method | Path | Description |
|---|---|---|
| `POST` | `/auth/register` | Create an account (`full_name`, `email`, `password`) |
| `POST` | `/auth/login` | Returns `{ access_token, token_type }` |
| `GET` | `/auth/me` | Current user profile |
| `POST` | `/resumes/upload` | Upload a PDF resume (multipart `file`) → parses it |
| `GET` | `/resumes/latest` | Latest resume with parsed summary + skills |
| `POST` | `/interviews/start` | Body `{ role }` → creates interview + returns questions |
| `GET` | `/interviews` | List current user's interviews |
| `GET` | `/interviews/{id}/questions` | All questions for an interview |
| `POST` | `/interviews/{id}/answer` | Body `{ question_id, answer }` → saves an answer |
| `POST` | `/interviews/{id}/complete` | Runs evaluation → returns the result |
| `GET` | `/interviews/{id}/result` | Stored evaluation for a completed interview |
| `GET` | `/health` | Liveness check |

Interactive docs: `http://localhost:8000/docs` (Swagger UI).

---

## Running Locally

### Prerequisites

- Python 3.11+
- Node.js 18+
- A PostgreSQL database (local, or a free Neon database)
- A Google Gemini API key — https://aistudio.google.com/apikey

### 1. Backend

```bash
cd backend

# Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env            # then fill in DATABASE_URL, GEMINI_API_KEY, SECRET_KEY

# Apply database migrations
alembic upgrade head

# Run the server
uvicorn app.main:app --reload
```

The API is now at `http://localhost:8000` (docs at `/docs`).

### 2. (Optional) Rebuild the knowledge base index

If you add or change files under `backend/knowledge_base/`:

```bash
cd backend
python scripts/build_index.py
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

The app is now at `http://localhost:5173`. Vite proxies `/api` to
`http://localhost:8000`, so no env vars are needed locally.

### Smoke test the whole flow

1. Open `http://localhost:5173` — the landing page explains the product.
2. Click **Get started** → create an account (or sign in).
3. From the dashboard, open **Resume** and upload a PDF — it is parsed in a few seconds.
4. Click **Start interview** → confirm the role (AI/ML Engineer) → **Start interview** — wait ~10–20s while questions are generated.
5. Answer each question and finish — the evaluation page appears.

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | ✅ | Full PostgreSQL URL, e.g. `postgresql+psycopg2://user:pass@host:5432/db` |
| `GEMINI_API_KEY` | ✅ | Google Gemini API key |
| `SECRET_KEY` | ✅ | Random string for JWT signing (`secrets.token_hex(32)`) |
| `ALGORITHM` | – | JWT algorithm (default `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | – | Token lifetime (default `1440`) |
| `CORS_ORIGINS` | – | Comma-separated frontend origins (default localhost:5173/3000) |
| `UPLOAD_DIR` | – | Upload directory (default `uploads`) |

If `DATABASE_URL` is empty, the app falls back to `DATABASE_HOST/PORT/NAME/USER/PASSWORD`.

### Frontend (`frontend/.env`)

| Variable | Required | Description |
|---|---|---|
| `VITE_API_URL` | Only in production | Deployed backend URL, e.g. `https://api.example.com/api/v1`. Dev uses the Vite proxy. |

---

## Tests

Unit tests for pure-logic modules (no database or API key needed):

```bash
cd backend
python -m unittest discover -s tests -v
```

Covers: document chunker, question normalizer, interview planner, JWT +
password hashing, and the retrieval query builder (20 tests).

---

## Deployment

### 1. Database — Neon (free)

1. Create a free project at https://neon.tech.
2. Copy the connection string (the **pooled or direct** psycopg2 URL).
3. Keep it for the Render step.

### 2. Backend — Render (free)

**Option A — Blueprint (recommended).** A `render.yaml` is included:

1. Push this repository to GitHub.
2. Render → **New → Blueprint** → select the repo.
3. Fill in the prompted env vars:
   - `DATABASE_URL` → your Neon connection string
   - `GEMINI_API_KEY` → your Gemini key
4. Deploy. Render automatically runs `alembic upgrade head` before starting.

**Option B — Manual web service.**

- **Root directory:** `backend`
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Add the env vars from the table above, plus `PYTHON_VERSION=3.11.9`.
- Render shell (first deploy): `alembic upgrade head`.

### 3. Frontend — Vercel (free)

1. Import the repo on https://vercel.com.
2. **Root directory:** `frontend`
3. **Framework preset:** Vite
4. Build: `npm run build` · Output: `dist` (the included `vercel.json` adds
   SPA rewrites automatically).
5. Add env var: `VITE_API_URL = https://<your-render-app>.onrender.com/api/v1`
6. Deploy.

### 4. Post-deploy checklist

- `GET https://<your-app>.onrender.com/health` → `{"status":"ok"}`
- Register/login from the deployed frontend.
- Upload a resume and run a full interview.
- Update `CORS_ORIGINS` on Render to include your Vercel domain.

### Rebuilding the knowledge base index

The index is committed, so deploys don't rebuild it. To add real textbook
content (recommended before the demo):

1. Convert the assigned book chapters to markdown under
   `backend/knowledge_base/ai_ml/`.
2. Run `python scripts/build_index.py` locally (needs a valid
   `GEMINI_API_KEY`).
3. Commit `backend/knowledge_base/index/*`.

---

## Demo Video Plan

Suggested structure for the mandatory demo video (~5–7 minutes):

1. **Intro (30s)** — what the system does + the RAG idea in one sentence.
2. **Architecture walkthrough (45s)** — show the diagram above, explain the
   layered design.
3. **Auth (30s)** — register + login.
4. **Resume upload (45s)** — upload a PDF, show extracted skills.
5. **Interview (1.5 min)** — start interview, show generated questions tied to
   the resume, answer 2–3 questions.
6. **Evaluation (1 min)** — show scores, strengths/improvements, recommendation.
7. **Code walkthrough (1.5 min)** — InterviewService orchestration, the RAG
   pipeline, and one schema.
8. **Deployment (30s)** — show the live Render + Vercel URLs.
9. **Outro (15s)** — lessons learned + future scope.

---

## Key Design Decisions & Lessons Learned

- **One Gemini call per interview, not per question** — coherent interviews,
  predictable cost. The tradeoff is less adaptivity mid-interview (hence
  "Adaptive follow-up" in Future Scope).
- **Deterministic planner, generative questions** — the plan (skills × counts)
  is computed in code so the total is always predictable; Gemini fills in the
  actual questions. This makes the system auditable and testable.
- **Ownership checks on every interview endpoint** — a classic
  IDOR-vulnerability lesson: authenticated users can only read/answer their own
  interviews (repo-level `get_by_id_and_user`).
- **Singleton retriever** — the FAISS index + embedding service are loaded once
  per process, not per request. On Render's free tier this is the difference
  between a 3-second and a 20-second interview start.
- **Domain exceptions → HTTP status codes** — services raise typed exceptions;
  `main.py` maps them to 404/409/401/400. No more accidental 500s for "resume
  not found".
- **Committed FAISS index** — the vector store is part of the repo, so
  deployment skips re-embedding the whole book.
- **Gemini embeddings instead of bge-small-en-v1.5** — one API key, no local
  model download, still first-class embeddings. Documented tradeoff with a
  clear swap path.
- **Frontend designed like a job board, not a template** — the UI borrows the
  calm, information-dense structure of Indeed/Naukri (clean white surfaces,
  hairline borders, one restrained blue accent) under a distinct identity
  ("InterviewDesk"): Inter typography, split-screen auth, a focused
  full-screen interview workspace, skeleton loading, meaningful empty states,
  and user-friendly error copy. Only functionality backed by a real endpoint
  is enabled — the Resume page's education/experience/projects/certifications
  sections are wired to an isolated service call (`getParsedResumeDetails`)
  that lights up when the backend exposes those fields.
- **Migrations are a chain, and order matters** — a real bug was caught by
  generating the offline SQL: drop statements that ran at *import time* (module
  level) instead of inside `upgrade()` would have broken a fresh deploy. Always
  verify `alembic upgrade head --sql` on a clean checkout.

---

*Assignment submission: AI/ML & Backend Engineering Intern — RAG-based role
candidate screening. See `docs/PROJECT_REPORT.md` for the full module audit.*
