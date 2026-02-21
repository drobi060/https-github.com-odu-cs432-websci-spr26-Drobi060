#!/usr/bin/env python3
"""
Download HTML content from 500 URIs collected in HW1
Create URI to hash mapping for file storage
"""

import requests
import hashlib
import time
import sys
from pathlib import Path

def uri_to_hash(uri):
    """Convert URI to MD5 hash"""
    return hashlib.md5(uri.strip().encode()).hexdigest()

def download_uris(uri_file, output_dir, mapping_file):
    """Download HTML from all URIs and create mapping"""
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    successful = 0
    failed = 0
    mapping = {}
    
    with open(uri_file, 'r') as f:
        uris = [line.strip() for line in f if line.strip()]
    
    total = len(uris)
    print(f"Starting download of {total} URIs...")
    print(f"Output directory: {output_dir}\n")
    
    for i, uri in enumerate(uris, 1):
        try:
            # Generate hash for filename
            file_hash = uri_to_hash(uri)
            output_file = output_path / f"{file_hash}.html"
            
            # Skip if already downloaded
            if output_file.exists():
                print(f"[{i}/{total}] SKIP (exists): {uri}")
                mapping[file_hash] = uri
                successful += 1
                continue
            
            # Download the page
            try:
                response = requests.get(uri, timeout=5)
                response.raise_for_status()
                
                # Save HTML content
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                mapping[file_hash] = uri
                print(f"[{i}/{total}] OK: {uri}")
                successful += 1
                
            except requests.Timeout:
                print(f"[{i}/{total}] TIMEOUT: {uri}")
                failed += 1
            except requests.RequestException as e:
                print(f"[{i}/{total}] ERROR: {uri} - {str(e)[:50]}")
                failed += 1
            
            # Be nice to servers
            time.sleep(0.1)
        
        except Exception as e:
            print(f"[{i}/{total}] SKIP: {uri} - {str(e)[:50]}")
            failed += 1
    
    # Save mapping file
    with open(mapping_file, 'w') as f:
        for file_hash, uri in sorted(mapping.items()):
            f.write(f"{file_hash}\t{uri}\n")
    
    print(f"\n{'='*60}")
    print(f"Download complete!")
    print(f"Successful: {successful}/{total}")
    print(f"Failed: {failed}/{total}")
    print(f"Mapping saved to: {mapping_file}")
    print(f"HTML files saved to: {output_dir}")
    print(f"{'='*60}\n")
    
    return successful, failed

if __name__ == "__main__":
    uri_file = "collected_uris.txt"
    output_dir = "hw2_raw_html"
    mapping_file = "uri_to_hash_mapping.txt"
    
    if len(sys.argv) > 1:
        uri_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    if len(sys.argv) > 3:
        mapping_file = sys.argv[3]
    
    download_uris(uri_file, output_dir, mapping_file)
