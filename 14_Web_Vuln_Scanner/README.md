# 14 - Advanced Web Vulnerability Scanner (Mini-DAST)

An automated Dynamic Application Security Testing (DAST) tool designed to identify critical web vulnerabilities from the OWASP Top 10. This scanner actively fuzzes URL parameters and passively analyzes HTML structures to detect five major classes of vulnerabilities: SQLi, XSS, OS Command Injection, CRLF Injection, and CSRF misconfigurations.

## 🛡️ How Does it "Understand" Vulnerabilities?
Unlike naive scanners that blindly send requests, this tool parses the URL parameters, logically injects payloads, and actively analyzes the HTTP response using the DOM and Heuristics:

* **SQL Injection (SQLi):** Injects characters (like `'`) to break database queries and scans the HTML response for specific database driver error messages (MySQL, MSSQL, PostgreSQL, Oracle).
* **Cross-Site Scripting (XSS):** Injects a `<script>` payload and parses the returning HTML using `BeautifulSoup` to verify if the server reflected the payload *unescaped* into the DOM.
* **OS Command Injection:** Injects system commands (e.g., `; echo VULN_OS_CMD`) into parameters. If the server executes it on its underlying Linux/Windows operating system, the injected string will be reflected in the HTTP response.
* **CRLF Injection (HTTP Splitting):** Injects Carriage Return / Line Feed characters (`%0d%0a`) into the URL to force the server to start a new HTTP Header. If the script detects its custom fake Cookie in the server's response headers, the attack is successful.
* **Cross-Site Request Forgery (CSRF):** Acts *passively*. It reads the HTML of the page, locates all `<form>` tags, and checks if the developer forgot to include a hidden, randomized Anti-CSRF token (like `<input type="hidden" name="csrf_token">`). If missing, an attacker could force a victim to submit that form unknowingly.

## ⚠️ Educational Disclaimer & OPSEC
**This is an active exploitation tool.** Injecting payloads into a server can cause application errors, corrupt data, or trigger severe alerts on a Web Application Firewall (WAF). **Never run this tool against a domain you do not own or do not have explicit, written authorization to test.**

## ⚙️ Prerequisites & Installation

1. **Initialize the environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 🛡️ Note on Repository Maintenance (.gitignore)
A `.gitignore` file is included to prevent the upload of generated vulnerability reports (`*.txt`, `*.json`) to your public GitHub repository.

## 📖 Help Menu
```bash
python vuln_scanner.py --help
```

## 💻 Command Examples

**Testing an Educational Vulnerable Target:**
Use legally permitted training environments like Altoro Mutual site by IBM AppScan  to see the scanner in action. Provide a URL that contains a parameter (e.g., `?cat=1`).
```bash
python vuln_scanner.py -u "http://demo.testfire.net/search.jsp?query=test"
```

## 🔮 Future Perspectives (Roadmap)
To elevate this tool further, the following features are planned:
1. **Blind SQL Injection:** Implement Time-Based SQLi payloads (e.g., `WAITFOR DELAY '0:0:5'`). If the server takes exactly 5 seconds longer to respond, the tool mathematically proves a vulnerability exists even if no error text is returned.
2. **Form Extraction (POST requests):** Add a module that automatically extracts CSRF tokens and injects payloads via HTTP POST instead of just URL GET parameters.
3. **Burp Suite / Proxy Integration:** Allow routing the scanner's traffic through a local proxy (like `http://127.0.0.1:8080`) to capture the exact requests and responses for manual verification by a pentester.
