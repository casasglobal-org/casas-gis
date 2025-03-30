#!/bin/bash
# Script that takes the output of r.stats and
# puts it in a form suitable to produce a plot.

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2006 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 15 September 2006

# Read directory where maps are saved and
# other parameters from script arguments.
SaveDir=$1

# Check if the directory exists
if [[ ! -d "$SaveDir" ]]; then
    echo "Directory $SaveDir does not exist."
    exit 1
fi

# Change to the directory
cd "$SaveDir"

# Read *.rep files produced by r.stats
for file in *.rep; do
    if [[ -f "$file" ]]; then
        newTable=()
        while IFS= read -r line; do
            # Put rows as elements of the table array.
            table+=("$line")
        done < "$file"

        # Split rows in cells and rearrange them
        array_size=${#table[@]}
        IFS=$'\t' read -r -a firstLine <<< "${table[0]}"
        IFS=$'\t' read -r -a lastLine <<< "${table[$array_size-1]}"

        # Get the lowest and highest zone index in table
        firstZone=${firstLine[0]}
        currZone=$firstZone
        prevZone=$currZone
        newLine=(0 0 0 0 0)

        for row in "${table[@]}"; do
            IFS=$'\t' read -r -a tempLine <<< "$row"
            currZone=${tempLine[0]}
            if [[ "$currZone" == "$prevZone" ]]; then
                if [[ "${tempLine[1]}" == "1" ]]; then
                    newLine[1]=${tempLine[2]}
                elif [[ "${tempLine[1]}" == "2" ]]; then
                    newLine[2]=${tempLine[2]}
                elif [[ "${tempLine[1]}" == "3" ]]; then
                    newLine[3]=${tempLine[2]}
                elif [[ "${tempLine[1]}" == "4" ]]; then
                    newLine[4]=${tempLine[2]}
                fi
                newLine[0]=$currZone
            elif [[ "$currZone" != "$prevZone" ]]; then
                tablePush=$(IFS=$'\t'; echo "${newLine[*]}")
                newTable+=("$tablePush")
                newLine=(0 0 0 0 0)
                if [[ "${tempLine[1]}" == "1" ]]; then
                    newLine[1]=${tempLine[2]}
                elif [[ "${tempLine[1]}" == "2" ]]; then
                    newLine[2]=${tempLine[2]}
                elif [[ "${tempLine[1]}" == "3" ]]; then
                    newLine[3]=${tempLine[2]}
                elif [[ "${tempLine[1]}" == "4" ]]; then
                    newLine[4]=${tempLine[2]}
                fi
                newLine[0]=$currZone
            fi
            prevZone=$currZone
        done

        # Otherwise the last line does not get printed
        tablePush=$(IFS=$'\t'; echo "${newLine[*]}")
        newTable+=("$tablePush")
        output="${file%.rep}.tab"
        printf "%s\n" "${newTable[@]}" > "$output"
    fi
done

# Read *.tot files produced by r.stats
for file in *.tot; do
    if [[ -f "$file" ]]; then
        while IFS= read -r line; do
            # Put rows as elements of the table array.
            table+=("$line")
        done < "$file"

        newLine=(0 0 0 0 0)
        for row in "${table[@]}"; do
            IFS=$'\t' read -r -a tempLine <<< "$row"
            if [[ "${tempLine[0]}" == "1" ]]; then
                newLine[1]=${tempLine[1]}
            elif [[ "${tempLine[0]}" == "2" ]]; then
                newLine[2]=${tempLine[1]}
            elif [[ "${tempLine[0]}" == "3" ]]; then
                newLine[3]=${tempLine[1]}
            elif [[ "${tempLine[0]}" == "4" ]]; then
                newLine[4]=${tempLine[1]}
            fi
        done
        newLine[0]=1
        output="${file%.tot}.tabTot"
        printf "%s\n" "${newLine[*]}" > "$output"
    fi
done
