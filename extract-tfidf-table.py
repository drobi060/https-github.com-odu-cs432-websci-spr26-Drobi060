#!/usr/bin/env python3
"""
Extract top 10 results with TF values for Q2 table
"""

import re
import math

def extract_top_10_tfidf():
    """Extract top 10 results and create formatted table"""
    
    # Read the detailed results
    with open("tfidf_results_research.txt", 'r') as f:
        content = f.read()
    
    # Parse the results
    lines = content.split('\n')
    
    # Find data lines
    data_lines = []
    in_data = False
    for line in lines:
        if line.startswith('-'*50):
            in_data = True
            continue
        if in_data and line.strip() and not line.startswith('=='):
            data_lines.append(line)
    
    # Parse each line
    results = []
    for line in data_lines[:15]:  # Get first 15 to ensure we have 10 with different domains
        parts = line.split()
        if len(parts) >= 8:
            try:
                rank = int(parts[0])
                tfidf = float(parts[1])
                tf = float(parts[2])
                idf = float(parts[3])
                # URI is everything after the 7th field
                uri_start = sum(len(p) + 1 for p in parts[:7])
                uri = line[uri_start:].strip()
                
                results.append({
                    'rank': rank,
                    'tfidf': tfidf,
                    'tf': tf,
                    'idf': idf,
                    'uri': uri
                })
            except (ValueError, IndexError):
                pass
    
    # Get top 10 from different domains
    seen_domains = set()
    top_10 = []
    
    for result in results:
        domain = result['uri'].split('/')[2] if '://' in result['uri'] else result['uri']
        if domain not in seen_domains:
            top_10.append(result)
            seen_domains.add(domain)
            if len(top_10) == 10:
                break
    
    # Print Markdown table
    print("# Q2: TF-IDF Rankings for 'research'\n")
    print("## Computation Details\n")
    print("- **Query Term**: research")
    print("- **Document Frequency (DF)**: 171")
    print("- **Corpus Size**: 40,000,000,000 (Google estimate)")
    print("- **IDF Formula**: log₂(Corpus Size / DF) = log₂(40,000,000,000 / 171) = 27.8014")
    print("- **TF Formula**: (Term Count in Document) / (Total Words in Document)")
    print("- **TF-IDF Formula**: TF × IDF\n")
    
    print("## Rankings\n")
    print("| Rank | TF-IDF | TF | IDF | URI |")
    print("|------|--------|-----|-----|-----|")
    
    for i, result in enumerate(top_10, 1):
        print(f"| {i} | {result['tfidf']:.6f} | {result['tf']:.8f} | {result['idf']:.4f} | {result['uri']} |")
    
    return top_10

if __name__ == "__main__":
    results = extract_top_10_tfidf()
    
    # Save for later use
    with open("q2_tfidf_table.txt", 'w') as f:
        f.write("Top 10 Results for Q2\n")
        f.write("="*100 + "\n\n")
        for i, result in enumerate(results, 1):
            f.write(f"{i}. {result['uri']}\n")
            f.write(f"   TF-IDF: {result['tfidf']:.6f}, TF: {result['tf']:.8f}, IDF: {result['idf']:.4f}\n\n")
