from app.parsers.pdf_parser import PDFParser

text = PDFParser.extract_text(
    "uploads/a0d0cba3-c242-42c4-953e-3a3cc7d41859.pdf"
)

print(text[:1000])