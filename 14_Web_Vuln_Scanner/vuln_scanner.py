import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import sys

# Dictionaries of common database error messages to detect SQLi
SQL_ERRORS = {
    "MySQL": ["you have an error in your sql syntax", "warning: mysql", "unclosed quotation mark"],
    "PostgreSQL": ["pg_query() [", "syntax error at or near", "unterminated quoted string"],
    "MSSQL": ["microsoft odbc sql server driver", "unclosed quotation mark"],
    "Oracle": ["ora-00933: sql command not properly ended", "quoted string not properly terminated"]
}

# Advanced Payloads
SQLI_PAYLOADS = ["'", "\"", "' OR 1=1--", "' OR '1'='1"]
XSS_PAYLOAD = "<script>alert('VULN_XSS_DETECTED')</script>"
CMD_PAYLOADS = ["; echo VULN_OS_CMD", "| echo VULN_OS_CMD", "`echo VULN_OS_CMD`"]
CRLF_PAYLOADS = ["%0d%0aSet-Cookie:crlf_test=1", "\r\nSet-Cookie:crlf_test=1"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) (Ethical Security Scanner)"
}

def inject_payload(url: str, payload: str) -> list:
    """Injects a payload into every parameter of the URL, one by one."""
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    injected_urls = []

    if not params:
        return injected_urls

    for param_name in params.keys():
        manipulated_params = params.copy()
        manipulated_params[param_name] = [manipulated_params[param_name][0] + payload]
        new_query = urlencode(manipulated_params, doseq=True)
        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))
        injected_urls.append((new_url, param_name))

    return injected_urls

def test_sqli(url: str) -> bool:
    """Tests for SQL Injection by analyzing database error reflections."""
    print("\n[*] Initializing SQL Injection (SQLi) Module...")
    for payload in SQLI_PAYLOADS:
        for target_url, param in inject_payload(url, payload):
            try:
                response = requests.get(target_url, headers=HEADERS, timeout=5)
                content = response.text.lower()

                for db_type, errors in SQL_ERRORS.items():
                    for error in errors:
                        if error in content:
                            print(f" ╰──> 🚨 CRITICAL: SQLi Detected!")
                            print(f"      Parameter: '{param}' | Payload: {payload}")
                            print(f"      DB Type  : {db_type} (guessed)")
                            return True
            except requests.exceptions.RequestException:
                pass
    print(" [+] CLEAN: No SQLi vulnerabilities detected (Error-based).")
    return False

def test_xss(url: str) -> bool:
    """Tests for Reflected Cross-Site Scripting (XSS)."""
    print("\n[*] Initializing Reflected XSS Module...")
    for target_url, param in inject_payload(url, XSS_PAYLOAD):
        try:
            response = requests.get(target_url, headers=HEADERS, timeout=5)
            content = response.text
            
            if XSS_PAYLOAD in content:
                soup = BeautifulSoup(content, 'html.parser')
                if soup.find('script', string=lambda text: text and 'VULN_XSS_DETECTED' in text) or XSS_PAYLOAD in content:
                    print(f" ╰──> 🚨 HIGH: Reflected XSS Detected!")
                    print(f"      Parameter: '{param}' | Payload: {XSS_PAYLOAD}")
                    return True
        except requests.exceptions.RequestException:
            pass
    print(" [+] CLEAN: No Reflected XSS vulnerabilities detected.")
    return False

def test_os_cmd(url: str) -> bool:
    """Tests for OS Command Injection."""
    print("\n[*] Initializing OS Command Injection Module...")
    for payload in CMD_PAYLOADS:
        for target_url, param in inject_payload(url, payload):
            try:
                response = requests.get(target_url, headers=HEADERS, timeout=5)
                # If the server executed 'echo VULN_OS_CMD', the string will be in the output
                if "VULN_OS_CMD" in response.text and "echo" not in response.text:
                    print(f" ╰──> 🚨 CRITICAL: OS Command Injection Detected!")
                    print(f"      Parameter: '{param}' | Payload: {payload}")
                    return True
            except requests.exceptions.RequestException:
                pass
    print(" [+] CLEAN: No OS Command Injection detected.")
    return False

def test_crlf(url: str) -> bool:
    """Tests for CRLF Injection / HTTP Response Splitting."""
    print("\n[*] Initializing CRLF Injection Module...")
    for payload in CRLF_PAYLOADS:
        for target_url, param in inject_payload(url, payload):
            try:
                # We use allow_redirects=False to catch injected headers before the browser redirects
                response = requests.get(target_url, headers=HEADERS, timeout=5, allow_redirects=False)
                
                # Check if our injected cookie actually made it into the HTTP Headers
                if 'crlf_test' in response.cookies or any('crlf_test' in str(v) for v in response.headers.values()):
                    print(f" ╰──> 🚨 MEDIUM: CRLF Injection (HTTP Splitting) Detected!")
                    print(f"      Parameter: '{param}' | Payload: {payload}")
                    return True
            except requests.exceptions.RequestException:
                pass
    print(" [+] CLEAN: No CRLF Injection detected.")
    return False

def check_csrf(url: str) -> bool:
    """Passively analyzes the page for forms missing Anti-CSRF tokens."""
    print("\n[*] Initializing CSRF Misconfiguration Module (Passive)...")
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        
        if not forms:
            print(" [+] CLEAN: No HTML forms found on this page to exploit.")
            return False

        vulnerable_forms = 0
        csrf_keywords = ['csrf', 'token', 'xsrf', 'authenticity_token']

        for i, form in enumerate(forms, 1):
            has_token = False
            # Look for hidden input fields that might be CSRF tokens
            inputs = form.find_all('input', type='hidden')
            for inp in inputs:
                name = inp.get('name', '').lower()
                if any(keyword in name for keyword in csrf_keywords):
                    has_token = True
                    break
            
            if not has_token:
                vulnerable_forms += 1
                action = form.get('action', 'Self (Current URL)')
                print(f" ╰──> ⚠️ WARNING: Form #{i} (Action: {action}) is missing an Anti-CSRF token!")

        if vulnerable_forms > 0:
            return True
        else:
            print(" [+] CLEAN: All forms appear to have hidden security tokens.")
            return False
            
    except requests.exceptions.RequestException:
        print(" [-] Error: Could not fetch page to check for CSRF.")
        return False

def main():
    parser = argparse.ArgumentParser(description="Advanced Web Vulnerability Scanner (SQLi, XSS, CMD, CRLF, CSRF)")
    parser.add_argument("-u", "--url", required=True, help="Target URL with parameters (e.g., http://site.com/page?id=1)")
    
    args = parser.parse_args()

    if '?' not in args.url:
        print("[-] Error: The target URL must contain at least one parameter to test (e.g., ?id=1 or ?search=test)")
        sys.exit(1)

    print("="*75)
    print("🕷️  Advanced Web Vulnerability Scanner (Mini-DAST)")
    print("="*75)
    print(f"[*] Target : {args.url}")

    # Run the active testing modules
    sqli_found = test_sqli(args.url)
    xss_found = test_xss(args.url)
    cmd_found = test_os_cmd(args.url)
    crlf_found = test_crlf(args.url)
    
    # Run the passive testing module
    csrf_found = check_csrf(args.url)

    print("\n" + "="*75)
    print("📋 SCAN SUMMARY:")
    
    findings = any([sqli_found, xss_found, cmd_found, crlf_found, csrf_found])
    
    if findings:
        print("[!] Target is VULNERABLE to one or more attacks. Check the logs above.")
    else:
        print("[+] Target appears secure against these specific vulnerabilities.")
    print("="*75)

if __name__ == "__main__":
    main()
