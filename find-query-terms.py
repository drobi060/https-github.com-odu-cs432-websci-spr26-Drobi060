#!/usr/bin/env python3
"""
Find suitable query terms that appear in multiple documents
"""

import os
import re
from pathlib import Path
from collections import Counter
import string

# Common stop words
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do',
    'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
    'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
    'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every',
    'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
    'same', 'so', 'than', 'too', 'very', 'just', 'as', 'if', 'then', 'because',
    'http', 'https', 'www', 'com', 'org', 'edu', 'net', 'html', 'css', 'js',
    'br', 'p', 'div', 'span', 'class', 'id', 'style', 'src', 'href', 'alt', 'title'
}

def find_query_terms(processed_dir="processed_text", min_docs=10):
    """Find words that appear in at least min_docs documents"""
    
    # Get all processed files
    text_files = list(Path(processed_dir).glob("*.txt"))
    print(f"Found {len(text_files)} processed text files\n")
    
    # Count documents containing each word
    word_docs = Counter()
    file_word_count = {}
    
    for i, text_file in enumerate(sorted(text_files)):
        if i % 100 == 0:
            print(f"Processing file {i}/{len(text_files)}")
        
        try:
            with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
            
            # Simple tokenization
            words = re.findall(r'\b[a-z]+\b', content)
            unique_words = set(words)
            
            for word in unique_words:
                if word not in STOP_WORDS and len(word) > 3:
                    word_docs[word] += 1
            
            file_word_count[text_file.name] = len(words)
        
        except Exception as e:
            print(f"Error reading {text_file.name}: {e}")
    
    # Filter words that appear in at least min_docs documents
    query_candidates = [(word, count) for word, count in word_docs.most_common(1000) 
                        if count >= min_docs]
    
    print(f"\n{'='*60}")
    print(f"Words appearing in at least {min_docs} documents:")
    print(f"{'='*60}")
    
    for word, count in query_candidates[:30]:
        print(f"{word:20} {count:4} documents")
    
    print(f"\nTotal candidates: {len(query_candidates)}")
    
    # Save to file
    with open("query_candidates.txt", 'w') as f:
        for word, count in query_candidates:
            f.write(f"{word}\t{count}\n")
    
    print("\nTop candidates saved to query_candidates.txt")
    return query_candidates

if __name__ == "__main__":
    find_query_terms()
