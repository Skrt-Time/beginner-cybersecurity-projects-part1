import os
import stat
import argparse
import sys

def check_file_permissions(filepath: str, check_writable: bool = False, check_readable: bool = False) -> bool:
    """Checks if a critical system file is dangerously accessible."""
    if not os.path.exists(filepath):
        return False
    
    # Get the file status
    st = os.stat(filepath)
    
    # Check if world-writable (Others can write)
    if check_writable and bool(st.st_mode & stat.S_IWOTH):
        return True
        
    # Check if world-readable (Others can read)
    if check_readable and bool(st.st_mode & stat.S_IROTH):
        return True
        
    return False

def find_suid_binaries(search_paths: list) -> list:
    """Hunts for SUID binaries which can run with root privileges."""
    suid_files = []
    
    for path in search_paths:
        if not os.path.exists(path):
            continue
            
        for root, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    st = os.stat(full_path)
                    # Check if the SUID bit is set
                    if stat.S_ISUID & st.st_mode:
                        suid_files.append(full_path)
                except Exception:
                    # Ignore files we do not have permission to stat
                    continue
                    
    return suid_files

def check_ssh_root_login() -> str:
    """Checks the SSH configuration to see if root can login directly."""
    sshd_config = "/etc/ssh/sshd_config"
    if not os.path.exists(sshd_config):
        return "Not found"
        
    try:
        with open(sshd_config, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("PermitRootLogin"):
                    return line.split()[1]
    except PermissionError:
        return "Permission denied to read"
        
    return "Not explicitly defined (Default varies)"

def main():
    parser = argparse.ArgumentParser(description="Linux Local Privilege Escalation Analyzer")
    parser.add_argument("-o", "--output", help="Save the audit report to a text file")
    
    args = parser.parse_args()
    
    print("="*70)
    print("🐧 Linux Local Privilege Escalation Analyzer (Mini-PEAS)")
    print("="*70)
    print("[*] Starting system audit...\n")
    
    findings = []
    
    # 1. Check critical files
    print("[*] Checking critical system files...")
    
    if check_file_permissions("/etc/passwd", check_writable=True):
        alert = "🚨 CRITICAL: /etc/passwd is world-writable! An attacker can create a new root user."
        print(alert)
        findings.append(alert)
    else:
        print(" [+] /etc/passwd permissions are secure.")
        
    if check_file_permissions("/etc/shadow", check_readable=True):
        alert = "🚨 CRITICAL: /etc/shadow is world-readable! An attacker can crack password hashes."
        print(alert)
        findings.append(alert)
    else:
        print(" [+] /etc/shadow permissions are secure.")
        
    # 2. Check SSH Root Login
    print("\n[*] Analyzing SSH Configuration...")
    root_login_status = check_ssh_root_login()
    if root_login_status.lower() in ["yes", "without-password"]:
        alert = f"⚠️  WARNING: Direct SSH Root Login is allowed ({root_login_status})."
        print(alert)
        findings.append(alert)
    else:
        print(f" [+] SSH Root Login status: {root_login_status}")

    # 3. Hunt for SUID binaries
    print("\n[*] Hunting for SUID binaries (This may take a few seconds)...")
    # Limiting paths for speed in this educational tool
    common_paths = ["/bin", "/usr/bin", "/sbin", "/usr/sbin"]
    suid_binaries = find_suid_binaries(common_paths)
    
    if suid_binaries:
        print(f" ╰──> Found {len(suid_binaries)} SUID binaries.")
        print("      (Review these against GTFOBins for potential exploit paths)")
        # Store a summary in findings
        findings.append(f"Found {len(suid_binaries)} SUID binaries in standard paths.")
    else:
        print(" [+] No unusual SUID binaries found in standard paths.")

    print("\n" + "="*70)
    print("📋 AUDIT SUMMARY:")
    if findings:
        print("[!] Vulnerabilities or misconfigurations detected! Review the logs above.")
    else:
        print("[+] System baseline appears secure against basic PrivEsc vectors.")
    print("="*70)

    # Export report
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write("System Privilege Escalation Audit Report\n")
                f.write("="*40 + "\n\n")
                if findings:
                    f.write("FINDINGS:\n")
                    for finding in findings:
                        f.write(f"- {finding}\n")
                else:
                    f.write("No critical vulnerabilities detected.\n")
                    
                if suid_binaries:
                    f.write("\nSUID BINARIES DETECTED:\n")
                    for binary in suid_binaries:
                        f.write(f"- {binary}\n")
            print(f"[+] Full audit report successfully saved to '{args.output}'")
        except Exception as e:
            print(f"[-] Error saving report: {e}")

if __name__ == "__main__":
    main()
