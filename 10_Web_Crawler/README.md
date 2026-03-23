# 10 - Advanced OSINT Web Crawler (Email Harvester)

An enterprise-grade, recursive web spider designed for the Open Source Intelligence (OSINT) and reconnaissance phases of penetration testing. 

## 🕸️ What is a Web Crawler?
A Web Crawler (also known as a Spider) is an automated script that systematically browses the internet.  
Instead of a human manually clicking on every link on a website to find information, the crawler downloads a webpage, extracts all the hyperlinks it contains, and then automatically visits those new links to repeat the process. This is the exact same underlying technology that search engines like Google use to index the web.

## 🛠️ What Does This Specific Program Do?
Our script is a targeted OSINT harvester. When provided with a starting URL (the "seed"), it performs the following tasks:
1. **HTML Scraping:** It downloads the raw source code of the webpage.
2. **Data Extraction:** It uses Regular Expressions (Regex) to hunt down and save any email address hidden in the text.
3. **Link Discovery:** It maps out all internal and external links found on the page.
4. **Recursive Crawling (Breadth-First Search):** Instead of stopping, it automatically navigates to the newly discovered *internal* links to scrape them as well. It repeats this process up to a user-defined depth (e.g., Depth 2 means it visits the homepage, the subpages, and the sub-subpages).
5. **Deduplication:** It uses Python `Sets` and `Threading Locks` to ensure it never visits the same page twice, preventing infinite loops.

## ⚠️ Educational Disclaimer & OPSEC
**This tool is strictly for ethical hacking and authorized audits.** Recursive crawling generates significant server load. A deep crawl (Depth > 3) on a large website with high thread counts can act as a Layer 7 Denial of Service (DoS) attack and will likely be flagged by Web Application Firewalls (WAF) like Cloudflare. Always ensure you have written permission.

## ✨ Technical Features
* **Thread-Safe Architecture:** Utilizes `concurrent.futures.ThreadPoolExecutor` with `threading.Lock()` to prevent memory corruption when multiple threads concurrently read and write to the shared datasets.
* **MIME Type Filtering:** Automatically ignores non-HTML assets (PDFs, images, ZIP files) to save bandwidth.
* **Resilient Requests:** Ignores SSL certificate errors (`verify=False`) common in staging environments, handles timeouts gracefully, and masks the script with a modern Chrome User-Agent.

## ⚙️ Prerequisites & Installation

1. **Initialize the environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 🛡️ Note on Repository Maintenance (.gitignore)
Ensure that generated recon files (e.g., `target_recon.txt`) are ignored in your `.gitignore` (`*.txt`, `*.csv`) so sensitive client data is not uploaded to public repositories.

## 📖 Help Menu
```bash
python osint_crawler.py --help
```

## 💻 Command Examples

**Shallow Crawl (Safe Recon):**
Crawl the homepage and its immediate subpages (Depth 1) using 5 threads:
```bash
python osint_crawler.py -u [https://quotes.toscrape.com/](https://quotes.toscrape.com/) -d 1 -t 5
```

**Deep Aggressive Extraction:**
Perform a deep crawl (Depth 3) using 20 threads and export the findings to a text file:
```bash
python osint_crawler.py -u [https://books.toscrape.com/](https://books.toscrape.com/) -d 3 -t 20 -o osint_report.txt
```

## 🔮 Future Perspectives (Roadmap)
To elevate this tool further, the following features are planned for future releases:
1. **Headless Browser Integration:** Replace the `requests` library with `Playwright` or `Selenium` to execute JavaScript, allowing the crawler to extract emails from modern Single Page Applications (React/Vue/Angular) that dynamically render content.
2. **Authentication Support:** Add the ability to pass session cookies or Bearer tokens via CLI flags to crawl authenticated areas of a web application (e.g., internal employee portals).
3. **Database Export:** Introduce a SQLite export module to securely store and query massive amounts of OSINT data collected across multi-day crawling sessions.
