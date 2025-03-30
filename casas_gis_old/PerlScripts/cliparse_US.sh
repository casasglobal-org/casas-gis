#!/bin/bash
# Script that transforms a string containing attribute DBF
# values to a formula suitable for use in GRASS clipping.
# This version takes more arguments so that also attribute
# column name, and input and output files can be specified.

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2010 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 26 January 2010

# Read string from GRASS parser.
HomeDir=$1
fieldName=$2
input=$3
output=$4

# Check if the input file exists
if [[ ! -f "$input" ]]; then
    echo "Can't open $input for reading."
    exit 1
fi

# Put integers indicating regions into an array.
regions=()
while IFS= read -r line; do
    regions+=($line)
done < "$input"

# Formulate database query
n=0
formula=()
for reg in "${regions[@]}"; do
    # Remove any leading/trailing whitespace
    reg=$(echo "$reg" | xargs)
    formula[$n]="($fieldName='$reg')"
    n=$((n + 1))
done

# Write the query
{
    IFS=" or "
    echo "${formula[*]}"
} > "$output"
