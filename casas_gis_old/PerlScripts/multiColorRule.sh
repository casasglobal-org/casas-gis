#!/bin/bash
# Script that writes color rules file to apply a unique color rule
# to models raters based on overall range of data.

# Compared to rangeColorRule.pl, this version can use any
# combination of any number of colors.

# The central color will get a zero value.

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2008 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 24 April 2008

# Set some variables.
HomeDir=$1
rule=$2
lowCut=$3
hiCut=$4
divergentRule=$5

# Check if the directory exists
if [[ ! -d "$HomeDir/models_temp/" ]]; then
    echo "Directory $HomeDir/models_temp/ does not exist."
    exit 1
fi

# Read temporary files.
cd "$HomeDir/models_temp/"

# Import model output files for reading
range=()
for file in *; do
    while IFS= read -r line; do
        # Remove trailing whitespace
        line=$(echo "$line" | sed 's/[[:space:]]*$//')
        range+=("$(echo "$line" | awk '{print $3}')")
    done < "$file"
done

# Sort and get maximum and minimum of overall range of data.
sortedRange=($(printf "%s\n" "${range[@]}" | sort -n))
min=${sortedRange[0]}
max=${sortedRange[-1]}

# Check if cutting points influence the range.
if (( $(echo "$hiCut < $max" | bc -l) )); then
    max=$hiCut
fi
if (( $(echo "$lowCut > $min" | bc -l) )); then
    min=$lowCut
fi

# Change to the home directory
cd "$HomeDir"
output="customColorRule.txt"

# Put colors into an array.
IFS='-' read -r -a colors <<< "$rule"

# Compute number of colors and bands.
numOfColors=${#colors[@]}
NumOfBands=$((numOfColors - 1))
halfNumOfBands=$(( (numOfColors - 1) / 2 ))

if [ "$divergentRule" == "divNo" ]; then
    # Build array of coefficients.
    baseCoeff=$(echo "scale=2; 1 / $NumOfBands" | bc)
    coefficients=("$min")
    for ((i = 1; i <= NumOfBands - 1; i++)); do
        coefficients+=($(echo "$min + ($i * $baseCoeff * ($max - $min))" | bc))
    done
    coefficients+=("$max")

    # Print color rule file.
    {
        for ((i = 0; i < numOfColors; i++)); do
            echo "${coefficients[$i]} ${colors[$i]}"
        done
        echo "end"
    } > "$output"

elif [ "$divergentRule" == "divYes" ]; then
    # Build array of coefficients.
    baseCoeff=$(echo "scale=2; 1 / $halfNumOfBands" | bc)
    coefficients=("$min")
    for ((i = halfNumOfBands - 1; i >= 1; i--)); do
        coefficients+=($(echo "$i * $baseCoeff * $min" | bc))
    done

    if (( numOfColors % 2 == 1 )); then
        coefficients+=("0")
    else
        coefficients+=("0" "0")
    fi

    for ((i = 1; i <= halfNumOfBands - 1; i++)); do
        coefficients+=($(echo "$i * $baseCoeff * $max" | bc))
    done
    coefficients+=("$max")

    # Print color rule file.
    {
        for ((i = 0; i < numOfColors; i++)); do
            echo "${coefficients[$i]} ${colors[$i]}"
        done
        echo "end"
    } > "$output"
fi

# Print file with the minimum value of data range.
echo "$min" > "min.txt"

# Print file with the maximum value of data range.
echo "$max" > "max.txt"
