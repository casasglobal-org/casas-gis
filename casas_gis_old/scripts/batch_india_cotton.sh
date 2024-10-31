#!/bin/sh
#
# Batch run india cotton CASAS GIS
#
# To run it from 64-SVN DOS text, please e
# "%GRASS_SH%" batch_india_cotton.sh
#
# Luigi Ponti, 7 October 2013
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
#~ 12. dd
#~ 13. totrain
#~ 14. avg_bales
#~ 15. CVbales
#~ 16. std_bales
#~ 17. kg_ha
#~ 18. revenues
#~ 19. W_VarCost
#~ 20. w_Bt

#~ Number of rows is 2837.


for i in 17
do

    #~ # kg/ha
    #~ if [ $i -eq 17 ] ; then
        #~ # Set run
        #~ directory="india_test_cotton_yield_full_area"
        #~ parameter="$i"
        #~ legend="kg per ha (full cotton area)"
        #~ # Run GIS routine
        #~ india -c -r \
        #~ states=India \
        #~ clip=cotton_full \
        #~ SaveDir="$directory" \
        #~ longitude=5 latitude=6 year=11 \
        #~ parameter="$parameter" \
        #~ interpolation="bspline" \
        #~ numpoints=3 pow=2.0 spline_step_east=57000 spline_step_north=57000 tykhonov_reg=0.05 \
        #~ lowercut=0 uppercut=0 \
        #~ legend1="$legend" \
        #~ alt=2000 resolution=1
        #~ wait
    #~ fi

    if [ $i -eq 17 ] ; then
        # Set run
        directory="india_test_cotton_yield_irrigated_area"
        parameter="$i"
        legend="kg per ha (irrigated cotton area)"
        # Run GIS routine
        india -c -r \
        states=India \
        clip="cotton_irrig" \
        SaveDir="$directory" \
        longitude=5 latitude=6 year=11 \
        parameter="$parameter" \
        interpolation="bspline" \
        numpoints=3 pow=2.0 spline_step_east=57000 spline_step_north=57000 tykhonov_reg=0.05 \
        lowercut=0 uppercut=0 \
        legend1="$legend" \
        alt=2000 resolution=1
        wait
    fi

    #~ if [ $i -eq 17 ] ; then
        #~ # Set run
        #~ directory="india_test_cotton_yield_rainfed_area"
        #~ parameter="$i"
        #~ legend="kg per ha (rainfed cotton area)"
        #~ # Run GIS routine
        #~ india -c -r \
        #~ states=India \
        #~ clip="cotton_rainfed" \
        #~ SaveDir="$directory" \
        #~ longitude=5 latitude=6 year=11 \
        #~ parameter="$parameter" \
        #~ interpolation="bspline" \
        #~ numpoints=3 pow=2.0 spline_step_east=57000 spline_step_north=57000 tykhonov_reg=0.05 \
        #~ lowercut=0 uppercut=0 \
        #~ legend1="$legend" \
        #~ alt=2000 resolution=1
        #~ wait
    #~ fi

done
exit 0

