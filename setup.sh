#!/bin/bash

# Directories to store tools
TOOLS_DIR="$HOME/security-tools"
mkdir -p $TOOLS_DIR

# Update system and install necessary dependencies
echo "[+] Updating system and installing dependencies..."
sudo apt-get update && sudo apt-get install -y git python3 python3-pip ruby curl proxychains4 python3-tk

# Cloning necessary tools
echo "[+] Cloning required tools..."
cd $TOOLS_DIR

# Clone tools
git clone https://github.com/aboul3la/Sublist3r.git
git clone https://github.com/sqlmapproject/sqlmap.git
git clone https://github.com/ifrostman/wapiti.git
git clone https://github.com/wpscanteam/wpscan.git
git clone https://github.com/Viralmaniar/BigBountyRecon.git
git clone https://github.com/googleinurl/SCANNER-INURLBR.git dorking_tool

# Install Python dependencies
echo "[+] Installing Python dependencies..."
pip3 install -r $TOOLS_DIR/Sublist3r/requirements.txt
pip3 install wapiti3 requests proxybroker

# Install Ruby dependencies for WPScan
echo "[+] Installing Ruby dependencies..."
sudo gem install wpscan

echo "[+] Setup completed successfully. You can now run AutoProx."
