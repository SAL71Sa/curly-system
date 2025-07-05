#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime

def print_banner():
    banner = r"""
 _____  ___   _     ___  ___  ___   _   _         ___   _     _____ _   _______ _____ 
/  ___|/ _ \ | |    |  \/  | / _ \ | \ | |       / _ \ | |   |  _  | | | |  ___|_   _|
\ `--./ /_\ \| |    | .  . |/ /_\ \|  \| |______/ /_\ \| |   | | | | | | | |_    | |  
 `--. \  _  || |    | |\/| ||  _  || . ` |______|  _  || |   | | | | | | |  _|   | |  
/\__/ / | | || |____| |  | || | | || |\  |      | | | || |___\ \_/ / |_| | |    _| |_ 
\____/\_| |_/\_____/\_|  |_/\_| |_/\_| \_/      \_| |_/\_____/\___/ \___/\_|    \___/ 


    """
    print(banner)
    print("Tool ID: EAL")
    print("Developed by SALMAN - ALOUFI
")

def run_command(cmd, output_file=None):
    print(f"[+] Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if output_file:
        with open(output_file, "w") as f:
            f.write(result.stdout)
    return result.stdout

def main(domain):
    print_banner()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"results/{domain}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Subfinder
    sub_file = f"{output_dir}/subs.txt"
    run_command(f"subfinder -d {domain} -silent", sub_file)

    # Step 2: Live hosts
    live_file = f"{output_dir}/live.txt"
    run_command(f"httpx -l {sub_file} -silent", live_file)

    # Step 3: URLs
    urls_file = f"{output_dir}/urls.txt"
    run_command(f"cat {sub_file} | gau", urls_file)

    # Step 4: Nuclei scan
    nuclei_file = f"{output_dir}/nuclei.txt"
    run_command(f"nuclei -l {live_file} -severity critical,high,medium,low -silent", nuclei_file)

    # Step 5: Dalfox scan
    dalfox_file = f"{output_dir}/dalfox.txt"
    run_command(f"dalfox file {urls_file} --skip-bav -o {dalfox_file}")

    print(f"
[✔] All scans completed. Results saved in {output_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SALMAN - ALOUFI | EAL Tool")
    parser.add_argument("-d", "--domain", required=True, help="Target domain")
    args = parser.parse_args()
    main(args.domain)
