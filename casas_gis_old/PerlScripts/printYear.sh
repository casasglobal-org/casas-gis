#!/bin/bash

# Script that prints analysis years to a file according to
# GRASS parser input for use in legend.

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2006 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 2 March 2006

# Import files in models directory for reading.
HomeDir="$1"
models_dir="$HomeDir/outfiles/"

# Check if the directory exists
if [ ! -d "$models_dir" ]; then
  echo "Directory $models_dir does not exist."
  exit 1
fi

fileNumber=1
declare -a years

# Loop through each file in the directory
for file in "$models_dir"*.txt; do
  if [ -f "$file" ]; then
    # Read the file and store lines in an array
    mapfile -t table < "$file"

    # Read inputPar.txt to get the column index
    inputParFile="$models_dir/inputPar.txt"
    if [ -f "$inputParFile" ]; then
      read -ra inputs < "$inputParFile"
      yearColumn=$((inputs[3] - 1))

      # Extract the year from the specified column
      IFS=$'\t' read -ra columns <<< "${table[1]}"
      years[$fileNumber-1]=${columns[$yearColumn]}

      # Write the year to an output file
      output="year$fileNumber.txt"
      echo "${columns[$yearColumn]}" > "$HomeDir/$output"

      ((fileNumber++))
    else
      echo "File $inputParFile not found."
      exit 1
    fi
  fi
done

# Join years of interest to the analysis and print them to a text file.
# Uncomment the following lines if needed
# output="years$fileNumber.txt"
# echo "${years[@]}" > "$HomeDir/$output"

