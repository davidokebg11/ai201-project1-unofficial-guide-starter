import os
from dotenv import load_dotenv
load_dotenv()
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from ingest import process_documents

def build_vector_store():
    chunks = process_documents()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="freshman_tips")
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk["text"]).tolist()
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[{"source": chunk["source"], "chunk_index": chunk["chunk_index"]}]
        )
    return collection, model

def ask(question):
    collection, model = build_vector_store()
    
    query_embedding = model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
    
    chunks = results["documents"][0]
    sources = list(set([m["source"] for m in results["metadatas"][0]]))
    context = "\n\n".join(chunks)
    
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    prompt = f"""You are a helpful assistant for college freshmen.
Answer the question using ONLY the information provided in the documents below.
If the documents don't contain enough information to answer, say "I don't have enough information on that."
Always be specific and cite which document your answer comes from.

Documents:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return {
        "answer": response.choices[0].message.content,
        "sources": sources
    }

if __name__ == "__main__":
    print("Testing end-to-end query...\n")
    result = ask("How should I handle homesickness in college?")
    print("Answer:", result["answer"])
    print("\nSources:", result["sources"])