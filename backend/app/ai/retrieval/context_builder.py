class ContextBuilder:
    """
    Converts retrieved chunks into a prompt-ready context.
    """

    def build(
        self,
        retrieval_results: list[dict],
    ) -> str:

        sections = []

        for result in retrieval_results:

            metadata = result["metadata"]

            section = (
                f"Source: {metadata['filename']}\n\n"
                f"{metadata['content']}"
            )

            sections.append(section)

        return "\n\n" + "=" * 80 + "\n\n".join(sections)