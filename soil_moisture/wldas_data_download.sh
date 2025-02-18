#!/bin/bash

# Base URL components
BASE_URL="https://hydro1.gesdisc.eosdis.nasa.gov/data/WLDAS/WLDAS_NOAHMP001_DA1.D1.0"
YEAR=2001
MONTH=01
PYTHON_SCRIPT="process_file.py"  # Change this to your actual Python script

# Authentication cookies file (uses .netrc for credentials)
COOKIE_FILE="$HOME/.urs_cookies"

# Loop through all days of the month
for DAY in {01..31}; do
    FILE_NAME="WLDAS_NOAHMP001_DA1_${YEAR}${MONTH}${DAY}.D10.nc"
    FILE_URL="${BASE_URL}/${YEAR}/${MONTH}/${FILE_NAME}"

    echo "Downloading: $FILE_URL"

    # Use curl with recommended options for NASA Earthdata authentication
    curl -n -c "$COOKIE_FILE" -b "$COOKIE_FILE" -LJO --url "$FILE_URL"

    # Check if download was successful before running Python script
    if [[ -f "$FILE_NAME" ]]; then
        echo "Processing: $FILE_NAME"
        python3 "$PYTHON_SCRIPT" "$FILE_NAME"
    else
        echo "Failed to download: $FILE_NAME"
    fi
done

echo "Download and processing complete."

