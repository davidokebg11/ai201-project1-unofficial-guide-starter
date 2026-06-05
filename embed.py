import chromadb
from sentence_transformers import SentenceTransformer
from ingest import process_documents

def build_vector_store():
    print("Loading documents and chunks...")
    chunks = process_documents()

    print("\nLoading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Setting up ChromaDB...")
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="freshman_tips")

    print("Embedding and storing chunks...")
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk["text"]).tolist()
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[{"source": chunk["source"], "chunk_index": chunk["chunk_index"]}]
        )

    print(f"\nStored {len(chunks)} chunks in vector store!")
    return collection, model

def search(query, collection, model, k=5):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    return results

if __name__ == "__main__":
    collection, model = build_vector_store()

    print("\n--- Testing Retrieval ---")
    test_queries = [
        "How do I deal with homesickness in college?",
        "What should I do about textbooks?",
        "How important is going to office hours?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        results = search(query, collection, model)
        for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            print(f"\n  Result {i+1} (source: {meta['source']}):")
            print(f"  {doc[:200]}...")
        print("-" * 40)