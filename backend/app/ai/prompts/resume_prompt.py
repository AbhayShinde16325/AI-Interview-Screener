RESUME_ANALYSIS_PROMPT = """
You are an expert technical recruiter.

Analyze the following resume.

Return ONLY valid JSON.

Do not return markdown.

Do not explain anything.

The response MUST exactly follow this schema.

{{
  "summary": "Short professional summary",

  "skills": [
    "Python",
    "FastAPI"
  ],

  "education": [
    {{
      "degree": "Bachelor of Engineering",
      "institution": "ABC University",
      "graduation_year": "2027"
    }}
  ],

  "experience": [
    {{
      "company": "PGAGI",
      "role": "AI/ML Intern",
      "duration": "Jan 2026 - Present"
    }}
  ],

  "projects": [
    {{
      "title": "AI Interview Screener",
      "description": "LLM powered interview platform",
      "technologies": [
        "FastAPI",
        "PostgreSQL",
        "Gemini"
      ]
    }}
  ],

  "certifications": [
    "AWS Cloud Practitioner"
  ],

  "keywords": [
    "Python",
    "LLM",
    "Machine Learning"
  ]
}}

Rules:

- Every project MUST contain:
  - title
  - description
  - technologies

- Every experience MUST contain:
  - company
  - role
  - duration

- Do not rename fields.

- Do not invent new keys.

Resume:

{resume_text}
"""