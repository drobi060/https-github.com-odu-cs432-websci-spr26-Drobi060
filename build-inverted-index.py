#!/usr/bin/env python3
"""
Q5: Build inverted index for all words from 500 processed documents
Simple ASCII format with word -> document list mapping
"""

import re
from pathlib import Path
from collections import defaultdict

def build_inverted_index(processed_dir="processed_text"):
    """Build inverted index from all processed documents"""
    
    text_files = sorted(Path(processed_dir).glob("*.txt"))
    print(f"Building inverted index from {len(text_files)} documents...\n")
    
    inverted_index = defaultdict(set)  # word -> set of file hashes
    
    # Read URI mapping
    uri_map = {}
    with open("uri_mapping.txt", 'r') as f:
        for line in f:
            parts = line.strip().split('\t', 1)
            if len(parts) == 2:
                uri_map[parts[0]] = parts[1]
    
    # Process each document
    for i, text_file in enumerate(text_files, 1):
        file_hash = text_file.stem
        
        try:
            with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
            
            # Tokenize: extract words (alphanumeric + hyphen)
            words = re.findall(r'\b[a-z0-9]+(?:-[a-z0-9]+)*\b', content)
            
            # Add to inverted index
            for word in set(words):  # Use set to avoid duplicates
                inverted_index[word].add(file_hash)
        
        except Exception as e:
            print(f"Error processing {file_hash}: {e}")
        
        if i % 100 == 0:
            print(f"  Processed {i}/{len(text_files)} documents...")
    
    print(f"\nInverted index built!")
    print(f"Total unique words: {len(inverted_index)}")
    print(f"Average docs per word: {sum(len(docs) for docs in inverted_index.values()) / len(inverted_index):.2f}")
    
    return inverted_index, uri_map

def save_inverted_index(inverted_index, uri_map, output_file="inverted_index.txt"):
    """Save inverted index to ASCII file"""
    
    print(f"\nSaving inverted index to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("INVERTED INDEX FOR 500 DOCUMENTS\n")
        f.write("="*100 + "\n")
        f.write(f"Format: word\tdocument_count\tdocument_hashes\n")
        f.write("="*100 + "\n\n")
        
        # Sort words alphabetically
        sorted_words = sorted(inverted_index.keys())
        
        for word in sorted_words:
            doc_hashes = sorted(inverted_index[word])
            doc_count = len(doc_hashes)
            
            # Format: word<tab>count<tab>hash1,hash2,hash3,...
            line = f"{word}\t{doc_count}\t"
            line += ",".join(doc_hashes)
            f.write(line + "\n")
    
    print(f"Inverted index saved!")
    print(f"File size: {Path(output_file).stat().st_size / (1024*1024):.2f} MB")
    
    return output_file

def analyze_inverted_index(inverted_index, uri_map):
    """Analyze and display interesting statistics"""
    
    print("\n" + "="*100)
    print("INVERTED INDEX ANALYSIS")
    print("="*100)
    
    # Find most common words
    word_frequencies = [(word, len(docs)) for word, docs in inverted_index.items()]
    word_frequencies.sort(key=lambda x: x[1], reverse=True)
    
    print("\nTop 50 Most Common Words (by document count):")
    print("-"*100)
    print(f"{'Rank':<6} {'Word':<20} {'Doc Count':<12} {'Frequency':<12}")
    print("-"*100)
    
    for rank, (word, count) in enumerate(word_frequencies[:50], 1):
        frequency = count / len(uri_map) * 100
        print(f"{rank:<6} {word:<20} {count:<12} {frequency:.2f}%")
    
    # Find rare words (appear in only 1 document)
    rare_words = [word for word, docs in inverted_index.items() if len(docs) == 1]
    
    print(f"\n\nRare Words (appearing in exactly 1 document): {len(rare_words)}")
    print(f"Percentage of vocabulary: {len(rare_words)/len(inverted_index)*100:.2f}%")
    
    # Find words appearing in all/most documents
    all_doc_words = [word for word, docs in inverted_index.items() if len(docs) == len(uri_map)]
    most_doc_words = [word for word, docs in inverted_index.items() if len(docs) >= len(uri_map) * 0.9]
    
    print(f"\n\nWords appearing in ALL documents: {len(all_doc_words)}")
    print(f"Words appearing in >=90% of documents: {len(most_doc_words)}")
    
    # Interesting domain-specific words
    print(f"\n\nDomain-Specific Words (high frequency in academic context):")
    domain_words = ['research', 'university', 'students', 'program', 'academic', 'education',
                    'faculty', 'courses', 'degrees', 'graduate', 'undergraduate', 'learning']
    
    for word in domain_words:
        if word in inverted_index:
            count = len(inverted_index[word])
            frequency = count / len(uri_map) * 100
            print(f"  {word:<20} appears in {count:>3} docs ({frequency:>5.1f}%)")

if __name__ == "__main__":
    # Build index
    inverted_index, uri_map = build_inverted_index()
    
    # Save to file
    output_file = save_inverted_index(inverted_index, uri_map)
    
    # Analyze
    analyze_inverted_index(inverted_index, uri_map)
    
    print("\n" + "="*100)
    print("Q5 COMPLETE: Inverted index built and saved")
    print("="*100)
