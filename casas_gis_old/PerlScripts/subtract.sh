#!/bin/bash
############################################################################
#
# MODULE:       diff.sh
#
# AUTHOR(S):    Luigi Ponti
#
# PURPOSE:      Makes a CASAS-mappable file by subtracting two model
#               output files one from the other.
#
# NOTE:
#
# Copyright:    (c) 2008 Luigi Ponti, quartese at gmail.com
#               CASAS (Center for the Analysis of Sustainable
#               Agricultural Systems, https://www.casasglobal.org/)
#
#               SPDX-License-Identifier: GPL-2.0-or-later
#
#############################################################################

# %Module
# % description: Makes a CASAS-mappable file subracting two model output files
# %End

# %option
# % key: working_directory
# % type: string
# % answer: /home/andy/outfiles/
# % gisprompt: old_file,file,input
# % description: Directory where input files are
# % required: yes
# %end

# %option
# % key: warmest_file
# % type: string
# % gisprompt: old_file,file,input
# % description: Warmed weather file
# % required: yes
# %end

# %option
# % key: observed_file
# % type: string
# % gisprompt: old_file,file,input
# % description: Observed weather file
# % required: yes
# %end

# %option
# % key: diff_file
# % type: string
# % gisprompt: new_file,file,output
# % description: New output file
# % required: yes
# %end

# Check if the script is being run within GRASS GIS
if [ -z "$GISBASE" ]; then
    echo "You must be in GRASS GIS to run this program." >&2
    exit 1
fi

# Check if the arguments have been parsed
if [ "$1" != "@ARGS_PARSED@" ]; then
    args=""
    for arg in "$@"; do
        args+=" $arg "
    done
    "$GISBASE/bin/g.parser" "$0" $args
    exit
fi

# Read environment variables for file paths
workDir=$GIS_OPT_workDir
warmFile=$GIS_OPT_warmFile
obsFile=$GIS_OPT_obsFile
diffFile=$GIS_OPT_diffFile

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
