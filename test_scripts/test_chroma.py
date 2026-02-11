import chromadb
from sentence_transformers import SentenceTransformer

# Test 1: Can we create a ChromaDB client?
print("Test 1: Creating ChromaDB client...")
client = chromadb.PersistentClient(path="./chroma_test_db")
print("✓ Client created")

# Test 2: Can we create a collection?
print("\nTest 2: Creating collection...")
collection = client.get_or_create_collection(name="test_collection")
print(f"✓ Collection created: {collection.name}")

# Test 3: Can we load the embedding model?
print("\nTest 3: Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✓ Model loaded")

# Test 4: Can we create embeddings?
print("\nTest 4: Creating embeddings...")
test_text = "This is a test about neural networks"
embedding = model.encode(test_text)
print(f"✓ Embedding created, dimension: {len(embedding)}")

# Test 5: Can we store and retrieve?
print("\nTest 5: Storing and retrieving...")
collection.add(
    documents=["This is about neural networks"],
    embeddings=[embedding.tolist()],
    ids=["test_1"]
)
results = collection.query(
    query_embeddings=[embedding.tolist()],
    n_results=1
)
print(f"✓ Retrieved: {results['documents'][0]}")

print("\n🎉 All tests passed! ChromaDB is working.")