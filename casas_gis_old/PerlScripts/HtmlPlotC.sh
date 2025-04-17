#!/bin/bash
# Script that plots histograms produced by
# d.histogram and puts .png outputs in a HTML page

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2008 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 16 January 2008

# Read Directory where maps are saved and
# other parameters from script arguments.
SaveDir=$1
LegendString=$2

# Check if the directory exists
if [[ ! -d "$SaveDir" ]]; then
    echo "Directory $SaveDir does not exist."
    exit 1
fi

# Change to the directory
cd "$SaveDir"

# Create or overwrite the HTML file
outputFile="$LegendString-PLOTc.html"
{
    echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
    echo "<html>"
    echo "<head>"
    echo "<title>$LegendString - Histograms</title>"
    echo '<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">'
    echo "</head>"
    echo "<body>"
    echo "<h1>Histograms for \"$LegendString\"</h1>"

    # Loop write plot info.
    for file in *-HIST.png; do
        if [[ -f "$file" ]]; then
            echo "Histogram for input file <b>${file%.png}.txt</b><br>"
            echo "<img src=\"$file\" width=\"66%\">"
            echo "<hr>"
        fi
    done

    echo "</body>"
    echo "</html>"
} > "$outputFile"
