#!/usr/bin/env python3
"""
Remove HTML boilerplate using boilerpy3
Process raw HTML files to extract main text content
"""

import os
import sys
from pathlib import Path
from boilerpy3.extractors import ArticleExtractor

def process_html_files(input_dir, output_dir, mapping_file):
    """Extract text from HTML files using boilerpy3"""
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    extractor = ArticleExtractor()
    
    html_files = list(input_path.glob("*.html"))
    total = len(html_files)
    
    print(f"Processing {total} HTML files...")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}\n")
    
    successful = 0
    failed = 0
    empty = 0
    
    # Load URI mapping if available
    uri_mapping = {}
    if Path(mapping_file).exists():
        with open(mapping_file, 'r') as f:
            for line in f:
                file_hash, uri = line.strip().split('\t', 1)
                uri_mapping[file_hash] = uri
    
    for i, html_file in enumerate(sorted(html_files), 1):
        try:
            file_hash = html_file.stem
            uri = uri_mapping.get(file_hash, "unknown")
            
            # Read HTML content
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Extract text
            try:
                extracted_text = extractor.get_text(html_content)
                
                if not extracted_text or len(extracted_text.strip()) == 0:
                    print(f"[{i}/{total}] EMPTY: {uri}")
                    empty += 1
                    continue
                
                # Save processed text
                output_file = output_path / f"{file_hash}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)
                
                print(f"[{i}/{total}] OK: {uri}")
                successful += 1
                
            except UnicodeDecodeError:
                print(f"[{i}/{total}] ENCODING ERROR: {uri}")
                failed += 1
            except Exception as e:
                print(f"[{i}/{total}] ERROR: {uri} - {str(e)[:50]}")
                failed += 1
        
        except Exception as e:
            print(f"[{i}/{total}] SKIP: {html_file.name} - {str(e)[:50]}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Processing complete!")
    print(f"Successful: {successful}/{total}")
    print(f"Empty files: {empty}/{total}")
    print(f"Failed: {failed}/{total}")
    print(f"Processed files saved to: {output_dir}")
    print(f"{'='*60}\n")
    
    return successful, empty, failed

if __name__ == "__main__":
    # Install boilerpy3 if needed
    try:
        import boilerpy3
    except ImportError:
        print("Installing boilerpy3...")
        os.system("pip install boilerpy3 -q")
    
    input_dir = "hw2_raw_html"
    output_dir = "hw2_processed_text"
    mapping_file = "uri_to_hash_mapping.txt"
    
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    if len(sys.argv) > 3:
        mapping_file = sys.argv[3]
    
    process_html_files(input_dir, output_dir, mapping_file)
