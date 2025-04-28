#!/bin/bash
# Script that tweaks output tables from CASAS systems models
# for import to GRASS-GIS, interpolation & visualization.

# This version accepts output file names such as "Olive_02Mar06_00003.txt".

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2006 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 2 February 2006

# Create a temporary folder for tweaked files.
HomeDir="$1"

# Permissive chmod
# https://www.perlmonks.org/?node_id=543062
# umask 0

# mkdir -m 777 "$HomeDir/models_temp/"
mkdir "$HomeDir/models_temp/"


# Read string from GRASS parser.
cd "$HomeDir"
file="inputPar.txt"
if [[ ! -f "$file" ]]; then
    echo "Can't open $file for reading."
    exit 1
fi

# Put integers indicating columns into an array.
inputs=()
while IFS= read -r line; do
    inputs+=($line)
done < "$file"

# Import files in models directory for reading.
models_dir="./outfiles/"
if [[ ! -d "$models_dir" ]]; then
    echo "Can't open directory $models_dir."
    exit 1
fi

# Set column numbers imported from GRASS parser as array indices
# and make the scope of corresponding variables wide enough by keeping
# them out of the loop.
lon=$((inputs[0] - 1))
lat=$((inputs[1] - 1))
par=$((inputs[2] - 1))
parName=""

# Import model output files for reading
for file in "$models_dir"*.txt; do
    if [[ -f "$file" ]]; then
        cd "$HomeDir/outfiles/"
        table=()
        while IFS= read -r line; do
            # Strip off all trailing white spaces - tabs, spaces, new lines and returns as well.
            # This makes your code work on Unix and Linux whether the input file is from Windows or from Unix.
            # As a side effect, it also removes any trailing whitespace on each line which is usually but not always an advantage.
            # Source: http://www.wellho.net/forum/Perl-Programming/New-line-characters-beware.html
            line=$(echo "$line" | sed 's/[[:space:]]*$//')
            if [[ -n "$line" ]]; then
                table+=("$line")
            fi
        done < "$file"

        # Make longitude negative (necessary for import to LatLong location).
        array_size=${#table[@]}
        for ((i = 1; i < array_size; i++)); do
            IFS=$'\t' read -r -a tempLine <<< "${table[$i]}"
            tempLine[$lon]=$(echo "${tempLine[$lon]} * -1" | bc)

            # Get name of the parameter being mapped.
            if [[ $i == 1 ]]; then
                IFS=$'\t' read -r -a tempLine <<< "${table[0]}"
                parName="${tempLine[$par]}"
            fi
            table[$i]=$(IFS=$'\t'; echo "${tempLine[$lon]} ${tempLine[$lat]} ${tempLine[$par]}")
        done

        # Get rid of column names (as of GRASS 6.0.0, there is no way to skip header line).
        unset 'table[0]'

        # Write tweaked files to the temporary directory from where they
        # should be imported by the main shell script.
        cd "$HomeDir/models_temp/"
        baseName=$(basename "$file" .txt)
        file2="${parName}_${baseName}"
        output="$file2"
        {
            printf "%s\n" "${table[@]}"
        } > "$output"
    fi
done
