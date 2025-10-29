#!/bin/bash
#
# Batch run mediterraneo CASAS GIS
#
# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2009 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 10 July 2009
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

#~ 12. dd
#~ 13. ddbZero
#~ 14. FruWgt
#~ 15. fruNum
#~ 16. Bloomday
#~ 17. BloomYr
#~ 18. DDBSum
#~ 19. ChillHD
#~ 20. PrcpYrSum
#~ 21. TempIncr
#~ 22. OFEgDays
#~ 23. OFLrDays
#~ 24. OFPuDays
#~ 25. OFAdDays
#~ 26. OfPupSum
#~ 27. DamFrSum
#~ 28. PrcntAtkd

for i in 12 14 16 17 22 23 24 25 26 28; do
    #~ # Day degrees
    #~ if [ $i -eq 12 ] ; then
    #~ # Set run
    #~ directory="DayDegrees"
    #~ parameter="$i"
    #~ legend="Day degrees"
    #~ # Run GIS routine
    #~ mediterraneo -c save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" lowercut=1 uppercut=0 region=NA alt=700 resolution=2\
    #~ legend1="$legend"
    #~ wait
    #~ fi
    #~ # Fruit weight
    #~ if [ $i -eq 14 ] ; then
    #~ # Set run
    #~ directory="FruitWeight"
    #~ parameter="$i"
    #~ legend="Fruit weight"
    #~ # Run GIS routine
    #~ mediterraneo -c save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" lowercut=1 uppercut=0 region=NA alt=700 resolution=2\
    #~ legend1="$legend"
    #~ wait
    #~ fi
    #~ # Bloom date
    #~ if [ $i -eq 16 ] ; then
    #~ # Set run
    #~ directory="BloomDate"
    #~ parameter="$i"
    #~ legend="Bloom date"
    #~ # Run GIS routine
    #~ mediterraneo -c save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" lowercut=1 uppercut=0 region=NA alt=700 resolution=2\
    #~ legend1="$legend"
    #~ wait
    #~ fi
    #~ # Years of blooming
    #~ if [ $i -eq 17 ] ; then
    #~ # Set run
    #~ directory="BloomYears"
    #~ parameter="$i"
    #~ legend="Years with bloom"
    #~ # Run GIS routine
    #~ mediterraneoBloomYears -c save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" lowercut=0 uppercut=0 region=NA alt=700 resolution=2\
    #~ legend1="$legend"
    #~ wait
    #~ fi
    # OF egg days
    #~ if [ $i -eq 22 ] ; then
    #~ # Set run
    #~ directory="OFeggDays"
    #~ parameter="$i"
    #~ legend="OF egg days"
    #~ # Run GIS routine
    #~ mediterraneo -c save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" lowercut=1 uppercut=0 region=NA alt=700 resolution=2\
    #~ legend1="$legend"
    #~ wait
    #~ fi
    #~ # OF larvae days
    #~ if [ $i -eq 23 ] ; then
    #~ # Set run
    #~ directory="OFlarvaeDays"
    #~ parameter="$i"
    #~ legend="OF larvae days"
    #~ # Run GIS routine
    #~ mediterraneo -c save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" lowercut=1 uppercut=0 region=NA alt=700 resolution=2\
    #~ legend1="$legend"
    #~ wait
    #~ fi
    #~ # OF pupae days
    #~ if [ $i -eq 24 ] ; then
    #~ # Set run
    #~ directory="OFpupaeDays"
    #~ parameter="$i"
    #~ legend="OF pupae days"
    #~ # Run GIS routine
    #~ mediterraneo -c save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" lowercut=1 uppercut=0 region=NA alt=700 resolution=2\
    #~ legend1="$legend"
    #~ wait
    #~ fi
    #~ # OF adult days
    #~ if [ $i -eq 25 ] ; then
    #~ # Set run
    #~ directory="OFadultDays"
    #~ parameter="$i"
    #~ legend="OF adult days"
    #~ # Run GIS routine
    #~ mediterraneo -c save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" lowercut=1 uppercut=0 region=NA alt=700 resolution=2\
    #~ legend1="$legend"
    #~ wait
    #~ fi
    # OF pupae CumSum
    #~ if [ $i -eq 26 ] ; then
    #~ # Set run
    #~ directory="OFpupaeCumSum_AvgOnly"
    #~ parameter="$i"
    #~ legend="OF pupae CumSum"
    #~ # Run GIS routine
    #~ mediterraneo -c save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" lowercut=1 uppercut=0 region=NA alt=700 resolution=2\
    #~ legend1="$legend"
    #~ wait
    #~ fi
    # Percent fruit attacked
    if [ $i -eq 28 ]; then
        # Set run
        directory="PercentFruitAttacked_AvgOnly"
        parameter="$i"
        legend="Percent fruit attacked"
        # Run GIS routine
        mediterraneo -c save_directory="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" lowercut=1 uppercut=0 region=NA alt=700 resolution=2 legend1="$legend"
        wait
    fi
done
exit 0
