# Production deployment

This repository is configured for Neon (PostgreSQL), Render (FastAPI), and
Vercel (Vite/React). Deploy the backend first, then the frontend.

## 1. Create required accounts and values

Create a Neon PostgreSQL database and copy its connection string. Create a
Google Gemini API key. Keep both values private: they belong in the hosting
provider's environment-variable settings, never in Git.

## 2. Deploy the API on Render

1. Push this repository to GitHub.
2. In Render, choose **New > Blueprint** and select the repository.
3. Render reads `render.yaml`; set the prompted values:
   - `DATABASE_URL`: Neon connection string.
   - `GEMINI_API_KEY`: Gemini API key.
4. Deploy. The Blueprint runs Alembic migrations during the build and probes
   `/health`, which also verifies PostgreSQL connectivity.
5. Copy the API URL, for example `https://ai-interview-screener-api.onrender.com`.

## 3. Deploy the frontend on Vercel

1. In Vercel, import the same GitHub repository.
2. Set **Root Directory** to `frontend` and the framework to **Vite**.
3. Add this **Production** environment variable:

   ```text
   VITE_API_URL=https://ai-interview-screener-api.onrender.com/api/v1
   ```

4. Deploy and copy the resulting `*.vercel.app` production URL.

## 4. Connect both services

In the Render service settings, set `CORS_ORIGINS` to the exact Vercel URL, for
example:

```text
https://ai-interview-screener.vercel.app
```

Redeploy the API. Do not use a wildcard CORS origin: the API accepts
JWT-authenticated browser requests. If the API URL changes in the future, update
`VITE_API_URL` in Vercel and redeploy the frontend because Vite embeds this
value at build time.

## 5. Verify the public release

1. Visit `https://<render-service>/health`; expect:

   ```json
   {"status":"ok","database":"ok"}
   ```

2. Open the Vercel URL in an incognito window.
3. Register a test account, upload a text-based PDF, create an interview, and
   submit answers through the final evaluation screen.

## Data handling

Resume PDFs are stored only temporarily while text is extracted, then deleted.
The extracted text and parsed resume data are stored in PostgreSQL. If a future
version needs original-file downloads, add private object storage (for example
S3, R2, or Vercel Blob) before exposing that capability.
