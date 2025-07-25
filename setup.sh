#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --quiet

# Print confirmation
echo "Virtual environment activated and dependencies installed."
echo "To run the main script: python src/main.py"
echo "To deactivate: deactivate"
