#!/bin/sh
#
# Batch run medPresentClimate CASAS GIS
#
# To run it from 64-SVN DOS text, please e
# "%GRASS_SH%" batch_oliveProtheusWin.sh
#
# Luigi Ponti, 17 March 2010
#

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

for i in 12 13 14 16 17 18 20 22 23 24 25 26 28
do
    #~ # Day degrees
    #~ if [ $i -eq 12 ] ; then
        #~ # Set run
        #~ directory="test_US-Mex_dd"
        #~ parameter="$i"
        #~ legend="dd for olive"       
        #~ # Run GIS routine
       #~ usa states='US_conterm_Mex'\
            #~ SaveDir="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" lowercut=0 uppercut=0\
            #~ legend1="$legend"\
            #~ alt=1000 resolution=1 # colorRuleDivergent=4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0
        #~ wait
    #~ fi
    
    #~ # Day degrees below zero
    #~ if [ $i -eq 13 ] ; then
        #~ # Set run
        #~ directory="ddBelowZeroNoClip_lowercut30"
        #~ parameter="$i"
        #~ legend="day degrees below zero"   
        #~ # Run GIS routine
        #~ medPresentClimate -c -p SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" interpolation="inverse_distance_weighting" lowercut=30 uppercut=0 region=-1 alt=10000 resolution=1\
            #~ legend1="$legend" 
            #~ # colorRuleDivergent=4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0
       #~ # This color is Panoply with white in the middle (divergent)
        #~ wait            
    #~ fi    
   
    #~ # Fruit weight
    #~ if [ $i -eq 14 ] ; then
        #~ # Set run
        #~ directory="FruitWeight_Hawaii"
        #~ parameter="$i"
        #~ legend="Fruit Weight"       
        #~ # Run GIS routine
       #~ usa -c states='HI'\
            #~ SaveDir="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" lowercut=0 uppercut=0\
            #~ legend1="$legend"\
            #~ alt=900 resolution=1 # colorRuleDivergent=4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0
        #~ wait
    #~ fi
    
    #~ # Bloom date
    #~ if [ $i -eq 16 ] ; then
        #~ # Set run
        #~ directory="BloomDate_US_mex"
        #~ parameter="$i"
        #~ legend="Bloom date"        
        #~ # Run GIS routine
        #~ usa -c states='US_conterm_Mex'\
            #~ SaveDir="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" lowercut=1 uppercut=0\
            #~ legend1="$legend"\
            #~ alt=900 resolution=1  # colorRuleDivergent=4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0
        # This color is Panoply with white in the middle (divergent)
        #~ wait 
    #~ fi
    
    #~ # Years of blooming
    #~ if [ $i -eq 17 ] ; then
        #~ # Set run
        #~ directory="BloomYears_Diff2"
        #~ parameter="$i"
        #~ legend="Years with bloom"   
        #~ # Run GIS routine
        #~ medPresentClimate -c -p -d -x SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" lowercut=-999999 uppercut=0 region='21 22 23 25 31 32 33 35' alt=700 resolution=1\
            #~ legend1="$legend" colorRuleDivergent=4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0
       #~ # This color is Panoply with white in the middle (divergent)
        #~ wait            
    #~ fi   
    
    #~ # Total day degrees below 9.1
    #~ if [ $i -eq 18 ] ; then
        #~ # Set run
        #~ directory="DDBSum"
        #~ parameter="$i"
        #~ legend="day degrees below 9.1"
        #~ # Run GIS routine
        #~ medPresentClimate -c -p SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" lowercut=0 uppercut=0 region='21 22 23 25 31 32 33 35' alt=700 resolution=1\
            #~ legend1="$legend" # colorRuleDivergent=4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0
       #~ # This color is Panoply with white in the middle (divergent)
        #~ wait            
    #~ fi    

    # Total yearly rainfall
    if [ $i -eq 20 ] ; then
        # Set run
        directory="Prcp_US_Hawaii3"
        parameter="$i"
        legend="mm rainfall per year"
        # Run GIS routine
        usa states='HI'\
            SaveDir="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" lowercut=0 uppercut=0\
            legend1="$legend"\
            alt=1500 resolution=1 # colorRuleDivergent=4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0
        wait            
    fi
    
    #~ # ddBelow -10 �C only with a recent run of olive plant.
    #~ if [ $i -eq 22 ] ; then
        #~ # Set run
        #~ directory="ddbMinus10"
        #~ parameter="$i"
        #~ legend="Day degrees below -10"
        #~ # Run GIS routine
        #~ medPresentClimate -c -p SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" interpolation="inverse_distance_weighting" lowercut=1 uppercut=0 region='21 22 23 25 31 32 33 35' alt=10000 resolution=1\
            #~ legend1="$legend" 
    #~ wait             
    #~ fi
    
    #~ # ddBelow -8.3 �C only with a recent run of olive plant.
    #~ if [ $i -eq 23 ] ; then
        #~ # Set run
        #~ directory="ddbMinus83_bspline"
        #~ parameter="$i"
        #~ legend="Day degrees below -8.3"
        #~ # Run GIS routine
        #~ medPresentClimate -c -p SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" interpolation="bicubic_spline" lowercut=1 uppercut=0 region=-1 alt=10000 resolution=1\
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
        #~ medPresentClimate -c -p SaveDir="$directory" longitude=5 latitude=6 year=11\
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
        #~ medPresentClimate -c -p SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" lowercut=0 uppercut=0 region='21 22 23 25 31 32 33 35' alt=700 resolution=1\
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
        #~ medPresentClimate -c -p SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" lowercut=0 uppercut=0 region='21 22 23 25 31 32 33 35' alt=700 resolution=1\
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
        #~ medPresentClimate -c -p SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" lowercut=1 uppercut=0 region='21 22 23 25 31 32 33 35' alt=700 resolution=1\
            #~ legend1="$legend"       
    #~ wait         
    #~ fi
    
    #~ # OF pupae CumSum
    #~ if [ $i -eq 26 ] ; then
        #~ # Set run
        #~ directory="OFpupaeCumSum_MedClip"
        #~ parameter="$i"
        #~ legend="OF pupae CumSum"       
        #~ # Run GIS routine
        #~ medPresentClimate -p -m SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" interpolation="inverse_distance_weighting" lowercut=0 uppercut=0 region='21 22 23 25 31 32 33 35' alt=700 resolution=1\
            #~ legend1="$legend" 
            #~ # colorRuleDivergent=4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0
    #~ fi
    
    #~ # Percent fruit attacked
    #~ if [ $i -eq 28 ] ; then
        #~ # Set run
        #~ directory="PercentFruitAttacked_MedClip"
        #~ parameter="$i"
        #~ legend="Percent fruit attacked"    
        #~ # Run GIS routine
        #~ medPresentClimate -p -m SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" interpolation="inverse_distance_weighting" lowercut=0 uppercut=0 region='21 22 23 25 31 32 33 35' alt=700 resolution=1\
            #~ legend1="$legend" 
            #~ # colorRuleDivergent=4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0   
    #~ fi
    
done
exit 0
