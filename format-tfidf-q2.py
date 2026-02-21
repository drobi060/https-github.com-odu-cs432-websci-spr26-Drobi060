#!/usr/bin/env python3
"""
Extract exactly top 10 from different domains for Q2
"""

import re

# Read the results file
with open("tfidf_results_research.txt", 'r') as f:
    content = f.read()

# Parse the data section
lines = content.split('\n')
data_start = False
results = []

for line in lines:
    if 'Rank' in line and 'TF-IDF' in line:
        data_start = True
        continue
    if data_start and line.strip() and not line.startswith('-') and not line.startswith('='):
        # Parse line
        parts = line.split(None, 6)  # Split on whitespace, max 6 parts
        if len(parts) >= 7 and parts[0].isdigit():
            try:
                rank = int(parts[0])
                tfidf = float(parts[1])
                tf = float(parts[2])
                idf = float(parts[3])
                uri = ' '.join(parts[6:]).strip()
                
                # Extract domain
                if '://' in uri:
                    domain = uri.split('//')[1].split('/')[0]
                else:
                    domain = uri.split('/')[0]
                
                results.append({
                    'rank': rank,
                    'tfidf': tfidf,
                    'tf': tf,
                    'idf': idf,
                    'uri': uri,
                    'domain': domain
                })
            except (ValueError, IndexError):
                pass

# Get unique domains (top 10)
seen_domains = set()
top_10 = []

for result in results:
    if result['domain'] not in seen_domains:
        top_10.append(result)
        seen_domains.add(result['domain'])
        if len(top_10) == 10:
            break

# Print markdown table
print("# Q2: TF-IDF Rankings for Query Term 'research'\n")
print("## Methodology\n")
print("**Query Term**: research")
print("**Document Frequency**: 171 documents contain this term")
print("**Corpus Size**: 40,000,000,000 (Google estimate from worldwidewebsize.com)\n")
print("**Formulas**:")
print("- IDF = log₂(Corpus Size / Document Frequency) = log₂(40,000,000,000 / 171) = 27.8014")
print("- TF = (Term Frequency in Document) / (Total Words in Document)")
print("- TF-IDF = TF × IDF\n")

print("## Rankings - Top 10 Results (Different Domains)\n")
print("| Rank | TF-IDF | TF | IDF | URI |")
print("|---:|---:|---:|---:|---|")

for i, result in enumerate(top_10, 1):
    tfidf_str = f"{result['tfidf']:.6f}"
    tf_str = f"{result['tf']:.8f}"
    idf_str = f"{result['idf']:.4f}"
    print(f"| {i} | {tfidf_str} | {tf_str} | {idf_str} | {result['uri']} |")

# Save the top 10 for PageRank lookup in Q3
print("\n\n## Top 10 URIs for Q3 PageRank Lookup\n")
for i, result in enumerate(top_10, 1):
    print(f"{i}. {result['uri']}")

# Save to file for Q3
with open("q2_top_10_uris.txt", 'w') as f:
    for i, result in enumerate(top_10, 1):
        f.write(f"{i}\t{result['uri']}\t{result['tfidf']:.6f}\n")

print("\nTop 10 URIs saved to q2_top_10_uris.txt")
