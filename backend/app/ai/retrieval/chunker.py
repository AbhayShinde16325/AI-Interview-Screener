import re
from typing import List


class DocumentChunker:
    """
    Markdown-aware document chunker.

    Priority:
    1. Markdown headings
    2. Paragraphs
    3. Sentences
    4. Character split (last resort)

    This implementation avoids breaking semantic context whenever possible.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 150,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        """
        Split an entire markdown document.
        """

        sections = self._split_sections(text)

        chunks = []

        for section in sections:
            chunks.extend(
                self._chunk_section(section)
            )

        return chunks

    # --------------------------------------------------

    def _split_sections(
        self,
        text: str,
    ) -> List[str]:
        """
        Split document by markdown headings.
        """

        lines = text.splitlines()

        sections = []

        current = []

        for line in lines:

            if line.startswith("#") and current:
                sections.append(
                    "\n".join(current).strip()
                )
                current = []

            current.append(line)

        if current:
            sections.append(
                "\n".join(current).strip()
            )

        return sections

    # --------------------------------------------------

    def _chunk_section(
        self,
        section: str,
    ) -> List[str]:

        paragraphs = [
            p.strip()
            for p in section.split("\n\n")
            if p.strip()
        ]

        chunks = []

        current_chunk = ""

        for paragraph in paragraphs:

            # Paragraph fits
            if (
                len(current_chunk)
                + len(paragraph)
                + 2
                <= self.chunk_size
            ):

                if current_chunk:
                    current_chunk += "\n\n"

                current_chunk += paragraph

            else:

                # Paragraph itself is huge
                if len(paragraph) > self.chunk_size:

                    if current_chunk:
                        chunks.append(current_chunk)
                        current_chunk = ""

                    chunks.extend(
                        self._split_large_paragraph(
                            paragraph
                        )
                    )

                else:

                    if current_chunk:
                        chunks.append(current_chunk)

                    overlap = ""

                    if chunks:
                        overlap = chunks[-1][
                            -self.overlap :
                        ]

                    current_chunk = (
                        overlap
                        + "\n\n"
                        + paragraph
                    )

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    # --------------------------------------------------

    def _split_large_paragraph(
        self,
        paragraph: str,
    ) -> List[str]:

        """
        Split oversized paragraph into sentences.
        """

        sentences = re.split(
            r'(?<=[.!?])\s+',
            paragraph,
        )

        chunks = []

        current = ""

        for sentence in sentences:

            if (
                len(current)
                + len(sentence)
                + 1
                <= self.chunk_size
            ):

                current += (
                    sentence + " "
                )

            else:

                if current:
                    chunks.append(
                        current.strip()
                    )

                # Extremely long sentence
                if len(sentence) > self.chunk_size:

                    for i in range(
                        0,
                        len(sentence),
                        self.chunk_size,
                    ):

                        chunks.append(
                            sentence[
                                i : i
                                + self.chunk_size
                            ]
                        )

                    current = ""

                else:

                    current = sentence + " "

        if current:
            chunks.append(current.strip())

        return chunks