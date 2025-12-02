#!/bin/bash

# Script that transforms a string containing ET0 regions
# to a formula suitable for use in GRASS clipping.

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2006 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 10 January 2006

# Read string from GRASS parser.
HomeDir=$1
clipRegionFile="$HomeDir/clipRegion.txt"

if [ -f "$clipRegionFile" ]; then
  read -ra regions < "$clipRegionFile"
else
  echo "File $clipRegionFile not found."
  exit 1
fi

# Identify "zone" attribute for GRASS formula.
formula=()
for reg in "${regions[@]}"; do
  formula+=("(zone=$reg)")
done

# Join features selected by attribute "zone" into
# a string to use in the clipping formula.
output="$HomeDir/formula.txt"
printf "%s" "${formula[*]}" | sed 's/ / or /g' > "$output"

