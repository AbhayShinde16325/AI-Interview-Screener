from pathlib import Path

import faiss
import numpy as np
import json

class FAISSStore:
    """
    Handles storing and searching vector embeddings.
    """

    def __init__(
        self,
        dimension: int = 3072,
    ):
        self.dimension = dimension

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.metadata = []

    # -------------------------------

    def add(
        self,
        embedding: list[float],
        metadata: dict,
    ) -> None:

        vector = np.array(
            [embedding],
            dtype=np.float32,
        )

        self.index.add(vector)

        self.metadata.append(metadata)

    # -------------------------------

    def search(
        self,
        embedding: list[float],
        k: int = 5,
    ):

        vector = np.array(
            [embedding],
            dtype=np.float32,
        )

        distances, indices = self.index.search(
            vector,
            k,
        )

        results = []

        for distance, idx in zip(
            distances[0],
            indices[0],
        ):

            if idx == -1:
                continue

            results.append(
                {
                    "distance": float(distance),
                    "metadata": self.metadata[idx],
                }
            )

        return results

    # -------------------------------
    def save(
        self,
        index_path: str,
        metadata_path: str,
    ):

        index_file = Path(index_path)
        index_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            self.index,
            str(index_file),
        )

        with open(
            metadata_path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                self.metadata,
                f,
                indent=2,
                ensure_ascii=False,
            )

    # -------------------------------

    def load(
        self,
        index_path: str,
        metadata_path: str,
    ):

        self.index = faiss.read_index(
        index_path,
        )

        with open(
        metadata_path,
        "r",
        encoding="utf-8",
        ) as f:

            self.metadata = json.load(f)