#!/bin/bash
#
# Batch run medPresentClimate CASAS GIS
#
# To run it from 64-SVN DOS text, please e
# "%GRASS_SH%" batch_oliveProtheusWin.sh
#
# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2010 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 17 March 2010

#~ No fly:

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
#~ 22. ddbMinus10
#~ 23. ddbMinus83

#~ With fly:

#~ 24. OFEgDays
#~ 25. OFLrDays
#~ 26. OFPuDays
#~ 27. OFAdDays
#~ 28. OfPupSum
#~ 29. DamFrSum
#~ 30. PrcntAtkd

for i in 12 13 14 16 17 18 20 22 23 24 25 28 30; do
    #~ # Day degrees
    #~ if [ $i -eq 12 ] ; then
    #~ # Set run
    #~ directory="DayDegrees"
    #~ parameter="$i"
    #~ legend="Day degrees"
    #~ # Run GIS routine
    #~ medPresentClimate -c -p save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" lowercut=0 uppercut=0 region='21 22 23 25 31 32 33 35' alt=700 resolution=1\
    #~ legend1="$legend"
    #~ wait
    #~ fi

    #~ # Day degrees below zero
    #~ if [ $i -eq 13 ] ; then
    #~ # Set run
    #~ directory="ddBelowZeroNoClip_lowercut30"
    #~ parameter="$i"
    #~ legend="day degrees below zero"
    #~ # Run GIS routine
    #~ medPresentClimate -c -p save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" interpolation="idw" lowercut=30 uppercut=0 region=-1 alt=10000 resolution=1\
    #~ legend1="$legend"
    #~ # color_rule_divergent=4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0
    #~ # This color is Panoply with white in the middle (divergent)
    #~ wait
    #~ fi

    #~ # Fruit weight
    #~ if [ $i -eq 14 ] ; then
    #~ # Set run
    #~ directory="majorRev_FruitWeight_EH5OM_A1B_yearly"
    #~ parameter="$i"
    #~ legend="Fruit weight"
    #~ # Run GIS routine
    #~ medPresentClimate -c -p -m save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" interpolation="idw" lowercut=1 uppercut=0 region=-1 alt=900 resolution=1\
    #~ legend1="$legend"
    #~ wait
    #~ fi

    #~ # Bloom date
    #~ if [ $i -eq 16 ] ; then
    #~ # Set run
    #~ directory="majorRev_BloomDate"
    #~ parameter="$i"
    #~ legend="Bloom date"
    #~ # Run GIS routine
    #~ medPresentClimate -c -p -m save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" interpolation="idw" lowercut=1 uppercut=0 region=-1 alt=900 resolution=1\
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
    #~ medPresentClimate -c -p -m save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" interpolation="idw" lowercut=0 uppercut=0 region=-1 alt=900 resolution=1\
    #~ legend1="$legend"
    #~ wait
    #~ fi

    #~ # Total day degrees below 9.1
    #~ if [ $i -eq 18 ] ; then
    #~ # Set run
    #~ directory="DDBSum"
    #~ parameter="$i"
    #~ legend="day degrees below 9.1"
    #~ # Run GIS routine
    #~ medPresentClimate -c -p save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" lowercut=0 uppercut=0 region='21 22 23 25 31 32 33 35' alt=900 resolution=1\
    #~ legend1="$legend" # color_rule_divergent=4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0
    #~ # This color is Panoply with white in the middle (divergent)
    #~ wait
    #~ fi

    #~ # Total yearly rainfall
    #~ if [ $i -eq 20 ] ; then
    #~ # Set run
    #~ directory="Prcp_h5jetModified2_idw_OliveAreaOnly"
    #~ parameter="$i"
    #~ legend="mm rainfall per year"
    #~ # Run GIS routine
    #~ medPresentClimate -c -p -m save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" interpolation="idw" lowercut=0 uppercut=0 region=-1 alt=10000 resolution=1\
    #~ legend1="$legend"
    #~ wait
    #~ fi

    #~ # ddBelow -10 °C only with a recent run of olive plant.
    #~ if [ $i -eq 22 ] ; then
    #~ # Set run
    #~ directory="ddbMinus10"
    #~ parameter="$i"
    #~ legend="Day degrees below -10"
    #~ # Run GIS routine
    #~ medPresentClimate -c -p save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" interpolation="idw" lowercut=1 uppercut=0 region='21 22 23 25 31 32 33 35' alt=10000 resolution=1\
    #~ legend1="$legend"
    #~ wait
    #~ fi

    #~ # ddBelow -8.3 °C only with a recent run of olive plant.
    #~ if [ $i -eq 23 ] ; then
    #~ # Set run
    #~ directory="ddbMinus83_h5jetModified2"
    #~ parameter="$i"
    #~ legend="Day degrees below -8.3"
    #~ # Run GIS routine
    #~ medPresentClimate -c -p save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" interpolation="idw" lowercut=1 uppercut=0 region=-1 alt=10000 resolution=1\
    #~ legend1="$legend"
    #~ wait
    #~ fi

    ####################
    ### Change input file here! ###
    ##################

    # OF egg days
    #~ if [ $i -eq 22 ] ; then
    #~ # Set run
    #~ directory="OFeggDays"
    #~ parameter="$i"
    #~ legend="OF egg days"
    #~ # Run GIS routine
    #~ medPresentClimate -c -p save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" lowercut=1 uppercut=0 region='21 22 23 25 31 32 33 35' alt=700 resolution=1\
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
    #~ medPresentClimate -c -p save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" lowercut=0 uppercut=0 region='21 22 23 25 31 32 33 35' alt=700 resolution=1\
    #~ legend1="$legend"
    #~ wait
    #~ fi
    #~ # OF pupae days
    #~ if [ $i -eq 24 ] ; then
    #~ # Set run
    #~ directory="OFpupaeDays_OceanColor"
    #~ parameter="$i"
    #~ legend="OF pupae days"
    #~ # Run GIS routine
    #~ medPresentClimate -c -p -m save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" lowercut=0 uppercut=0 region=-1 alt=700 resolution=1\
    #~ legend1="$legend"
    #~ fi
    #~ # OF adult days
    #~ if [ $i -eq 25 ] ; then
    #~ # Set run
    #~ directory="OFadultDays"
    #~ parameter="$i"
    #~ legend="OF adult days"
    #~ # Run GIS routine
    #~ medPresentClimate -c -p save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" lowercut=1 uppercut=0 region='21 22 23 25 31 32 33 35' alt=700 resolution=1\
    #~ legend1="$legend"
    #~ wait
    #~ fi

    # OF pupae CumSum
    if [ $i -eq 28 ]; then
        # Set run
        directory="majorRevision_OFpupaeCumSum"
        parameter="$i"
        legend="OF pupae CumSum"
        # Run GIS routine
        medPresentClimate -c -p -m save_directory="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" interpolation="idw" lowercut=0 uppercut=0 region=-1 alt=900 resolution=1 legend1="$legend"
    fi

    #~ # Percent fruit attacked
    #~ if [ $i -eq 30 ] ; then
    #~ # Set run
    #~ directory="SD_PercentFruitAttacked_h5jetModified2"
    #~ parameter="$i"
    #~ legend="Percent fruit attacked"
    #~ # Run GIS routine
    #~ medPresentClimate -c -p -m save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" interpolation="idw" lowercut=1 uppercut=0 region=-1 alt=900 resolution=1\
    #~ legend1="$legend"
    #~ fi

done
exit 0
