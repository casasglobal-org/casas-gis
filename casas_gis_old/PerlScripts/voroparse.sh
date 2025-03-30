#!/bin/bash
# Script that transforms a string with categories
# of Voronoi polygons containing zero value points
# to a formula suitable for use in GRASS v.extract

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2006 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 4 Aprile 2006

# Read string from GRASS parser.
HomeDir=$1
cd "$HomeDir"
file="voronoi.txt"

# Check if the file exists and is readable
if [[ ! -r "$file" ]]; then
    echo "Can't open $file for reading."
    exit 1
fi

# Put categories of Voronoi polygons into an array.
regions=()
while IFS= read -r line; do
    regions+=("$line")
done < "$file"

# Identify categories for GRASS formula to
# select from vector of Voronoi polygons.
formula=()
for reg in "${regions[@]}"; do
    formula+=("(cat=$reg)")
done

# Join features selected by category into
# a string to use in the clipping formula.
output="voronoiFormula.txt"

# Write the formula to the output file
printf "%s" "${formula[*]}" > "$output"

# Replace spaces with " or " in the output file
sed -i 's/ / or /g' "$output"
