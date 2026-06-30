from pathlib import Path


class KnowledgeBaseLoader:
    """
    Loads every markdown file from the knowledge base.
    """

    def __init__(
        self,
        knowledge_base_path: str = "knowledge_base",
    ):
        self.base_path = Path(
            knowledge_base_path
        )

    def load_documents(self) -> list[dict]:

        documents = []

        for md_file in self.base_path.rglob("*.md"):

            with open(
                md_file,
                "r",
                encoding="utf-8",
            ) as f:

                documents.append(
                    {
                        "category": md_file.parent.name,
                        "filename": md_file.name,
                        "content": f.read(),
                    }
                )

        return documents