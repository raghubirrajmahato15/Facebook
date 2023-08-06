#!/bin/bash

# Update system packages
sudo apt update
sudo apt upgrade -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install gdebi-core
sudo gdebi google-chrome-stable_current_amd64.deb
sudo apt update


# Uninstall existing packages
sudo apt remove -y chromium-browser chromium-chromedriver python3-pip tesseract-ocr tesseract-ocr-eng


# Install required packages
sudo apt install -y python3 python3-pip tesseract-ocr tesseract-ocr-eng

# Install Chromium (replace with your preferred browser if not using Chromium)
sudo apt install chromium
sudo apt install chromium-common
sudo apt install chromium-driver
sudo apt install chromium-l10n
sudo apt install chromium-sandbox
sudo apt install chromium-shell


# Install Python dependencies
pip3 install --upgrade pip
pip3 install asyncio aiohttp selenium requests Pillow pytesseract termcolor



# Provide a success message
echo "Setup complete! You can now run your automatic login tool using the provided Python script."
