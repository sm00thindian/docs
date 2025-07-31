#!/bin/bash

# Exit on any error
set -e

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate the virtual environment
source venv/bin/activate

# Set SSL certificate file for secure connections
export SSL_CERT_FILE=$(python -m certifi)

# Check if src/pipeline.py exists
if [ ! -f "src/pipeline.py" ]; then
    echo "Error: src/pipeline.py not found. Ensure the project structure is correct."
    exit 1
fi

# Check if input directory is provided as an argument
if [ -z "$1" ]; then
    echo "Error: Input directory not provided."
    echo "Usage: $0 <input_directory> [output_directory]"
    echo "Example: $0 /path/to/docs output/"
    exit 1
fi

# Assign input directory
INPUT_DIR="$1"

# Assign output directory (default to 'output' if not provided)
OUTPUT_DIR="${2:-output}"

# Validate input directory
if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Input directory '$INPUT_DIR' does not exist or is not a directory."
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Validate output directory
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "Error: Could not create output directory '$OUTPUT_DIR'."
    exit 1
fi

# Run the pipeline
echo "Running pipeline with input: $INPUT_DIR and output: $OUTPUT_DIR"
python src/pipeline.py --input_dir "$INPUT_DIR" --output_dir "$OUTPUT_DIR" || {
    echo "Error: Pipeline execution failed. Check src/pipeline.py or input files."
    exit 1
}

# Print completion message
echo "Pipeline completed successfully. Output saved to $OUTPUT_DIR."
echo "To deactivate the virtual environment: deactivate"
