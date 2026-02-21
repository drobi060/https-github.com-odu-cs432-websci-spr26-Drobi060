#!/usr/bin/env python3
"""
Compute TF-IDF rankings for a query term
"""

import os
import re
import math
from pathlib import Path
from urllib.parse import urlparse

def get_word_count(text_file):
    """Get total word count from a processed text file"""
    try:
        with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        words = re.findall(r'\b[a-z]+\b', content.lower())
        return len(words)
    except:
        return 0

def count_term_occurrences(text_file, query_term):
    """Count occurrences of query term in document"""
    try:
        with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
        # Use word boundaries to match whole words only
        pattern = r'\b' + re.escape(query_term) + r'\b'
        occurrences = len(re.findall(pattern, content))
        return occurrences
    except:
        return 0

def compute_tfidf(query_term, processed_dir="processed_text", mapping_file="uri_mapping.txt", 
                  corpus_size=40_000_000_000, use_bing=False):
    """
    Compute TF-IDF for all documents containing the query term
    
    Args:
        query_term: The term to search for
        processed_dir: Directory containing processed text files
        mapping_file: File mapping hashes to URIs
        corpus_size: Total size of search engine corpus
        use_bing: If True, use Bing corpus size (4 billion), else Google (40 billion)
    """
    
    if use_bing:
        corpus_size = 4_000_000_000
    
    # Load URI mapping
    uri_map = {}
    with open(mapping_file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t', 1)
            if len(parts) == 2:
                uri_map[parts[0]] = parts[1]
    
    # Get all processed files
    text_files = sorted(Path(processed_dir).glob("*.txt"))
    print(f"Searching {len(text_files)} documents for term: '{query_term}'\n")
    
    results = []  # (file_hash, uri, term_count, word_count, tf, idf, tfidf)
    
    # Get document frequency (count docs containing term)
    df = 0
    doc_info = {}
    
    for text_file in text_files:
        file_hash = text_file.stem
        occurrences = count_term_occurrences(text_file, query_term)
        
        if occurrences > 0:
            word_count = get_word_count(text_file)
            if word_count > 0:
                doc_info[file_hash] = (occurrences, word_count)
                df += 1
    
    print(f"Found in {df} documents\n")
    
    if df < 10:
        print(f"Error: Query term found in only {df} documents (need at least 10)")
        return None
    
    # Calculate IDF (using log base 2)
    idf = math.log2(corpus_size / df)
    
    # Calculate TF-IDF for each document
    for file_hash, (occurrences, word_count) in doc_info.items():
        tf = occurrences / word_count
        tfidf = tf * idf
        
        uri = uri_map.get(file_hash, "Unknown")
        domain = urlparse(uri).netloc
        
        results.append({
            'file_hash': file_hash,
            'uri': uri,
            'domain': domain,
            'occurrences': occurrences,
            'word_count': word_count,
            'tf': tf,
            'idf': idf,
            'tfidf': tfidf
        })
    
    # Sort by TF-IDF descending
    results.sort(key=lambda x: x['tfidf'], reverse=True)
    
    # Print results
    print(f"{'='*100}")
    print(f"TF-IDF Rankings for '{query_term}'")
    print(f"IDF = log2({corpus_size:,} / {df}) = {idf:.4f}")
    print(f"{'='*100}\n")
    
    print(f"{'TF-IDF':>10} {'TF':>10} {'Occurrences':>12} {'Words':>8} Domain{' ':>45} URI")
    print(f"{'-'*150}")
    
    for i, result in enumerate(results[:20], 1):
        print(f"{result['tfidf']:10.4f} {result['tf']:10.6f} {result['occurrences']:12} "
              f"{result['word_count']:8} {result['domain']:<50} {result['uri'][:30]}")
    
    # Save detailed results
    with open(f"tfidf_results_{query_term}.txt", 'w') as f:
        f.write(f"TF-IDF Rankings for '{query_term}'\n")
        f.write(f"Query Term: {query_term}\n")
        f.write(f"Document Frequency: {df}\n")
        f.write(f"IDF (log base 2): {idf:.6f}\n")
        f.write(f"Corpus Size: {corpus_size:,}\n")
        f.write(f"{'='*150}\n\n")
        
        f.write(f"{'Rank':>4} {'TF-IDF':>10} {'TF':>10} {'IDF':>10} {'Occurrences':>12} {'Words':>8} URI\n")
        f.write(f"{'-'*150}\n")
        
        for rank, result in enumerate(results[:50], 1):
            f.write(f"{rank:4} {result['tfidf']:10.6f} {result['tf']:10.8f} {result['idf']:10.6f} "
                   f"{result['occurrences']:12} {result['word_count']:8} {result['uri']}\n")
    
    print(f"\nDetailed results saved to: tfidf_results_{query_term}.txt")
    print(f"Total documents with term: {len(results)}")
    
    return results

if __name__ == "__main__":
    # Use "research" as the query term
    query_term = "research"
    results = compute_tfidf(query_term)
    
    if results and len(results) >= 10:
        # Get top 10 from different domains
        seen_domains = set()
        top_10 = []
        
        for result in results:
            if result['domain'] not in seen_domains:
                top_10.append(result)
                seen_domains.add(result['domain'])
                if len(top_10) == 10:
                    break
        
        # Save top 10 for Q3
        with open("top_10_query_results.txt", 'w') as f:
            f.write(f"Top 10 Results for '{query_term}' (from different domains)\n")
            f.write(f"{'='*100}\n\n")
            for i, result in enumerate(top_10, 1):
                f.write(f"{i}. {result['uri']}\n")
                f.write(f"   Domain: {result['domain']}\n")
                f.write(f"   TF-IDF: {result['tfidf']:.6f}\n\n")
        
        print(f"\nTop 10 results from different domains saved to: top_10_query_results.txt")
