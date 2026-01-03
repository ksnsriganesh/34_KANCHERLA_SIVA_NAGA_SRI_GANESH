from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class FinancialEvidenceStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)
        self.text_chunks = []

    def add_documents(self, documents: list):
        """
        documents: list of strings (financial facts / metrics)
        """
        embeddings = self.model.encode(documents)
        self.index.add(np.array(embeddings).astype("float32"))
        self.text_chunks.extend(documents)

    def retrieve(self, query: str, top_k: int = 3) -> list:
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(
            np.array(query_embedding).astype("float32"),
            top_k
        )

        return [self.text_chunks[i] for i in indices[0]]
