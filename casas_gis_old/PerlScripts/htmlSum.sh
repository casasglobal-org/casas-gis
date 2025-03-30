#!/bin/bash
# Script that writes a HTML visual summary for CASAS models

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2006 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 16 April 2006

# Read Directory where maps are saved and
# other parameters from script arguments.
SaveDir=$1
LegendString=$2
MapPar=$3
LowerCut=$4
UpperCut=$5
AltClip=$6
SurfCut=$7
EtoClip=$8
Plots=$9

# Check if the directory exists
if [[ ! -d "$SaveDir" ]]; then
    echo "Directory $SaveDir does not exist."
    exit 1
fi

# Change to the directory
cd "$SaveDir"

# Create or overwrite the HTML file
outputFile="$LegendString.html"
{
    echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
    echo "<html>"
    echo "<head>"
    echo "<title>$LegendString - Visual Summary</title>"
    echo '<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">'
    echo "</head>"
    echo "<body>"
    echo "<h1>Report for \"$LegendString\"</h1>"
    echo "<h2>Output maps</h2>"

    # Read map names, write them to HTML file,
    # and create links to stat reports.
    for file in *.png; do
        if [[ "$file" != *PLOT* && "$file" != *HIST* ]]; then
            baseName="${file%.png}"
            echo "<a href=\"$baseName.txt\"><img src=\"$file\" width=\"32%\"></a>"
        fi
    done

    echo "<p><i>Please, click on images to see stat report.</i></p>"

    # Print a link to page with barchart plots.
    if [[ -n "$Plots" ]]; then
        echo "<p><i>You may also see raster statistics as barcharts"
        echo " (<a href=\"$LegendString-PLOTa.html\" target=\"_blank\">zoned</a>"
        echo " and <a href=\"$LegendString-PLOTb.html\" target=\"_blank\">overall</a>)"
        echo " and as cell frequency <a href=\"$LegendString-PLOTc.html\" target=\"_blank\">histogram</a>.</i></p>"
    fi

    # Print some other useful stuff.
    echo "<h2>Mapping parameters</h2>"
    echo "<ul>"
    echo "<li>Parameter mapped: $MapPar"
    echo "<li>Lower cutting point: $LowerCut"
    echo "<li>Upper cutting point: $UpperCut"
    echo "<li>Region clip: $EtoClip"
    echo "<li>Altitude clip: $AltClip m"
    echo "<li>Stations above altitude clip were used to interpolate: $SurfCut"
    echo "</ul>"

    # Append log with input files.
    echo "<h2>Input file log</h2>"
    if [[ -f "$LegendString.log" ]]; then
        while IFS= read -r line; do
            if [[ "$line" =~ " " ]]; then
                echo "$line<br>"
            else
                echo "<ul>"
                echo "<li>$line</li>"
                echo "</ul>"
            fi
        done < "$LegendString.log"
    fi

    echo "</body>"
    echo "</html>"
} > "$outputFile"
