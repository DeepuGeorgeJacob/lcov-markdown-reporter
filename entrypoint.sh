#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Use positional arguments from Docker args ---
LCOV_FILENAME="$1"
OUTPUT_FILENAME="$2"

# Construct the absolute path by combining the workspace root and the validated input.
LCOV_FILE=${LCOV_FILENAME}
OUTPUT_FILE=${OUTPUT_FILENAME}


echo "Starting LCOV to Markdown conversion..."
echo "  Input LCOV File: ${LCOV_FILE}"
echo "  Output Markdown File: ${OUTPUT_FILE}"

# Execute the main Python script, using the reporter.py file we built
# Note: You must ensure reporter.py (or main.py if you renamed it) exists in /app/
python3 /app/main.py "$LCOV_FILE" "$OUTPUT_FILE"

echo "Conversion complete. Report written to ${OUTPUT_FILE}"