import os

def load_documents(folder_path="documents"):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({
                "filename": filename,
                "text": text
            })
            print(f"Loaded: {filename}")
    return documents

def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if len(chunk.strip()) > 0:
            chunks.append(chunk)
        start = end - overlap
    return chunks

def process_documents(folder_path="documents"):
    documents = load_documents(folder_path)
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["filename"],
                "chunk_index": i,
                "text": chunk
            })
    print(f"\nTotal chunks created: {len(all_chunks)}")
    return all_chunks

if __name__ == "__main__":
    chunks = process_documents()
    print("\n--- 5 Sample Chunks ---")
    for chunk in chunks[:5]:
        print(f"\nSource: {chunk['source']}")
        print(f"Chunk {chunk['chunk_index']}:")
        print(chunk['text'])
        print("-" * 40)