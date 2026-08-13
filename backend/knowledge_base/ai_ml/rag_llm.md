# LLMs and Retrieval-Augmented Generation

## Large Language Models

Large language models are trained to predict the next token in a sequence over
enormous text corpora. They can follow instructions, reason, and generate
coherent text. Common limitations are hallucination (confidently stating false
information) and stale knowledge (training data has a cutoff date).

## Retrieval-Augmented Generation (RAG)

RAG grounds the model's answer in an external knowledge base:

1. A query is embedded and searched against a vector store.
2. The top relevant chunks are retrieved.
3. Chunks are injected into the prompt as context.
4. The model answers using only that context.

Benefits: up-to-date knowledge, reduced hallucination, and the ability to cite
sources. The two main stages are ingestion (chunk, embed, index) and retrieval
(embed query, search, rank).

## Chunking

Documents must be split into chunks small enough to fit the model context and
retrievable at the right granularity. Heading-aware chunking preserves
semantic boundaries; a small overlap between chunks avoids cutting ideas in
half. Chunk size is a tradeoff between precision and context.

## Embeddings

Embeddings map text to dense vectors where semantically similar text is close
in vector space. Similarity is usually measured with cosine similarity or
Euclidean distance.

## Common Interview Questions

- What is RAG and why is it useful?
- How would you reduce hallucination in an LLM application?
- What is a vector database and when would you use one?
- How do you choose a chunk size for a knowledge base?
- What is the difference between fine-tuning and RAG?
