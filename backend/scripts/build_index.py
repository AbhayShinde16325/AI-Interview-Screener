"""
Builds the FAISS index from the markdown knowledge base.

Usage (from the backend/ directory):

    python scripts/build_index.py

What it does:
    1. Loads every *.md file under knowledge_base/
    2. Chunks each document (heading-aware, with overlap)
    3. Embeds every chunk with Gemini embeddings
    4. Writes knowledge_base/index/faiss.index + metadata.json

The committed index can be rebuilt any time the knowledge base changes.
"""

import logging
import sys
from pathlib import Path

# Allow running as `python scripts/build_index.py` from backend/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.ai.embeddings.index_builder import IndexBuilder  # noqa: E402
from app.core.logging import setup_logging  # noqa: E402

setup_logging()
logger = logging.getLogger("build_index")


def main() -> None:
    logger.info("Starting knowledge base index build...")

    builder = IndexBuilder()
    builder.build()

    logger.info("Index build finished.")


if __name__ == "__main__":
    main()
