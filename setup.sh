#!/bin/bash

# Exit on any error
set -e

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version (e.g., ensure >= 3.8 for spaCy compatibility)
PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
MIN_VERSION="3.8"
if [ "$(printf '%s\n' "$PYTHON_VERSION" "$MIN_VERSION" | sort -V | head -n1)" != "$MIN_VERSION" ]; then
    echo "Error: Python $MIN_VERSION or higher is required. Found $PYTHON_VERSION."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Set SSL certificate file for secure connections
export SSL_CERT_FILE=$(python -m certifi)

# Create directories
mkdir -p examples output

# Upgrade pip to avoid potential issues with outdated versions
pip install --upgrade pip --quiet

# Install dependencies
echo "Installing dependencies from requirements.txt..."
if ! pip install -r requirements.txt --quiet; then
    echo "Error: Failed to install dependencies. Check requirements.txt or network connection."
    exit 1
fi

# Download NLTK resources
echo "Downloading NLTK resources..."
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('punkt_tab', quiet=True)" || {
    echo "Error: Failed to download NLTK resources."
    exit 1
}

# Download spaCy model
echo "Downloading spaCy model en_core_web_sm..."
if ! python -m spacy download en_core_web_sm --quiet; then
    echo "Error: Failed to download spaCy model en_core_web_sm."
    exit 1
}

# Print confirmation and instructions
echo -e "\nSetup completed successfully!"
echo "Virtual environment is activated for this session."
echo "To deactivate: deactivate"
echo -e "\nTo run the pipeline:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo "2. Set the SSL certificate (if needed):"
echo "   export SSL_CERT_FILE=$(python -m certifi)"
echo "3. Run the pipeline with your input directory:"
echo "   python src/pipeline.py --input_dir /path/to/your/docs --output_dir output/"
echo -e "\nReplace '/path/to/your/docs' with the actual path to your documents."
