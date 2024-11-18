#!/bin/sh
#
# Get boxplot stats from raster map
#
# Need to set GRASS vars for appropriate location
#
# To run it from 64-SVN DOS text, please (currently does not work)
# "%GRASS_SH%" get_boxplot_stats.sh RasterName LocationName MapsetName DivergentRule IsPercentScale
#
# First do:
# cd C:/cygwin/home/andy/
#
# Then launch e.g.:
# "C:/cygwin/home/andy/get_boxplot_stats.sh" tomato_YieldPerHectare_175_above_0 AEA_Med luigi divNo 0
#
# It expects (and colls) Perl script getBoxplotColorRule.pl
# to be in the same directory
#
# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2013 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 11 October 2013

#~ cotton_harea_175crops2000_india
#~ cotton_area_irrig_fraction_M3
#~ cotton_area_rainf_fraction_M3
#~ cotton_yield_175crops2000_india_clip_harea

export HOME="C:/cygwin/home/andy/"

RasterMapName="$1"
locationname="$2"
mapsetname="$3"
divrule="$4" # i.e. divYes or divNo
percent="$5" # i.e. 0 or 1 (is the var in % scale?)

# Set location and mapset
g.mapset mapset=$mapsetname location=$locationname

# Stats for boxplot from raster data.
echo "# Raster statistics for raster $RasterMapName #" | tee ~/${RasterMapName}"_stats.txt"
echo "" | tee -a ~/${RasterMapName}"_stats.txt"
r.univar -e map=$RasterMapName output=~/${RasterMapName}"_stats.txt"
echo "" | tee -a ~/${RasterMapName}"_stats.txt"

# Get univariate statistics from rater map
eval $(r.univar -g -e map="$RasterMapName")
abs_min=$min
abs_max=$max

# Write header of boxplot stats file
echo "# Whiskers for a boxplot based on raster $RasterMapName #" | tee -a ~/${RasterMapName}"_stats.txt"
eval $(r.univar -g -e map="$RasterMapName")

# R boxplot
# https://www.r-bloggers.com/whisker-of-boxplot/

# Tentative position of lower whisker
# lower whisker = max(min(x), Q_1 – 1.5 * IQR)
iqr_low=$(perl -E "say "$first_quartile" - (1.5 * ("$third_quartile" - "$first_quartile"))")

# Tentative position of higher whisker
# upper whisker = min(max(x), Q_3 + 1.5 * IQR)
iqr_high=$(perl -E "say "$third_quartile" + (1.5 * ("$third_quartile" - "$first_quartile"))")

# If there is no outliers (data beyond iqr_low)
# lower whisker is absolute minimum
# lower whisker = max(min(x), Q_1 – 1.5 * IQR)
whisker_low=$(perl -E "use List::Util qw( min max ); my @numbers = ($abs_min, $iqr_low); say max(@numbers)")
echo $whisker_low

# If there is no outliers (data beyond iqr_high)
# higher whisker is absolute maximum
# upper whisker = min(max(x), Q_3 + 1.5 * IQR)
whisker_high=$(perl -E "use List::Util qw( min max ); my @numbers = ($abs_max, $iqr_high); say min(@numbers)")
echo $whisker_high

# Write more stuff on boxplot stats file
echo "" | tee -a ~/${RasterMapName}"_stats.txt"
echo "Ends of whiskers are $whisker_low and $whisker_high" | tee -a ~/${RasterMapName}"_stats.txt"
echo "" | tee -a ~/${RasterMapName}"_stats.txt"

echo "# Raster info #" | tee -a ~/${RasterMapName}"_stats.txt"
r.info map=$RasterMapName >> ~/${RasterMapName}"_stats.txt"
echo "" | tee -a ~/${RasterMapName}"_stats.txt"

# Write GRASS GIS color rule based on box plot stats
# using external Perl script
perl ../PerlScripts/getBoxplotColorRule.pl "$whisker_low" "$whisker_high" "$abs_min" "$abs_max" "$divrule" "$percent" "$RasterMapName" >&test.log

exit 0
