import fitz


class PDFParser:

    @staticmethod
    def extract_text(
        file_path: str,
    ) -> str:
        """
        Extract all text from a PDF.
        """

        document = fitz.open(file_path)

        extracted_text = ""

        for page in document:
            extracted_text += page.get_text()

        document.close()

        return extracted_text.strip()