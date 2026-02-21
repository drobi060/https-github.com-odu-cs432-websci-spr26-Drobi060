#!/usr/bin/env python3
"""
Faster parallel download of remaining URIs using threading
"""

import os
import sys
import requests
import hashlib
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

def get_md5_hash(uri):
    """Compute MD5 hash of URI"""
    return hashlib.md5(uri.strip().encode()).hexdigest()

def download_single(uri, output_dir, lock):
    """Download a single URI"""
    uri_hash = get_md5_hash(uri)
    output_file = os.path.join(output_dir, f"{uri_hash}.html")
    
    # Skip if already downloaded
    if os.path.exists(output_file):
        return uri_hash, uri, "skipped", None
    
    try:
        response = requests.get(uri, timeout=5)
        response.raise_for_status()
        
        with lock:
            # Double-check before writing
            if not os.path.exists(output_file):
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
        
        return uri_hash, uri, "success", None
    except Exception as e:
        return uri_hash, uri, "failed", str(e)[:50]

def download_uris_parallel(uri_file, output_dir="raw_html", mapping_file="uri_mapping.txt", num_workers=8):
    """Download HTML from all URIs using parallel workers"""
    
    Path(output_dir).mkdir(exist_ok=True)
    
    # Read URIs
    with open(uri_file, 'r') as f:
        uris = [line.strip() for line in f if line.strip()]
    
    print(f"Found {len(uris)} URIs to download")
    
    lock = threading.Lock()
    results = defaultdict(list)
    mapping = []
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(download_single, uri, output_dir, lock): uri 
                   for uri in uris}
        
        completed = 0
        for future in as_completed(futures):
            completed += 1
            uri_hash, uri, status, error = future.result()
            
            if status == "success":
                mapping.append(f"{uri_hash}\t{uri}")
                if completed % 50 == 0:
                    print(f"[{completed}/{len(uris)}] Downloaded: {uri_hash[:8]}...")
            elif status == "skipped":
                mapping.append(f"{uri_hash}\t{uri}")
            else:
                print(f"[{completed}/{len(uris)}] Failed {uri_hash[:8]}...: {error}")
            
            results[status].append(uri)
    
    # Save mapping
    with open(mapping_file, 'w') as f:
        for entry in mapping:
            f.write(entry + '\n')
    
    print(f"\n{'='*60}")
    print(f"Download complete!")
    print(f"Successful: {len(results['success'])}")
    print(f"Skipped: {len(results['skipped'])}")
    print(f"Failed: {len(results['failed'])}")
    print(f"Total: {len(uris)}")
    print(f"Mapping saved to: {mapping_file}")
    print(f"HTML files saved to: {output_dir}/")
    print(f"{'='*60}")

if __name__ == "__main__":
    uri_file = "collected_uris.txt"
    
    if not os.path.exists(uri_file):
        print(f"Error: {uri_file} not found")
        sys.exit(1)
    
    download_uris_parallel(uri_file, num_workers=10)
