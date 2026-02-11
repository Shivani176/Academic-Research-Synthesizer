print("Installing all-mpnet-base-v2...")
print("This model is larger but much better for academic text")
print()

from sentence_transformers import SentenceTransformer

# Download the model
print("Downloading model (this may take 2-3 minutes)...")
model = SentenceTransformer('all-mpnet-base-v2')

# Test it
print("\nTesting model...")
test_text = "BERT uses bidirectional transformers for language understanding"
embedding = model.encode(test_text)

print(f"✓ Model loaded successfully!")
print(f"  Embedding dimensions: {len(embedding)}")
print(f"  Model type: {model.__class__.__name__}")
print()
print("Ready to use!")

"""
Install and test the better embedding model
"""

print("Installing all-mpnet-base-v2...")
print("This model is larger but much better for academic text")
print()

from sentence_transformers import SentenceTransformer

# Download the model
print("Downloading model (this may take 2-3 minutes)...")
model = SentenceTransformer('all-mpnet-base-v2')

# Test it
print("\nTesting model...")
test_text = "BERT uses bidirectional transformers for language understanding"
embedding = model.encode(test_text)

print(f"✓ Model loaded successfully!")
print(f"  Embedding dimensions: {len(embedding)}")
print(f"  Model type: {model.__class__.__name__}")
print()
print("Ready to use!")