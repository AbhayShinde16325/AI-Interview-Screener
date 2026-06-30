from app.parsers.pdf_parser import PDFParser
from app.ai.resume_parser.analyzer import ResumeAnalyzer
from app.ai.interview.planner import InterviewPlanner

# Use an existing PDF
pdf_path = "uploads/96d8c9e8-d8ba-47d4-a6ff-3b2ae912b1a3.pdf"

resume_text = PDFParser.extract_text(pdf_path)

parsed_resume = ResumeAnalyzer().analyze(
    resume_text
)

planner = InterviewPlanner()

plan = planner.create_plan(
    parsed_resume
)

print(plan)