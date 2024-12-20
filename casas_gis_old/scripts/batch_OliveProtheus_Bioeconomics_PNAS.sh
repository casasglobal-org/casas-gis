#!/bin/bash
#
# Batch run medPresentClimate CASAS GIS
#
# To run it from 64-SVN DOS text, please enter
# "%GRASS_SH%" batch_oliveProtheusWin.sh
#
# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2014 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 07 Jan 2014

#~ YIELD

#~ 1. Model
#~ 2. Date
#~ 3. Time
#~ 4. WxFile
#~ 5. Long
#~ 6. Lat
#~ 7. JdStart
#~ 8. DysToOut
#~ 9. Month
#~ 10. Day
#~ 11. Year
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

#~ INFESTATION

#~ 1. Model
#~ 2. Date
#~ 3. Time
#~ 4. WxFile
#~ 5. Long
#~ 6. Lat
#~ 7. JdStart
#~ 8. DysToOut
#~ 9. Month
#~ 10. Day
#~ 11. Year
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
#~ 24. OFEgDays
#~ 25. OFLrDays
#~ 26. OFPuDays
#~ 27. OFAdDays
#~ 28. OfPupSum
#~ 29. DamFrSum
#~ 30. PrcntAtkd

#~ PROFIT:

#~ 1. Model
#~ 2. Date
#~ 3. Cat
#~ 4. GridCoords
#~ 5. Long
#~ 6. Lat
#~ 7. Year
#~ 8. ObsYieldM3Crops
#~ 9. SimulatedYield
#~ 10. ObsYieldScaled
#~ 11. EUcountry
#~ 12. PrcntAttck
#~ 13. CountryPrice
#~ 14. Profit
#~ 15. ProfitWithAid

#~ Number of rows is 996.

#~ Number of rows is 996.

for i in 24; do
    #~ # Yield
    #~ if [ $i -eq 14 ] ; then
    #~ # Set run
    #~ directory="olive_yield_delta_CV"
    #~ parameter="$i"
    #~ legend="olive yield delta CV"
    #~ # Run GIS routine
    #~ medPresentClimate -p -m -w SaveDir="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" interpolation="idw" lowercut=-10000 region=-1 alt=900 resolution=1\
    #~ legend1="$legend" lowBarCol=-34.8554307206397 upBarCol=22.9235309499502
    #~ wait
    #~ fi
    #~ # Infestation
    #~ if [ $i -eq 30 ] ; then
    #~ # Set run
    #~ directory="olive_infestation_delta_IQR"
    #~ parameter="$i"
    #~ legend="olive infestation delta IQR"
    #~ # Run GIS routine
    #~ medPresentClimate -p -m -w SaveDir="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" interpolation="idw" lowercut=-10000 region=-1 alt=900 resolution=1\
    #~ legend1="$legend" lowBarCol=-24.4430010546617 upBarCol=21.1323842803864
    #~ wait
    #~ fi
    # Profit
    if [ $i -eq 24 ]; then
        # Set run
        directory="olive_profit_delta_for_Agnoletti"
        parameter="$i"
        legend="olive profit delta"
        # Run GIS routine
        medPresentClimate -p -m -w SaveDir="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" interpolation="idw" lowercut=-10000 region=-1 alt=900 resolution=1 legend1="$legend" lowBarCol=-256.458 upBarCol=430.768
        wait
    fi
done
exit 0
