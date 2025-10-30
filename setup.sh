#!/bin/bash

set -e  # Exit on error

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

mkdir -p examples output

source venv/bin/activate

python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org

pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --quiet

export SSL_CERT_FILE=$(python -m certifi)

python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('punkt_tab', quiet=True)"

python -m spacy download en_core_web_lg

echo "Setup complete. Run:"
echo "source venv/bin/activate"
echo "export SSL_CERT_FILE=$(python -m certifi)"
echo "python src/pipeline.py --input_dir examples/ --output_dir output/ [--ocr_images] [--to_pdf]"
