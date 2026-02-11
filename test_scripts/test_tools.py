from tools import (
    PaperDatabase, 
    check_stored_papers, 
    find_paper_connections, 
    find_semantic_connections, 
    find_research_bridges
)

print("=== TESTING DATABASE ===")
result = check_stored_papers()
print(result)

print("\n=== TESTING TITLE CONNECTIONS ===")
result = find_paper_connections()
print(result)

print("\n=== TESTING SEMANTIC CONNECTIONS ===")
result = find_semantic_connections()
print(result)

print("\n=== TESTING BRIDGE ANALYSIS ===")
result = find_research_bridges()
print(result)