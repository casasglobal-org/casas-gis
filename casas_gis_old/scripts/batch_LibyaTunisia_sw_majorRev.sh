#!/bin/sh
#
# Batch run screwwrom in Libya-Tunisia
#
# To run it from 64-SVN DOS text, please e
# "%GRASS_SH%" batch_LibyaTunisia_sw_majorRev.sh
#
# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2012 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 18 June 2012

#~ The following column names

#~ 1. Model
#~ 2. Date
#~ 3. Time
#~ 4. WxFile
#~ 5. Long
#~ 6. Lat
#~ 7. JdStart
#~ 8. JdEnd
#~ 9. Month
#~ 10. Day
#~ 11. Year
#~ 12. rain
#~ 13. CutDD
#~ 14. Yeardd
#~ 15. Root
#~ 16. Stem/Yr
#~ 17. Leaf/Yr
#~ 18. (St+Lf)/Yr
#~ 19. Tons/Acre/Yr
#~ 20. NrCuts
#~ 21. TempIncr
#~ 22. MortSummer
#~ 23. tcold
#~ 24. EggPerYr
#~ 25. Larvae/Yr
#~ 26. Pupae/Yr
#~ 27. Adlts/Yr
#~ 28. RIxPupae

#~ Number of rows is 38.

for i in 12 22 23 24 25 26 27 28; do

    ############ Yearly output ############

    #~ # Rain
    #~ if [ $i -eq 12 ] ; then
    #~ # Set run
    #~ directory="sw_majorRev_rain_1989-2009"
    #~ parameter="$i"
    #~ legend="rain"
    #~ # Run GIS routine
    #~ LibyaTunisia -w -g save_directory="$directory"\
    #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
    #~ interpolation=idw numpoints=7\
    #~ lowercut=0 uppercut=0 legend1="$legend"\
    #~ alt=900 resolution=1 lowBarCol=0.00 upBarCol=1280
    #~ wait
    #~ fi

    #~ # Mort Summer
    #~ if [ $i -eq 22 ] ; then
    #~ # Set run
    #~ directory="sw_majorRev_MortSummer_1989-2009"
    #~ parameter="$i"
    #~ legend="MortSummer"
    #~ # Run GIS routine
    #~ LibyaTunisia -w -g save_directory="$directory"\
    #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
    #~ interpolation=idw numpoints=7\
    #~ lowercut=0 uppercut=0 legend1="$legend"\
    #~ alt=900 resolution=1 lowBarCol=0.011 upBarCol=3.334
    #~ wait
    #~ fi

    #~ # tcold
    #~ if [ $i -eq 23 ] ; then
    #~ # Set run
    #~ directory="sw_majorRev_tcold_1989-2009"
    #~ parameter="$i"
    #~ legend="tcold"
    #~ # Run GIS routine
    #~ LibyaTunisia -w -g save_directory="$directory"\
    #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
    #~ interpolation=idw numpoints=7\
    #~ lowercut=0 uppercut=0 legend1="$legend"\
    #~ alt=900 resolution=1 lowBarCol=6.384 upBarCol=32.441
    #~ wait
    #~ fi

    #~ # EggPerYr
    #~ if [ $i -eq 24 ] ; then
    #~ # Set run
    #~ directory="sw_majorRev_EggPerYr_1989-2009"
    #~ parameter="$i"
    #~ legend="EggPerYr"
    #~ # Run GIS routine
    #~ LibyaTunisia -w -g save_directory="$directory"\
    #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
    #~ interpolation=idw numpoints=7\
    #~ lowercut=0 uppercut=0 legend1="$legend"\
    #~ alt=900 resolution=1 lowBarCol=13.786 upBarCol=467.974
    #~ wait
    #~ fi

    #~ # LarvaePerYr
    #~ if [ $i -eq 25 ] ; then
    #~ # Set run
    #~ directory="sw_majorRev_LarvaePerYr_1989-2009"
    #~ parameter="$i"
    #~ legend="LarvaePerYr"
    #~ # Run GIS routine
    #~ LibyaTunisia -w -g save_directory="$directory"\
    #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
    #~ interpolation=idw numpoints=7\
    #~ lowercut=0 uppercut=0 legend1="$legend"\
    #~ alt=900 resolution=1 lowBarCol=6.183 upBarCol=339.366
    #~ wait
    #~ fi

    #~ # PuapePerYr
    #~ if [ $i -eq 26 ] ; then
    #~ # Set run
    #~ directory="sw_majorRev_PuapePerYr_1989-2009"
    #~ parameter="$i"
    #~ legend="PuapePerYr"
    #~ # Run GIS routine
    #~ LibyaTunisia -w -g save_directory="$directory"\
    #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
    #~ interpolation=idw numpoints=7\
    #~ lowercut=0 uppercut=0 legend1="$legend"\
    #~ alt=900 resolution=1 lowBarCol=4.551 upBarCol=249.767
    #~ wait
    #~ fi

    #~ # AdultsPerYr
    #~ if [ $i -eq 27 ] ; then
    #~ # Set run
    #~ directory="sw_majorRev_AdultsPerYr_1989-2009"
    #~ parameter="$i"
    #~ legend="AdultsPerYr"
    #~ # Run GIS routine
    #~ LibyaTunisia -w -g save_directory="$directory"\
    #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
    #~ interpolation=idw numpoints=7\
    #~ lowercut=0 uppercut=0 legend1="$legend"\
    #~ alt=900 resolution=1 lowBarCol=2.721 upBarCol=227.218
    #~ wait
    #~ fi

    #~ # RIxPupae
    #~ if [ $i -eq 28 ] ; then
    #~ # Set run
    #~ directory="sw_majorRev_RIxPupae_1989-2009"
    #~ parameter="$i"
    #~ legend="RIxPupae"
    #~ # Run GIS routine
    #~ LibyaTunisia -w -g save_directory="$directory"\
    #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
    #~ interpolation=idw numpoints=7\
    #~ lowercut=0 uppercut=0 legend1="$legend"\
    #~ alt=900 resolution=1 lowBarCol=0.02 upBarCol=158.419
    #~ wait
    #~ fi

    ############ Avg, Std, CV ############

    #~ # Rain
    #~ if [ $i -eq 12 ] ; then
    #~ # Set run
    #~ directory="sw_majorRev_rain_AvgStdCV"
    #~ parameter="$i"
    #~ legend="rain"
    #~ # Run GIS routine
    #~ LibyaTunisia -g save_directory="$directory"\
    #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
    #~ interpolation=idw numpoints=7\
    #~ lowercut=0 uppercut=0 legend1="$legend"\
    #~ alt=900 resolution=1 lowBarCol=0.00 upBarCol=1280
    #~ wait
    #~ fi

    #~ # Mort Summer
    #~ if [ $i -eq 22 ] ; then
    #~ # Set run
    #~ directory="sw_majorRev_MortSummer_AvgStdCV"
    #~ parameter="$i"
    #~ legend="MortSummer"
    #~ # Run GIS routine
    #~ LibyaTunisia -g save_directory="$directory"\
    #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
    #~ interpolation=idw numpoints=7\
    #~ lowercut=0 uppercut=0 legend1="$legend"\
    #~ alt=900 resolution=1 lowBarCol=0.011 upBarCol=3.334
    #~ wait
    #~ fi

    #~ # tcold
    #~ if [ $i -eq 23 ] ; then
    #~ # Set run
    #~ directory="sw_majorRev_tcold_AvgStdCV"
    #~ parameter="$i"
    #~ legend="tcold"
    #~ # Run GIS routine
    #~ LibyaTunisia -g save_directory="$directory"\
    #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
    #~ interpolation=idw numpoints=7\
    #~ lowercut=0 uppercut=0 legend1="$legend"\
    #~ alt=900 resolution=1 lowBarCol=6.384 upBarCol=32.441
    #~ wait
    #~ fi

    #~ # EggPerYr
    #~ if [ $i -eq 24 ] ; then
    #~ # Set run
    #~ directory="sw_majorRev_EggPerYr_AvgStdCV"
    #~ parameter="$i"
    #~ legend="EggPerYr"
    #~ # Run GIS routine
    #~ LibyaTunisia -g save_directory="$directory"\
    #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
    #~ interpolation=idw numpoints=7\
    #~ lowercut=0 uppercut=0 legend1="$legend"\
    #~ alt=900 resolution=1 lowBarCol=13.786 upBarCol=467.974
    #~ wait
    #~ fi

    # LarvaePerYr
    if [ $i -eq 25 ]; then
        # Set run
        directory="sw_majorRev_LarvaePerYr_AvgStdCV"
        parameter="$i"
        legend="LarvaePerYr"
        # Run GIS routine
        LibyaTunisia -g save_directory="$directory" \
            longitude=5 latitude=6 year=11 parameter="$parameter" \
            interpolation=idw numpoints=7 lowercut=0 uppercut=0 legend1="$legend" \
            alt=900 resolution=1 lowBarCol=6.183 upBarCol=339.366
        wait
    fi

    # PuapePerYr
    if [ $i -eq 26 ]; then
        # Set run
        directory="sw_majorRev_PuapePerYr_AvgStdCV"
        parameter="$i"
        legend="PuapePerYr"
        # Run GIS routine
        LibyaTunisia -g save_directory="$directory" \
            longitude=5 latitude=6 year=11 parameter="$parameter" \
            interpolation=idw numpoints=7 lowercut=0 uppercut=0 legend1="$legend" \
            alt=900 resolution=1 lowBarCol=4.551 upBarCol=249.767
        wait
    fi

    # AdultsPerYr
    if [ $i -eq 27 ]; then
        # Set run
        directory="sw_majorRev_AdultsPerYr_AvgStdCV"
        parameter="$i"
        legend="AdultsPerYr"
        # Run GIS routine
        LibyaTunisia -g save_directory="$directory" \
            longitude=5 latitude=6 year=11 parameter="$parameter" \
            interpolation=idw numpoints=7 lowercut=0 uppercut=0 legend1="$legend" \
            alt=900 resolution=1 lowBarCol=2.721 upBarCol=227.218
        wait
    fi

    # RIxPupae
    if [ $i -eq 28 ]; then
        # Set run
        directory="sw_majorRev_RIxPupae_AvgStdCV"
        parameter="$i"
        legend="RIxPupae"
        # Run GIS routine
        LibyaTunisia -g save_directory="$directory" \
            longitude=5 latitude=6 year=11 parameter="$parameter" \
            interpolation=idw numpoints=7 lowercut=0 uppercut=0 legend1="$legend" \
            alt=900 resolution=1 lowBarCol=0.02 upBarCol=158.419
        wait
    fi

done
exit 0
