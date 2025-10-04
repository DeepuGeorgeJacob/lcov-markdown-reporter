#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Map GitHub Action inputs (e.g., INPUT_LCOV-FILE) to local variables
LCOV_FILE="/github/workspace/${INPUT_LCOV_FILE}"
OUTPUT_FILE="/github/workspace/${INPUT_OUTPUT_FILE}"

echo "Starting LCOV to Markdown conversion..."
echo "  Input LCOV File: ${LCOV_FILE}"
echo "  Output Markdown File: ${OUTPUT_FILE}"

# Execute the main Python script
# Note: The script runs within the container, but uses the /github/workspace paths.
python3 /app/main.py "$LCOV_FILE" "$OUTPUT_FILE"

echo "Conversion complete. Report written to ${OUTPUT_FILE}"