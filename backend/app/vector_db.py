import chromadb
import uuid

client = chromadb.Client()

class VectorDB:
    def __init__(self, chunks):
        collection_id = str(uuid.uuid4())
        self.collection = client.create_collection(collection_id)
        chunk_ids = ['doc_' + str(id) for id in range(len(chunks))]
        self.collection.add(
            documents=chunks,
            ids=chunk_ids
        )

    def topk(self, query, k = 1):
        results = self.collection.query(
            query_texts=[query],
            n_results=k)
        return results['documents'][:k]


