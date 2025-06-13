#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install system dependencies
apt-get update -y
apt-get install -y tesseract-ocr
apt-get install -y tesseract-ocr-eng

# Install Python dependencies
pip install -r requirements.txt 