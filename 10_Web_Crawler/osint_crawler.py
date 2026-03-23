import argparse
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse, urldefrag
import concurrent.futures
import threading
import sys
import time

# Robust Regex for emails
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

# Headers to bypass basic anti-bot protections
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

class AdvancedCrawler:
    def __init__(self, base_url, max_depth, max_threads):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.max_depth = max_depth
        self.max_threads = max_threads
        
        # Shared resources among threads
        self.visited_urls = set()
        self.found_emails = set()
        self.external_links = set()
        
        # Thread locks to prevent race conditions when modifying sets
        self.lock = threading.Lock()

    def is_valid_internal_url(self, url):
        """Checks if the URL belongs to the target domain and is a valid web page."""
        parsed = urlparse(url)
        # Avoid crawling media files or documents
        ignored_extensions = ('.pdf', '.jpg', '.jpeg', '.png', '.gif', '.css', '.js', '.zip', '.tar.gz', '.mp4')
        if parsed.path.lower().endswith(ignored_extensions):
            return False
        return parsed.netloc == self.base_domain and parsed.scheme in ['http', 'https']

    def crawl_page(self, url, current_depth):
        """Fetches a single page, extracts emails, and finds new links."""
        if current_depth > self.max_depth:
            return []

        # Thread-safe check and add
        with self.lock:
            if url in self.visited_urls:
                return []
            self.visited_urls.add(url)

        try:
            # stream=False but we use timeout to prevent hanging on bad servers
            response = requests.get(url, headers=HEADERS, timeout=7, verify=False)
            
            # Only process HTML pages
            if 'text/html' not in response.headers.get('Content-Type', ''):
                return []
                
            response.raise_for_status()
            html = response.text
        except requests.exceptions.RequestException:
            return []

        # 1. Extract Emails safely
        emails = set(EMAIL_REGEX.findall(html))
        with self.lock:
            self.found_emails.update(emails)

        # 2. Extract Links
        soup = BeautifulSoup(html, 'html.parser')
        new_internal_links = set()

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            
            # Ignore mailto, tel, javascript
            if href.startswith(('mailto:', 'tel:', 'javascript:', '#')):
                continue

            # Build full URL and remove fragments (e.g., #section1)
            full_url = urljoin(url, href)
            full_url, _ = urldefrag(full_url)
            parsed_url = urlparse(full_url)

            if parsed_url.scheme not in ['http', 'https']:
                continue

            if parsed_url.netloc == self.base_domain:
                if self.is_valid_internal_url(full_url):
                    with self.lock:
                        if full_url not in self.visited_urls:
                            new_internal_links.add(full_url)
            else:
                with self.lock:
                    self.external_links.add(full_url)

        return list(new_internal_links)

    def run(self):
        """Manages the multithreaded breadth-first search (BFS) crawling."""
        print(f"[*] Starting Advanced Crawl on: {self.base_url}")
        print(f"[*] Max Depth: {self.max_depth} | Threads: {self.max_threads}\n")
        
        # Suppress insecure request warnings if target has bad SSL
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Queue of tuples: (url, depth)
        urls_to_crawl = [(self.base_url, 0)]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            while urls_to_crawl:
                # Submit current level of URLs to threads
                future_to_url = {
                    executor.submit(self.crawl_page, url, depth): (url, depth) 
                    for url, depth in urls_to_crawl
                }
                
                urls_to_crawl = [] # Reset for the next depth level
                
                for future in concurrent.futures.as_completed(future_to_url):
                    url, depth = future_to_url[future]
                    try:
                        new_links = future.result()
                        # Add newly discovered links to the queue with incremented depth
                        for link in new_links:
                            urls_to_crawl.append((link, depth + 1))
                    except Exception as e:
                        pass # Silently handle thread crashes to keep crawler alive

        print("\n[+] Crawl Completed!")

def main():
    parser = argparse.ArgumentParser(description="Advanced OSINT Web Crawler (Email & Link Harvester)")
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., https://example.com)")
    parser.add_argument("-d", "--depth", type=int, default=2, help="Crawl depth (Default: 2)")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of concurrent threads (Default: 10)")
    parser.add_argument("-o", "--output", help="Save results to a text file")

    args = parser.parse_args()

    if not args.url.startswith(('http://', 'https://')):
        print("[-] Error: URL must start with http:// or https://")
        sys.exit(1)

    print("="*65)
    print("🕸️  Advanced OSINT Web Crawler")
    print("="*65)

    start_time = time.time()
    
    crawler = AdvancedCrawler(args.url, args.depth, args.threads)
    crawler.run()

    elapsed = round(time.time() - start_time, 2)

    print("="*65)
    print(f"[*] Time elapsed    : {elapsed} seconds")
    print(f"[*] Pages crawled   : {len(crawler.visited_urls)}")
    print(f"[*] Emails found    : {len(crawler.found_emails)}")
    print(f"[*] External links  : {len(crawler.external_links)}")
    print("="*65)

    if crawler.found_emails:
        print("\n[+] Extracted Emails:")
        for email in sorted(crawler.found_emails):
            print(f" ╰──> {email}")

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(f"OSINT Reconnaissance Report for: {args.url}\n")
                f.write(f"Pages crawled: {len(crawler.visited_urls)}\n")
                f.write("="*50 + "\n\n")
                
                f.write("EMAILS FOUND:\n" + "-"*20 + "\n")
                for e in sorted(crawler.found_emails): f.write(f"{e}\n")
                
                f.write("\nEXTERNAL LINKS DISCOVERED:\n" + "-"*20 + "\n")
                for ex in sorted(crawler.external_links): f.write(f"{ex}\n")
                
            print(f"\n[+] Full report successfully saved to '{args.output}'")
        except Exception as e:
            print(f"[-] Error saving report: {e}")

if __name__ == "__main__":
    main()
