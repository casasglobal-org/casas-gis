#!/bin/sh

# Batch run EurMedGrape CASAS GIS
#
# OLD:
#  To run it from 64-SVN DOS text, please enter
#  "%GRASS_SH%" batch_oliveProtheusWin.sh
# NEW:
#  grass84 $HOME/data/casas/grass8data_casas/latlong/luigi/ --exec $HOME/software/casas-gis/casas_gis_old/scripts/batch_OliveProtheus.sh
#
# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2010 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 17 March 2010
############

# fail on error
set -e

export PATH="$PATH:$HOME/software/casas-gis/casas_gis_old/casas/grass_scripts/"

# Check for user break (signal list: trap -l)
trap 'exitprocedure' 1 2 3 15
# Ensure that we are in a GRASS session
if test "$GISBASE" = ""; then
    echo 'You must be in GRASS GIS to run this program.' >&2
    exit 1
fi

# 1. Model
# 2. Date
# 3. Time
# 4. WxFile
# 5. Long
# 6. Lat
# 7. JdStart
# 8. JdEnd
# 9. Month
# 10. Day
# 11. Year
# 12. rain
# 13. CutDD
# 14. Yeardd
# 15. Root
# 16. Stem_Yr
# 17. Leaf_Yr
# 18. St+Lf_Yr
# 19. Tons_Acre_Yr
# 20. NrCuts
# 21. TempIncr
# 22. GisYears
# 23. MortSummer
# 24. tcold
# 25. EggPerYr
# 26. Larvae_Yr
# 27. Pupae_Yr
# 28. Adlts_Yr
# 29. RIxPupae

# Number of rows is 15844.

for i in 27; do

    : << 'COMMENT'

	# Pupae per year
    if [ $i -eq 27 ] ; then
        # Set run
        directory="swd_eu_outliers_spline_005"
        parameter="$i"
        legend="pupae per year"
        # Run GIS routine
		EurMedGrape -w -r -p \
            save_directory="$directory" \
			longitude=5 latitude=6 year=11 parameter="$parameter" \
			interpolation=bspline lowercut=0 uppercut=0 \
            legend1="$legend" \
			region=-1 \
            alt=2000 resolution=1 \
			lowBarCol=0 \
			upBarCol=1295.219
        wait
    fi

COMMENT

    # : <<'COMMENT'

    # Pupae per year Stdv Coef
    if [ $i -eq 27 ]; then
        # Set run
        directory="swd_eu_outliers_spline_Stdv_Coef"
        parameter="$i"
        parameter="$i"
        legend="pupae per year"
        # Run GIS routine
        EurMedGrape -r -p \
            save_directory="$directory" \
            longitude=5 latitude=6 year=11 parameter="$parameter" \
            interpolation=bspline lowercut=0 uppercut=0 \
            legend1="$legend" \
            region=-1 \
            alt=2000 resolution=1
        wait
    fi

    # COMMENT

done
exit 0
