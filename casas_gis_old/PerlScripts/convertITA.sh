#!/bin/bash

# Script that tweaks output tables from CASAS systems models
# for import to GRASS-GIS, interpolation & visualization.

# This version accept outfiles names such as as "Olive-02Mar06-00003.txt".

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2006 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 13 April 2006

# Create a temporary folder for tweaked files.
HomeDir="$1"
# Import files in models directory for reading.
models_dir="$HomeDir/outfiles/"

mkdir -p "$HomeDir/models_temp"

echo "Converting ..."

# Read string from GRASS parser.
inputParFile="$models_dir/inputPar.txt"
if [ -f "$inputParFile" ]; then
  read -ra inputs < "$inputParFile"
else
  echo "File $inputParFile not found."
  exit 1
fi

# Set column numbers imported from GRASS parser as array indices
lon=$((inputs[0] - 1))
lat=$((inputs[1] - 1))
par=$((inputs[2] - 1))

# Check if the directory exists
if [ ! -d "$models_dir" ]; then
  echo "Directory $models_dir does not exist."
  exit 1
fi

# Process each file in the directory
for file in "$models_dir"*.txt; do
  if [ -f "$file" ]; then
    # Read the file and store lines in an array
    mapfile -t table < "$file"

    # Remove trailing whitespace from each line
    for i in "${!table[@]}"; do
      table[$i]=$(echo "${table[$i]}" | sed 's/[[:space:]]*$//')
    done

    # Get the parameter name
    IFS=$'\t' read -ra tempLine <<< "${table[0]}"
    parName="${tempLine[$par]}"

    # Process each line in the table
    for ((i=1; i<${#table[@]}; i++)); do
      IFS=$'\t' read -ra tempLine <<< "${table[$i]}"
      table[$i]=$(printf "%s\t%s\t%s\n" "${tempLine[$lon]}" "${tempLine[$lat]}" "${tempLine[$par]}")
    done

    # Remove the header line
    unset 'table[0]'

    # Write the tweaked file to the temporary directory
    filename=$(basename "$file" .txt)
    output="$HomeDir/models_temp/${parName}_$filename"
    printf "%s" "${table[@]}" > "$output"
  fi
done

