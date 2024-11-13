#!/bin/sh
#
# Batch run medPresentClimate CASAS GIS
#
# To run it from 64-SVN DOS text, please e
# "%GRASS_SH%" batch_oliveProtheusWin.sh
#
# Luigi Ponti, 17 November 2011
#

#~ The following column names were found:

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
#~ 22. SummerMort
#~ 23. FallWinMort
#~ 24. CmSwegg
#~ 25. CmSwLarvae
#~ 26. CmSwPupae
#~ 27. CmSwadlt
#~ 28. RIxPup

#~ Number of rows is 201.

for i in 12 23 26 28 29 30 31 32 33 34; do

    #~ # Rain.
    #~ if [ $i -eq 12 ] ; then
    #~ # Set run
    #~ directory="sworm_AnnualRain"
    #~ parameter="$i"
    #~ legend="rain (mm/year)"
    #~ # Run GIS routine
    #~ usa states='AL AZ CA FL GA LA MS MX NC NM SC TX'\
    #~ SaveDir="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" lowercut=0 uppercut=10000\
    #~ legend1="$legend"\
    #~ alt=10000 resolution=1
    #~ wait
    #~ fi

    #~ # Fall winter mortality.
    #~ if [ $i -eq 23 ] ; then
    #~ # Set run
    #~ directory="sworm_FallWinterMortality"
    #~ parameter="$i"
    #~ legend="screwworm fall winter mortality"
    #~ # Run GIS routine
    #~ usa states='AL AZ CA FL GA LA MS MX NC NM SC TX'\
    #~ SaveDir="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" lowercut=0 uppercut=10000\
    #~ legend1="$legend"\
    #~ alt=10000 resolution=1
    #~ wait
    #~ fi

    #~ # Cumulative pupae.
    #~ if [ $i -eq 26 ] ; then
    #~ # Set run
    #~ directory="sworm_CumPupae"
    #~ parameter="$i"
    #~ legend="screwworm cumulative pupae"
    #~ # Run GIS routine
    #~ usa states='AL AZ CA FL GA LA MS MX NC NM SC TX'\
    #~ SaveDir="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" lowercut=0 uppercut=10000\
    #~ legend1="$legend"\
    #~ alt=10000 resolution=1
    #~ wait
    #~ fi

    # Cumulative pupae Texas.
    if [ $i -eq 12 ]; then
        # Set run
        directory="sworm_rain_Texas_singleLegend"
        parameter="$i"
        legend="rain"
        # Run GIS routine
        usa -w states='TX' \
            SaveDir="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" \
            interpolation="idw" numpoints=3 lowercut=0 uppercut=2000 legend1="$legend" \
            alt=2000 resolution=2 lowBarCol=0.00 upBarCol=2549.70
        wait
    fi

    #~ # Rain index.
    #~ if [ $i -eq 28 ] ; then
    #~ # Set run
    #~ directory="sworm_rainIndex"
    #~ parameter="$i"
    #~ legend="screwworm rain index"
    #~ # Run GIS routine
    #~ usa states='AL AZ CA FL GA LA MS MX NC NM SC TX'\
    #~ SaveDir="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" lowercut=0 uppercut=10000\
    #~ legend1="$legend"\
    #~ alt=10000 resolution=1
    #~ wait
    #~ fi

    #~ # Screwworm index.
    #~ if [ $i -eq 30 ] ; then
    #~ # Set run
    #~ directory="sworm_pupaeRainIndex"
    #~ parameter="$i"
    #~ legend="screwworm favorability"
    #~ # Run GIS routine
    #~ usa states='AL AZ CA FL GA LA MS MX NC NM SC TX'\
    #~ SaveDir="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" lowercut=0 uppercut=10000\
    #~ legend1="$legend"\
    #~ alt=10000 resolution=1
    #~ wait
    #~ fi

    #~ # Survival index.
    #~ if [ $i -eq 31 ] ; then
    #~ # Set run
    #~ directory="sworm_survivalIndex"
    #~ parameter="$i"
    #~ legend="screwworm survival index"
    #~ # Run GIS routine
    #~ usa states='AL AZ CA FL GA LA MS MX NC NM SC TX'\
    #~ SaveDir="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" lowercut=0 uppercut=10000\
    #~ legend1="$legend"\
    #~ alt=10000 resolution=1
    #~ wait
    #~ fi

    #~ # Rain cold index.
    #~ if [ $i -eq 32 ] ; then
    #~ # Set run
    #~ directory="sworm_rainColdIndex"
    #~ parameter="$i"
    #~ legend="screwworm rain cold index"
    #~ # Run GIS routine
    #~ usa states='AL AZ CA FL GA LA MS MX NC NM SC TX'\
    #~ SaveDir="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" lowercut=0 uppercut=0\
    #~ legend1="$legend"\
    #~ alt=10000 resolution=1
    #~ wait
    #~ fi

    #~ # Surviving pupae based on rain limits only.
    #~ if [ $i -eq 33 ] ; then
    #~ # Set run
    #~ directory="sworm_survPupae_rainOnly"
    #~ parameter="$i"
    #~ legend="Surviving pupae (limiting rain only)"
    #~ # Run GIS routine
    #~ usa states='AL AZ CA FL GA LA MS MX NC NM SC TX'\
    #~ SaveDir="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" lowercut=0 uppercut=0\
    #~ legend1="$legend"\
    #~ alt=10000 resolution=1
    #~ wait
    #~ fi

    #~ # Surviving pupae based on rain and cold limits.
    #~ if [ $i -eq 33 ] ; then
    #~ # Set run
    #~ directory="sworm_survivingPupae"
    #~ parameter="$i"
    #~ legend="Surviving pupae"
    #~ # Run GIS routine
    #~ usa states='AL AZ CA FL GA LA MS MX NC NM SC TX'\
    #~ SaveDir="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" lowercut=0 uppercut=0\
    #~ legend1="$legend"\
    #~ alt=10000 resolution=1
    #~ wait
    #~ fi

done
exit 0
