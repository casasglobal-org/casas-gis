#!/bin/bash

# Script that prints column and row names of model output files
# for proper input selection in the GRASS parser.
# The part that prints years for legend has been
# transferred to a printYear.sh script (NOTE).

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2006 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 2 March 2006

# Import files in models directory for reading.
HomeDir=$1
models_dir="$HomeDir/outfiles/"

# Check if the directory exists
if [ ! -d "$models_dir" ]; then
  echo "Directory $models_dir does not exist."
  exit 1
fi

fileNumber=1

# Loop through each file in the directory
for file in "$models_dir"*.txt; do
  if [ -f "$file" ]; then
    # Read the file and store lines in an array
    mapfile -t table < "$file"

    # Print column names just once
    if [ $fileNumber -eq 1 ]; then
      IFS=$'\t' read -ra columns <<< "${table[0]}"
      echo -e "\nThe following column names were found:\n"
      for i in "${!columns[@]}"; do
        echo "$((i+1)). ${columns[$i]}"
      done

      # Print the number of rows
      rowNum=${#table[@]}
      echo -e "\nNumber of rows is $rowNum.\n"
    fi

    ((fileNumber++))
  fi
done

