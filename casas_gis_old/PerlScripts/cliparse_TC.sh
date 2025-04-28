#!/bin/bash
# Script that transforms a string containing attribute DBF
# values to a formula suitable for use in GRASS clipping.
# This version takes more arguments so that also attribute
# column name, and input and output files can be specified.
# _TC means type check--it checks type of column to know
# if quoting is necessary. Number or string.

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2010 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 26 January 2010

# Read string from GRASS parser.
HomeDir=$1
fieldName=$2
fieldType=$3
input=$4
output=$5

# Check if the input file exists
if [[ ! -f "$input" ]]; then
    echo "Can't open $input for reading."
    exit 1
fi

# Put integers indicating regions into an array.
regions=()
while IFS= read -r line; do
    # This is for compatibility with scripts that take comma-separated lists
    # as input. The EurMedGrape script uses a list of country names that
    # is comma-separated because some country names include spaces, and hence
    # the script would not know where to split based on spaces.
    if [[ "$line" == *","* ]]; then
        IFS=',' read -r -a regions <<< "$line"
    else
        regions+=($line)
    fi
done < "$input"

# Formulate database query
n=0
formula=()
if [[ "$fieldType" == "number" ]]; then
    # It is a number
    for reg in "${regions[@]}"; do
        # Remove any leading/trailing whitespace
        reg=$(echo "$reg" | xargs)
        formula[$n]="($fieldName=$reg)"
        n=$((n + 1))
    done
else
    # It is a string, you need to quote it
    for reg in "${regions[@]}"; do
        # Remove any leading/trailing whitespace
        reg=$(echo "$reg" | xargs)
        formula[$n]="($fieldName='$reg')"
        n=$((n + 1))
    done
fi

# Write the query
{
    IFS=" or "
    echo "${formula[*]}"
} > "$output"
