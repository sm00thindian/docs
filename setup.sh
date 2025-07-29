#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --quiet
export SSL_CERT_FILE=$(python -m certifi)

python -c "import nltk; nltk.download('punkt');nltk.download('stopwords');nltk.download('punkt_tab')"

python -m spacy download en_core_web_sm

# Print confirmation
echo "Virtual environment activated and dependencies installed."
echo "To deactivate: deactivate"
echo "To run:"
echo "source venv/bin/activate"
echo "python src/pipeline.py --input_dir path/to/docs --output_dir output/"
