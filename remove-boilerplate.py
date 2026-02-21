#!/usr/bin/env python3
"""
Remove HTML boilerplate from downloaded HTML files using boilerpy3
"""

import os
import sys
from pathlib import Path

try:
    from boilerpy3.extractors import ArticleExtractor
except ImportError:
    print("Installing boilerpy3...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "boilerpy3", "-q"])
    from boilerpy3.extractors import ArticleExtractor

def remove_boilerplate(input_dir="raw_html", output_dir="processed_text"):
    """Extract text content from HTML files"""
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Get all HTML files
    html_files = list(Path(input_dir).glob("*.html"))
    print(f"Found {len(html_files)} HTML files to process")
    
    successful = 0
    failed = 0
    empty = 0
    
    for i, html_file in enumerate(sorted(html_files), 1):
        output_file = Path(output_dir) / (html_file.stem + ".txt")
        
        try:
            # Read HTML
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()
            
            # Extract text
            extractor = ArticleExtractor()
            content = extractor.get_content(html_content)
            
            # Check if content is empty
            if not content or len(content.strip()) == 0:
                empty += 1
                print(f"[{i}/{len(html_files)}] Empty: {html_file.name}")
                continue
            
            # Save processed text
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            successful += 1
            if i % 50 == 0:
                print(f"[{i}/{len(html_files)}] Processed: {html_file.name}")
        
        except Exception as e:
            failed += 1
            if i % 50 == 0:
                print(f"[{i}/{len(html_files)}] Error in {html_file.name}: {str(e)[:50]}")
    
    print(f"\n{'='*60}")
    print(f"Processing complete!")
    print(f"Successful: {successful}")
    print(f"Empty results: {empty}")
    print(f"Failed: {failed}")
    print(f"Total: {len(html_files)}")
    print(f"Output saved to: {output_dir}/")
    print(f"{'='*60}")
    
    return successful

if __name__ == "__main__":
    if not os.path.exists("raw_html"):
        print("Error: raw_html directory not found")
        print("Please run download-webpages.py first")
        sys.exit(1)
    
    remove_boilerplate()
