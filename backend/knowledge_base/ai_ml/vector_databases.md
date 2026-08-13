# Vector Databases and Similarity Search

## Why Vector Search

Machine learning models represent text, images, and other data as embedding
vectors. Finding similar items means finding nearby vectors in a high
dimensional space.

## Approximate Nearest Neighbor (ANN)

Exact nearest-neighbor search is too slow for millions of vectors. ANN
algorithms trade a little accuracy for large speed gains.

- **Flat index (exact)**: brute-force scan, exact but slow.
- **IVF (inverted file)**: clusters vectors, searches only the closest
  clusters. Fast and memory friendly.
- **HNSW**: builds a graph of similar items; excellent recall and speed,
  higher memory usage.
- **PQ (product quantization)**: compresses vectors, very low memory, lower
  precision.

## FAISS

FAISS is a library for efficient similarity search, developed by Meta. It
stores vectors in an in-memory index and returns the k nearest neighbors plus
their distances. Metadata (source filename, chunk number, content) is kept
alongside so retrieved vectors can be traced back to their documents.

## Distance Metrics

- **L2 (Euclidean)**: distance in absolute space.
- **Cosine**: angle between vectors, robust to vector length differences.

## Common Interview Questions

- What is the difference between an exact and an approximate index?
- When would you choose HNSW over a flat index?
- What does "k" mean in k-nearest-neighbor search?
- How is metadata stored alongside vectors?
- How do you measure if a retrieval system is good?
