#!/bin/bash

set -e

function install_termux_dependencies() {
    echo "Installing required packages for Termux..."
    pkg update
    pkg upgrade -y
    pkg install -y python
    pkg install -y tesseract
    pkg install -y wget
    pkg install -y unzip
    pkg install -y sqlite
    echo "Required packages for Termux installed successfully."
}

function install_kali_dependencies() {
    echo "Installing required packages for Kali Linux..."
    sudo apt update
    sudo apt upgrade -y
    sudo apt install -y python3-pip
    sudo apt install -y tesseract-ocr
    sudo apt install -y libtesseract-dev
    sudo apt install -y wget
    sudo apt install -y unzip
    sudo apt install -y sqlite3
    echo "Required packages for Kali Linux installed successfully."
}

function install_python_packages() {
    echo "Installing Python packages..."
    pip3 install aiohttp
    pip3 install selenium
    pip3 install requests
    pip3 install Pillow
    pip3 install pytesseract
    pip3 install termcolor
    echo "Python packages installed successfully."
}

function download_chromedriver() {
    echo "Downloading ChromeDriver..."
    CHROME_DRIVER_VERSION="94.0.4606.41"
    wget -O chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip
    unzip -o chromedriver.zip
    rm -f chromedriver.zip
    chmod +x chromedriver
    sudo mv chromedriver /usr/local/bin/
    echo "ChromeDriver installed successfully."
}

function setup_database() {
    echo "Setting up database..."
    DB_FILE="login_results.db"98
    if [ -f "$DB_FILE" ]; then
        rm -f "$DB_FILE"
    fi
    sqlite3 "$DB_FILE" "CREATE TABLE IF NOT EXISTS login_attempts (username TEXT, password TEXT);"
    echo "Database set up successfully."
}

function run_python_script() {
    echo "Running Python script..."
    python3 facebook.py
    echo "Python script completed."
}

echo "Welcome to the Automated Login Setup Script!"

if [ -x "$(command -v pkg)" ]; then
    install_termux_dependencies
elif [ -x "$(command -v apt)" ]; then
    install_kali_dependencies
else
    echo "Unsupported operating system. Please install the required packages manually."
    exit 1
fi

install_python_packages
download_chromedriver
setup_database
run_python_script
