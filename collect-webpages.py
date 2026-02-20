#!/usr/bin/env python3
"""
Collect URIs of webpages with more than 1000 bytes

Usage: python3 collect-webpages.py <seed_uri> [target_count]
"""

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random

def extract_links(url, html_content, max_links=50):
    """Extract all links from HTML content"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        for link in soup.find_all('a', href=True):
            if len(links) >= max_links:
                break
            href = link['href']
            # Convert relative URLs to absolute
            absolute_url = urljoin(url, href)
            # Remove fragments
            absolute_url = absolute_url.split('#')[0]
            if absolute_url.startswith(('http://', 'https://')):
                links.append(absolute_url)
        return links
    except:
        return []

def is_valid_html(url, timeout=3):
    """Check if URL is HTML and > 1000 bytes"""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        content_type = response.headers.get('content-type', '').lower()
        
        if 'text/html' not in content_type:
            return False, None
        
        content_length = response.headers.get('content-length')
        if content_length:
            size = int(content_length)
        else:
            size = 0
        
        if size > 1000:
            return True, response.url
        return False, None
    except:
        return False, None

def collect_webpages(seed_uri, target_count=500):
    """Collect webpages using random walk"""
    collected = set()
    visited = set()
    to_visit = [seed_uri]
    
    print(f"Starting collection with seed: {seed_uri}")
    print(f"Target: {target_count} unique URIs\n")
    
    while len(collected) < target_count and (to_visit or collected):
        # Pick next URL to visit
        if random.random() < 0.4 and collected:
            current_url = random.choice(list(collected))
        elif to_visit:
            current_url = to_visit.pop(0)
        elif collected:
            current_url = random.choice(list(collected))
        else:
            break
        
        if current_url in visited:
            continue
        
        visited.add(current_url)
        
        try:
            # Fetch the page
            response = requests.get(current_url, timeout=3)
            links = extract_links(response.url, response.content)
            
            # Check each link
            for link in links:
                if len(collected) >= target_count:
                    break
                
                if link not in visited and link not in collected:
                    is_valid, final_url = is_valid_html(link)
                    if is_valid:
                        collected.add(final_url)
                        print(final_url)
                        
                        # Add to visit queue
                        if final_url not in visited and len(to_visit) < 100:
                            to_visit.append(final_url)
            
            # Show progress
            remaining = target_count - len(collected)
            if remaining > 0 and len(collected) % 50 == 0:
                print(f"Need to collect {remaining} more URIs...")
                if collected:
                    next_seed = random.choice(list(collected))
                    print(f" random seed: {next_seed}\n")
        
        except Exception as e:
            continue
    
    return collected

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 collect-webpages.py <seed_uri> [target_count]")
        sys.exit(1)
    
    seed_uri = sys.argv[1]
    target_count = 500
    
    if len(sys.argv) > 2:
        try:
            target_count = int(sys.argv[2])
        except ValueError:
            print("Invalid target count")
            sys.exit(1)
    
    # Install beautifulsoup4 if needed
    try:
        import bs4
    except ImportError:
        print("Installing beautifulsoup4...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4", "-q"])
    
    collected = collect_webpages(seed_uri, target_count)
    
    print(f"\nCollected {len(collected)} unique URIs")
    
    # Save to file
    output_file = 'collected_uris.txt'
    with open(output_file, 'w') as f:
        for uri in sorted(collected):
            f.write(uri + '\n')
    
    print(f"URIs saved to {output_file}")

if __name__ == "__main__":
    main()
