import requests
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------
QUERY = "artificial intelligence automation emerging technology"
NUM_PAPERS = 15
FIELDS = "title,abstract,year,citationCount,influentialCitationCount,venue"
OUTPUT_FILE = "sources.txt"

# -----------------------------
# Semantic Scholar API call
# -----------------------------
url = "https://api.semanticscholar.org/graph/v1/paper/search"
params = {
    "query": QUERY,
    "limit": NUM_PAPERS,
    "fields": FIELDS
}

response = requests.get(url, params=params)
data = response.json()

# -----------------------------
# Simple cutting research score
# -----------------------------
def cutting_score(paper):
    """
    Compute a simple score:
    - More recent papers → higher score
    - More citations → higher score
    """
    current_year = datetime.now().year
    year_score = max(0, 1 - (current_year - paper.get("year", current_year)) * 0.1)  # recent papers = higher
    citation_score = min(1, paper.get("citationCount", 0) / 100)  # normalize by 100 citations
    return round((year_score + citation_score) / 2, 2)

# -----------------------------
# Save results to a file
# -----------------------------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(f"Top {NUM_PAPERS} papers for query: '{QUERY}'\n\n")
    for paper in data.get("data", []):
        score = cutting_score(paper)
        f.write(f"Title: {paper.get('title')}\n")
        f.write(f"Year: {paper.get('year')}, Citations: {paper.get('citationCount')}, Score: {score}\n")
        abstract = paper.get("abstract", "No abstract available")
        f.write(f"Abstract: {abstract[:500]}{'...' if len(abstract) > 500 else ''}\n")
        f.write("-" * 80 + "\n")

print(f"Saved {NUM_PAPERS} papers to '{OUTPUT_FILE}'")
