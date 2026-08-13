class ContextBuilder:
    """
    Converts retrieved chunks into a prompt-ready context.

    Deduplicates by (filename, chunk_number) instead of exact text, so the
    same source chunk retrieved for different skills appears only once.
    """

    def build(self, retrieval_results: list[dict]) -> str:
        seen = set()
        sections = []

        for result in retrieval_results:
            metadata = result["metadata"]

            key = (
                metadata.get("filename"),
                metadata.get("chunk_number"),
            )

            if key in seen:
                continue

            seen.add(key)

            sections.append(
                f"Source: {metadata['filename']} "
                f"(chunk {metadata.get('chunk_number', '?')})\n\n"
                f"{metadata['content']}"
            )

        if not sections:
            return ""

        separator = "\n\n" + "=" * 80 + "\n\n"
        return separator.join(sections)
