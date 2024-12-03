#!/bin/bash
#
# Batch run medPresentClimate CASAS GIS
#
# To run it from 64-SVN DOS text, please enter
# "%GRASS_SH%" batch_oliveProtheusWin.sh
#
# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2011 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 01 September 2011

#~ 1. Model
#~ 2. Date
#~ 3. Cat
#~ 4. GridCoords
#~ 5. Long
#~ 6. Lat
#~ 7. Year
#~ 8. ObsYieldM3Crops
#~ 9. ObsYieldPlus2
#~ 10. FruWgtObs
#~ 11. FruWgtPlus2
#~ 12. DeltaYield
#~ 13. DeltaYieldObs
#~ 14. EUcountry
#~ 15. PrcntAttck
#~ 16. DeltaPrcntAttck
#~ 17. CountryPrice
#~ 18. ObsProfit
#~ 19. ObsProfitPlus2
#~ 20. DeltaRevenue
#~ 21. DeltaRevenueNoAid
#~ 22. DeltaControlCost
#~ 23. DeltaProfit
#~ 24. DeltaProfitNoAid

#~ Number of rows is 996.

## IMPORTANT NOTE ##
# To map only within outliers, the range=min,max option in d.legend
# needs to be enabled in the GIS script MedPresentClimate using
# the two whiskers of the R box plot (see boxplot.stats() in R).

for i in 24; do
    # Observed M3Crops yield
    if [ $i -eq 8 ]; then
        # Set run
        directory="ObservedYield_M3crops_995"
        parameter="$i"
        legend="Yield (tons per ha)"
        # Run GIS routine
        medPresentClimate -p -m -u SaveDir="$directory" longitude=5 latitude=6 year=7 parameter="$parameter" interpolation="idw" lowercut=-10 uppercut=50000 region=-1 alt=900 resolution=1 legend1="$legend"
        wait
    fi
    # Delta yield
    if [ $i -eq 13 ]; then
        # Set run
        directory="DeltaYield_M3crops_995"
        parameter="$i"
        legend="Delta yield (tons per ha) EH5OM"
        # Run GIS routine
        medPresentClimate -p -m -u SaveDir="$directory" longitude=5 latitude=6 year=7 parameter="$parameter" interpolation="idw" lowercut=-10 uppercut=50000 region=-1 alt=900 resolution=1 legend1="$legend"
        wait
    fi
    # Delta infestation
    if [ $i -eq 16 ]; then
        # Set run
        directory="DeltaInfestation_M3crops"
        parameter="$i"
        legend="Delta infestation (%) EH5OM"
        # Run GIS routine
        medPresentClimate -p -m -u SaveDir="$directory" longitude=5 latitude=6 year=7 parameter="$parameter" interpolation="idw" lowercut=-10000 uppercut=50000 region=-1 alt=900 resolution=1 legend1="$legend"
        wait
    fi
    # Delta profit with EU aid
    if [ $i -eq 23 ]; then
        # Set run
        directory="DeltaProfit_M3crops"
        parameter="$i"
        legend="Delta profit (USD per ha)"
        # Run GIS routine
        medPresentClimate -p -m -u SaveDir="$directory" longitude=5 latitude=6 year=7 parameter="$parameter" interpolation="idw" lowercut=-5000000 uppercut=35000000 region=-1 alt=900 resolution=1 legend1="$legend"
        wait
    fi
    # Delta profit without EU aid
    if [ $i -eq 24 ]; then
        # Set run
        directory="DeltaProfitNoAid_M3crops_995"
        parameter="$i"
        legend="Delta profit no aid (USD per ha) EH5OM"
        # Run GIS routine
        medPresentClimate -p -m -u SaveDir="$directory" longitude=5 latitude=6 year=7 parameter="$parameter" interpolation="idw" lowercut=-5000000 uppercut=35000000 region=-1 alt=900 resolution=1 legend1="$legend"
        wait
    fi
done
exit 0
