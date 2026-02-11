# check_database.py
from tools import PaperDatabase
import os

print("=== DATABASE VERIFICATION ===")

# Check actual database content
db = PaperDatabase()
all_papers = db.get_stored_papers(limit=1000)  # Remove the limit
print(f"Total papers in database: {len(all_papers)}")

# Check if multiple database files exist
db_files = [f for f in os.listdir('.') if f.endswith('.db')]
print(f"Database files found: {db_files}")

# Show first 10 papers with full details
print(f"\nFirst 10 papers:")
for i, paper in enumerate(all_papers[:10]):
    print(f"{i+1}. {paper['title']} ({paper['year']})")

print(f"\nLast 10 papers:")
for i, paper in enumerate(all_papers[-10:], len(all_papers)-9):
    print(f"{i}. {paper['title']} ({paper['year']})")