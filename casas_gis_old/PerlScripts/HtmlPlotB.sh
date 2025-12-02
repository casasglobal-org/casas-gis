#!/bin/bash
# Script that plots overall raster statistics
# using gnuplot and puts .png outputs in a HTML page

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2006 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 20 September 2006

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
outputFile="$LegendString-PLOTb.html"
{
    echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
    echo "<html>"
    echo "<head>"
    echo "<title>$LegendString - Total Plots</title>"
    echo '<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">'
    echo "</head>"
    echo "<body>"
    echo "<h1>Barchart statistics for \"$LegendString\"</h1>"

    # Loop to plot data with gnuplot
    # and save them to .png images.
    for file in *.tabTot; do
        if [[ -f "$file" ]]; then
            baseName="${file%.tabTot}"
            gnuplot <<EOF
set term png enhanced font "Arial,10" size 640,480
set output "${baseName}-PLOTb.png"
set autoscale
set xrange [0:5]
set tics out
set xtics nomirror rotate by 90 ("Low" 1, "Mid-low" 2, "Mid-high" 3, "High" 4)
set ytics nomirror
set title "Extent of raster categories"
set ylabel "Area (km^{2})" offset 0,-3
unset key
set boxwidth 0.5 absolute
set style fill solid 0.5 border
plot "${file}" using (\$1*1):(\$2/(10**6)) title "Low" with boxes linetype -1, \
     "${file}" using (\$1*2):(\$3/(10**6)) title "Mid-Low" with boxes linetype -1, \
     "${file}" using (\$1*3):(\$4/(10**6)) title "Mid-High" with boxes linetype -1, \
     "${file}" using (\$1*4):(\$5/(10**6)) title "High" with boxes linetype -1
set output
EOF

            echo "Plot for input file <b>${baseName}.txt</b><br>"
            echo "<img src=\"${baseName}-PLOTb.png\">"
            echo "<hr>"
        fi
    done

    echo "</body>"
    echo "</html>"
} > "$outputFile"
