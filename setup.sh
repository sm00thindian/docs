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
echo "To deactivate: deactivate"
echo "To run:"
echo "python src/pipeline.py --input_dir path/to/docs --output_dir output/"
