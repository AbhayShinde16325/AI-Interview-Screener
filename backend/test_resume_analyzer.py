from app.ai.resume_parser.analyzer import ResumeAnalyzer
from app.parsers.pdf_parser import PDFParser

resume_text = PDFParser.extract_text(
    "uploads/94950cf5-5550-413b-8da9-31535ecd99f1.pdf"
)

analyzer = ResumeAnalyzer()

parsed_resume = analyzer.analyze(
    resume_text,
)

print(parsed_resume.model_dump_json(indent=2))


