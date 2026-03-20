#!/bin/bash
# Setup script for India Problem Scanner Agent

echo "Updating system and installing python3-pip..."
sudo apt-get update
sudo apt-get install -y python3-pip

echo "Installing required Python libraries..."
python3 -m pip install -r requirements.txt

echo "Setup complete! Please configure your .env file."
