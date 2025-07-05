#!/bin/bash
echo "[+] Installing dependencies..."
sudo apt update
sudo apt install -y git curl jq

go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
go install -v github.com/hahwul/dalfox/v2@latest
go install -v github.com/lc/gau@latest

echo 'export PATH="$PATH:$(go env GOPATH)/bin"' >> ~/.bashrc
source ~/.bashrc
echo "[✔] Done."
