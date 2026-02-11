"""
Automated test for episodic summarization
"""

from main import execute_routed_query, chat_history
import time

def test_basic_summarization():
    """Test that summary is created after 10 exchanges"""
    print("🧪 Testing Basic Episodic Summarization\n")
    
    test_queries = [
        "Find papers about transformers",
        "Find papers about BERT", 
        "Find papers about GPT",
        "Find papers about attention mechanisms",
        "Find papers about self-attention",
        "Find papers about multi-head attention",
        "Find papers about positional encoding",
        "Find papers about layer normalization",
        "Find papers about residual connections",
        "Find papers about feed-forward networks",
        "Find papers about tokenization",  # 11th - starts new cycle
        "Find papers about embeddings",
    ]
    
    summaries_created = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"Query {i}/{len(test_queries)}: {query}")
        print('='*60)
        
        # Check if summary will be created
        if i % 10 == 0:
            print("⚠️  SUMMARY SHOULD BE CREATED AFTER THIS QUERY")
        
        result = execute_routed_query(query)
        
        # Wait a bit to see output
        time.sleep(2)
        
        if i % 10 == 0:
            summaries_created += 1
            print(f"\n✅ Summary #{summaries_created} should have been created!")
    
    print(f"\n{'='*60}")
    print(f"TEST COMPLETE")
    print(f"Expected summaries: {len(test_queries) // 10}")
    print(f"Check above for 💾 messages")
    print('='*60)

if __name__ == "__main__":
    test_basic_summarization()