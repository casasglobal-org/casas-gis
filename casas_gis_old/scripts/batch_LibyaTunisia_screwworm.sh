#!/bin/sh
#
# Batch run screwwrom in Libya-Tunisia
#
# To run it from 64-SVN DOS text, please e
# "%GRASS_SH%" batch_LibyaTunisia_screwworm.sh
#
# Luigi Ponti, 18 June 2012
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

#~ Number of rows is 38.

for i in 12 23 28
do

    ############ Yearly output ############

    #~ # Rain.
    #~ if [ $i -eq 12 ] ; then
        #~ # Set run
        #~ directory="screwworm_rain_1989-2005"
        #~ parameter="$i"
        #~ legend="rain (mm yr-1)"
        #~ # Run GIS routine
        #~ LibyaTunisia -w -g SaveDir="$directory"\
            #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
            #~ interpolation=idw numpoints=7\
            #~ lowercut=0 uppercut=0 legend1="$legend"\
            #~ alt=900 resolution=1 lowBarCol=0.00 upBarCol=1243.40
        #~ wait
    #~ fi

    # Fall winter mortality.
    #~ if [ $i -eq 23 ] ; then
        #~ # Set run
        #~ directory="screwworm_FallWinMort_1989-2005"
        #~ parameter="$i"
        #~ legend="FallWinMort"
        #~ # Run GIS routine
        #~ LibyaTunisia -w -g SaveDir="$directory"\
            #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
            #~ interpolation=idw numpoints=7\
            #~ lowercut=0 uppercut=0 legend1="$legend"\
            #~ alt=900 resolution=1 lowBarCol=6.61 upBarCol=32.44
        #~ wait
    #~ fi

    #~ # Rain index x Pupae.
    #~ if [ $i -eq 28 ] ; then
        #~ # Set run
        #~ directory="screwworm_RIxPup_1989-2005"
        #~ parameter="$i"
        #~ legend="RIxPup" 
        #~ # Run GIS routine
        #~ LibyaTunisia -w -g SaveDir="$directory"\
            #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
            #~ interpolation=idw numpoints=7\
            #~ lowercut=0 uppercut=0 legend1="$legend"\
            #~ alt=900 resolution=1 lowBarCol=0.01 upBarCol=111.39
        #~ wait
    #~ fi

    ############ Avg, Std, CV ############

    #~ # Rain.
    #~ if [ $i -eq 12 ] ; then
        #~ # Set run
        #~ directory="screwworm_rain_summary"
        #~ parameter="$i"
        #~ legend="rain (mm yr-1)"
        #~ # Run GIS routine
        #~ LibyaTunisia -g SaveDir="$directory"\
            #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
            #~ interpolation=idw numpoints=7\
            #~ lowercut=0 uppercut=0 legend1="$legend"\
            #~ alt=900 resolution=1
        #~ wait
        #~ g.copy raster=MskdModPOSrain_Alfalfa_15Jun1Avg,sw_rain_avg
        #~ r.contour input=sw_rain_avg output=sw_rain_iso450 levels=450.0
    #~ fi

    # Fall winter mortality.
    #~ if [ $i -eq 23 ] ; then
        #~ # Set run
        #~ directory="screwworm_FallWinMort_summary"
        #~ parameter="$i"
        #~ legend="FallWinMort"
        #~ # Run GIS routine
        #~ LibyaTunisia -g SaveDir="$directory"\
            #~ longitude=5 latitude=6 year=11 parameter="$parameter"\
            #~ interpolation=idw numpoints=7\
            #~ lowercut=0 uppercut=0 legend1="$legend"\
            #~ alt=900 resolution=1
        #~ wait
        #~ g.copy raster=MskdModPOSFallWinMort_Alfalfa_15Jun1Avg,sw_FallWinMort_avg
        #~ r.contour input=sw_FallWinMort_avg output=sw_FallWinMort_iso10 levels=10.0
    #~ fi

    # Rain index x Pupae.
    if [ $i -eq 28 ] ; then
        # Set run
        directory="screwworm_RIxPup_summary"
        parameter="$i"
        legend="RIxPup" 
        # Run GIS routine
        LibyaTunisia -g SaveDir="$directory"\
            longitude=5 latitude=6 year=11 parameter="$parameter"\
            interpolation=idw numpoints=7\
            lowercut=0 uppercut=0 legend1="$legend"\
            alt=900 resolution=1
        wait
    fi

done
exit 0

