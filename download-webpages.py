#!/usr/bin/env python3
"""
Download HTML content from 500 URIs collected in HW1
Creates URI-to-hash mapping and saves raw HTML files
"""

import sys
import os
import requests
import hashlib
import time
from pathlib import Path

def get_md5_hash(uri):
    """Compute MD5 hash of URI"""
    return hashlib.md5(uri.strip().encode()).hexdigest()

def download_uris(uri_file, output_dir="raw_html", mapping_file="uri_mapping.txt"):
    """Download HTML from all URIs"""
    
    # Create output directories
    Path(output_dir).mkdir(exist_ok=True)
    
    # Read URIs
    with open(uri_file, 'r') as f:
        uris = [line.strip() for line in f if line.strip()]
    
    print(f"Found {len(uris)} URIs to download")
    
    successful = 0
    failed = 0
    mapping = []
    
    for i, uri in enumerate(uris, 1):
        uri_hash = get_md5_hash(uri)
        output_file = os.path.join(output_dir, f"{uri_hash}.html")
        
        # Skip if already downloaded
        if os.path.exists(output_file):
            print(f"[{i}/{len(uris)}] Skipping (exists): {uri_hash}")
            mapping.append(f"{uri_hash}\t{uri}")
            successful += 1
            continue
        
        try:
            print(f"[{i}/{len(uris)}] Downloading: {uri}")
            response = requests.get(uri, timeout=5)
            response.raise_for_status()
            
            # Save HTML
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            mapping.append(f"{uri_hash}\t{uri}")
            successful += 1
            print(f"  ✓ Saved to {uri_hash}.html")
            
        except requests.exceptions.Timeout:
            failed += 1
            print(f"  ✗ Timeout: {uri}")
        except requests.exceptions.ConnectionError:
            failed += 1
            print(f"  ✗ Connection error: {uri}")
        except Exception as e:
            failed += 1
            print(f"  ✗ Error: {str(e)[:50]}")
        
        # Rate limiting
        if i % 10 == 0:
            time.sleep(1)
    
    # Save mapping
    with open(mapping_file, 'w') as f:
        for entry in mapping:
            f.write(entry + '\n')
    
    print(f"\n{'='*60}")
    print(f"Download complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {len(uris)}")
    print(f"Mapping saved to: {mapping_file}")
    print(f"HTML files saved to: {output_dir}/")
    print(f"{'='*60}")

if __name__ == "__main__":
    uri_file = "collected_uris.txt"
    
    if not os.path.exists(uri_file):
        print(f"Error: {uri_file} not found")
        print("Please run this from the directory containing collected_uris.txt from HW1")
        sys.exit(1)
    
    download_uris(uri_file)
