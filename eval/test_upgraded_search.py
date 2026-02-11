"""
Test the upgraded semantic search
Compare old vs new embeddings
"""

from memory_manager import MemoryManager
import time

print("="*70)
print("TESTING UPGRADED SEMANTIC SEARCH")
print("="*70)
print()

# Test query
test_query = "BERT language model"
print(f"Test query: '{test_query}'")
print()

# Test new (upgraded) system
print("Testing NEW system (all-mpnet-base-v2)...")
print("-"*70)

memory_new = MemoryManager(
    chroma_path="./chroma_db_mpnet",
    embedding_model="all-mpnet-base-v2"
)

start = time.time()
results_new = memory_new.search_papers(test_query, top_k=5)
time_new = time.time() - start

print(f"Found {len(results_new)} papers in {time_new*1000:.1f}ms")
print()
print("Top 3 results:")
for i, paper in enumerate(results_new[:3], 1):
    print(f"{i}. {paper['title'][:60]}...")
    print(f"   Similarity: {paper['similarity']:.3f}")
print()

# Try to test old system (if it exists)
print("Testing OLD system (all-MiniLM-L6-v2)...")
print("-"*70)

try:
    memory_old = MemoryManager(
        chroma_path="./chroma_db",
        embedding_model="all-MiniLM-L6-v2"
    )
    
    start = time.time()
    results_old = memory_old.search_papers(test_query, top_k=5)
    time_old = time.time() - start
    
    print(f"Found {len(results_old)} papers in {time_old*1000:.1f}ms")
    print()
    print("Top 3 results:")
    for i, paper in enumerate(results_old[:3], 1):
        print(f"{i}. {paper['title'][:60]}...")
        print(f"   Similarity: {paper['similarity']:.3f}")
    print()
    
    # Compare
    print("="*70)
    print("COMPARISON")
    print("="*70)
    print(f"Speed difference: {(time_new - time_old)*1000:.1f}ms (new is {'slower' if time_new > time_old else 'faster'})")
    print()
    
    # Check overlap
    new_ids = {p['id'] for p in results_new[:5]}
    old_ids = {p['id'] for p in results_old[:5]}
    overlap = len(new_ids & old_ids)
    print(f"Result overlap: {overlap}/5 papers in common")
    print(f"New unique papers: {len(new_ids - old_ids)}")
    print()
    
except Exception as e:
    print(f"Could not load old system: {e}")
    print("(This is okay if you deleted ./chroma_db)")
    print()

print("="*70)
print("✓ TEST COMPLETE")
print("="*70)
print()
print("New semantic search is working!")
print("Ready to proceed to Step 2: Improve BM25")
print()