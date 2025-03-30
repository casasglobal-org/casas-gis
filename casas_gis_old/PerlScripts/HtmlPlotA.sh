#!/bin/bash
# Script that plots raster statistics by ecozones
# using gnuplot and puts .png outputs in a HTML page

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2006 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 19 September 2006

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
outputFile="$LegendString-PLOTa.html"
{
    echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
    echo "<html>"
    echo "<head>"
    echo "<title>$LegendString - Zoned Plots</title>"
    echo '<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">'
    echo "</head>"
    echo "<body>"
    echo "<h1>Barchart statistics for \"$LegendString\"</h1>"

    # Loop to plot data with gnuplot
    # and save them to .png images.
    for file in *.tab; do
        if [[ -f "$file" ]]; then
            baseName="${file%.tab}"
            gnuplot <<EOF
set term png enhanced font "Arial,10" size 640,480
set output "${baseName}-PLOTa.png"
set size 1.5,1.0
set autoscale
set xrange [0.5:18.5]
set tics out
set xtics nomirror 1,1,18
set mxtics 2
set ytics auto
set title "Extent of raster categories by evapotranspiration zones"
set ylabel "Area (km^{2})" offset 0,-4
set xlabel "Evapotranspiration zones"
set key below right width 1 height 0.5 box linewidth 0.5
set boxwidth 0.2 absolute
set style fill pattern border
set grid mxtics ytics linewidth 2
plot "${file}" using (\$1-0.3):(\$2/(10**6)) title "Low" with boxes linetype -1, \
     "${file}" using (\$1-0.1):(\$3/(10**6)) title "Mid-Low" with boxes linetype -1, \
     "${file}" using (\$1+0.1):(\$4/(10**6)) title "Mid-High" with boxes linetype -1, \
     "${file}" using (\$1+0.3):(\$5/(10**6)) title "High" with boxes linetype -1
set output
EOF

            echo "Plot for input file <b>${baseName}.txt</b><br>"
            echo "<img src=\"${baseName}-PLOTa.png\">"
            echo "<hr>"
        fi
    done

    echo "</body>"
    echo "</html>"
} > "$outputFile"
