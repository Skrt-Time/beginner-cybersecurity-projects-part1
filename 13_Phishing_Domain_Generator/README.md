# 13 - Advanced Phishing Domain Generator & Verifier

A dual-purpose Cyber Threat Intelligence (CTI) utility. It serves both offensively to generate deceptive variations of a target domain name (Typosquatting/Homoglyphs) and defensively as an algorithmic Domain Verifier to protect end-users from sophisticated phishing attacks.

## 🛡️ Dual Modes of Operation

### 1. The Generator Mode (Red Team / CTI)
Predicts which fake domains an attacker might buy to target your company.
* **Massive Homoglyph Engine:** Swaps specific characters with their visual twins (e.g., `m` to `rn`).
* **Keyboard Proximity (QWERTY):** Simulates "fat-finger" typing errors.
* **Active DNS Resolution:** Queries internet DNS servers to instantly flag any generated domain that is already registered by threat actors.

### 2. The Verifier Mode (Blue Team / Defensive)
Takes an unknown, suspicious URL provided by a user (e.g., `rnicrosoft.com` or `paypa1.com`) and acts as an intelligent shield.
* **Algorithmic String Similarity:** Calculates the mathematical edit distance (using Python's `difflib` Gestalt Pattern Matching, functionally similar to the Levenshtein distance) between the suspicious input and a hardcoded list of highly targeted corporate brands.
* **Smart Alerting:** If the input is computationally deemed "too visually similar" to a legitimate brand (e.g., > 75% similarity), it alerts the user and suggests the correct, safe URL.

## ⚙️ Prerequisites & Installation

1. **Initialize the environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
*(No external `pip` requirements are needed).*

## 📖 Help Menu
```bash
python typosquatter.py --help
```

## 💻 Command Examples

**1. Defensive Mode: Verifying a suspicious link:**
Imagine you receive an email linking to `rnicrosoft.com`. Check it before clicking:
```bash
python typosquatter.py -v rnicrosoft.com
```
*Output: 🚨 DANGER: PHISHING ATTEMPT DETECTED! Did you mean 'microsoft.com' (Similarity: 94.7%)?*

**2. Offensive Mode: Generating Threats:**
Generate hundreds of malicious variations instantly:
```bash
python typosquatter.py -d paypal.com
```

**3. Offensive Mode: Active Threat Hunting:**
Generate variations AND aggressively check internet DNS records to see which ones are actively owned by attackers:
```bash
python typosquatter.py -d amazon.com --resolve
```

## 🔮 Future Perspectives (Roadmap)
To elevate this enterprise tool further, the following features are planned:
1. **Dynamic Brand Ingestion:** Allow the verifier mode to pull the top 100,000 legitimate domains from the Tranco or Alexa Top 1M list via API, rather than relying on a hardcoded list of brands.
2. **Machine Learning Classifier:** Implement a lightweight Random Forest model trained on natural language vs. DGA (Domain Generation Algorithms) to detect randomly generated domains used by botnet Command & Control servers.
3. **Punycode (IDN) Spoofing:** Implement internationalized domain name homograph attacks using Cyrillic characters converted into Punycode (`xn--...`).
