#!/bin/bash

# Default values
QUALITY=95
OUTPUT=""
PORT=8090
MODE=""

show_help() {
  cat << EOF
Usage: $0 [options]

Options for Streamlit (-s):
  -p    Port number for Streamlit app (default: 8090)

General:
  -h    Show this help message and exit

Examples:
  Run Streamlit app on custom port 8501:
    $0 -p 8501

EOF
  exit 1
}

# Parse options
while getopts "p:h" opt; do
  case ${opt} in
    p ) PORT=$OPTARG ;;
    h ) show_help ;;
    \? ) echo "Invalid option: -$OPTARG" >&2; show_help ;;
    : ) echo "Option -$OPTARG requires an argument." >&2; show_help ;;
  esac
done

# Set Source to Virtual Environment
source ./venv/bin/activate

# Install the Dependencies
pip install -r requirements.txt

# Run the App
streamlit run app.py --server.port "$PORT"
