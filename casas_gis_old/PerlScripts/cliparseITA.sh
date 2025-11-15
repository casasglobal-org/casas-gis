#!/bin/bash
# Script that transforms a string containing ET0 regions
# to a formula suitable for use in GRASS clipping.

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2006 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 10 January 2006

# Read string from GRASS parser.
HomeDir=$1
cd "$HomeDir"
file="clipRegion.txt"

# Check if the file exists
if [[ ! -f "$file" ]]; then
    echo "Can't open $file for reading."
    exit 1
fi

# Put integers indicating regions into an array.
regions=()
while IFS= read -r line; do
    regions+=($line)
done < "$file"

# Identify "zone" attribute for GRASS formula:
# "zone" is a column of the database connected
# to the evapotranspiration zones vector.
n=0
formula=()
for reg in "${regions[@]}"; do
    # Remove any leading/trailing whitespace
    reg=$(echo "$reg" | xargs)
    formula[$n]="(ISTAT=$reg)"
    n=$((n + 1))
done

# Join features selected by attribute "zone" into
# a string to use in the clipping formula.
output="formula.txt"
{
    IFS=" or "
    echo "${formula[*]}"
} > "$output"
