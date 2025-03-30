#!/bin/bash
# Script developed to calculate the difference
# between observed and warming weather scenarios
# in CASAS model outputs. NOTE: the script is supposed
# to use files with the same number of rows & columns.

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2008 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 22 January 2008

# Syntax:
# bash SubtractOutput.sh [directory where files are] [warming file] [observed file] [new file]
# Example:
# bash SubtractOutput.sh "/models/oliveGIS/" Olive_17gen08_AvgPlus3.txt Olive_17gen08_AvgObs.txt Olive_17gen08_AvgDiff3.txt

# Read arguments.
workDir=$1
warmFile=$2
obsFile=$3
diffFile=$4

# Check if the files exist and are readable
if [[ ! -r "$workDir/$warmFile" || ! -r "$workDir/$obsFile" ]]; then
    echo "Can't open files for reading."
    exit 1
fi

# Read warmer weather file.
cd "$workDir"
warmTable=($(tail -n +2 "$warmFile"))

# Read observed weather file.
obsTable=($(tail -n +2 "$obsFile"))

# Copy headers to table for new file.
header=$(head -n 1 "$obsFile")

# How many rows in input files (should be the same for both)?
numRows=${#obsTable[@]}

# Define a variable for number of columns.
numCols=$(awk -F'\t' '{print NF; exit}' "$warmFile")

# Perform subtraction.
diffTable=("$header")
for ((row = 0; row < numRows; row++)); do
    warmTableRow=($(echo "${warmTable[$row]}" | tr '\t' ' '))
    obsTableRow=($(echo "${obsTable[$row]}" | tr '\t' ' '))

    diffTableRow=()
    for ((col = 0; col < 11; col++)); do
        # Use the value of the observed weather file for the new file.
        diffTableRow+=("${obsTableRow[$col]}")
    done

    for ((col = 11; col < numCols; col++)); do
        if [[ "${warmTableRow[$col]}" =~ ^-?[0-9]*\.?[0-9]+$ ]]; then
            # Get the difference and put that in the new table.
            diffTableRow+=($(echo "${warmTableRow[$col]} - ${obsTableRow[$col]}" | bc))
        else
            # Just use the value of the observed weather file.
            diffTableRow+=("${obsTableRow[$col]}")
        fi
    done

    # Now join the new table row.
    diffTable+=($(IFS=$'\t'; echo "${diffTableRow[*]}"))
done

# Save new file which contains differences.
printf "%s\n" "${diffTable[@]}" > "$diffFile"
