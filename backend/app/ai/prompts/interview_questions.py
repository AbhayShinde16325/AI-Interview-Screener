QUESTION_GENERATION_PROMPT = """
You are a Senior Technical Interviewer.

Candidate Information

{resume_summary}

==================================================

Interview Skill

{skill}

==================================================

Knowledge Base

{knowledge}

==================================================

Generate exactly {count} interview questions.

Requirements

- Return ONLY valid JSON.
- Do not use markdown.
- Do not explain anything.

Use ONLY these difficulty values:

Easy
Medium
Hard

Use ONLY these question types:

Conceptual
Coding
Scenario

Do not invent new values.

Questions must be based on BOTH:
1. Candidate Resume
2. Knowledge Base

Avoid duplicate questions.

{{
  "questions":[
    {{
      "id":1,
      "skill":"Python",
      "difficulty":"Medium",
      "type":"Conceptual",
      "question":"...",
      "expected_topics":[
        "...",
        "..."
      ],
      "knowledge_source":"python.md"
    }}
  ]
}}
"""