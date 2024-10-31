#!/bin/bash
#
# Batch run medPresentClimate CASAS GIS
#
# Developed for the figures of the Ziska chapter.
#
# To run it from 64-SVN DOS text, please enter
# "%GRASS_SH%" batch_oliveProtheusWin.sh
#
# Luigi Ponti, 10 March 2012
#

#~ 28. OfPupSum

#~ Number of rows is 1008.

## IMPORTANT NOTE ##
# To map only within outliers, the range=min,max option in d.legend
# needs to be enabled in the GIS script MedPresentClimate using
# the two whiskers of the R box plot (see boxplot.stats() in R).

for i in 19 28 30
do
    # Cumulative olive fly pupae
    #~ if [ $i -eq 28 ] ; then
        #~ # Set run
        #~ directory="01_Cumulative_pupae_BW_fisher2"
        #~ parameter="$i"
        #~ legend="Cumulative olive fly pupae"
        #~ # Run GIS routine
        #~ medPresentClimate -g -p -m SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" interpolation="idw" lowercut=0 uppercut=50000\
            #~ region=-1 alt=900 resolution=2 legend1="$legend" lowBarCol=0.001666667 upBarCol=8315.186
        #~ wait
    #~ fi
    # Change in olive fly pupae POS
    #~ if [ $i -eq 28 ] ; then
        #~ # Set run
        #~ directory="02_DeltaPupaePOS_BW_outliers"
        #~ parameter="$i"
        #~ legend="Delta pupae POS"
        #~ # Run GIS routine
        #~ medPresentClimate -w -g -p -m SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" interpolation="idw" lowercut=0 uppercut=50000\
            #~ region=-1 alt=900 resolution=2 legend1="$legend" lowBarCol=37.645 upBarCol=5147.558
        #~ wait
    #~ fi
    # Change in olive fly pupae NEG
    #~ if [ $i -eq 28 ] ; then
        #~ # Set run
        #~ directory="02_DeltaPupaeNEG_BW_outliers"
        #~ parameter="$i"
        #~ legend="Delta pupae NEG"
        #~ # Run GIS routine
        #~ medPresentClimate -u -w -g -p -m SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" interpolation="idw" lowercut=-5000 uppercut=0\
            #~ region=-1 alt=900 resolution=2 legend1="$legend" lowBarCol=-3115.578 upBarCol=-6.420238
        #~ wait
    #~ fi
    # Change in % fruit attacked POS
    #~ if [ $i -eq 30 ] ; then
        #~ # Set run
        #~ directory="03_DeltaInfestPOS_BW_outliers"
        #~ parameter="$i"
        #~ legend="Delta infestation POS"
        #~ # Run GIS routine
        #~ medPresentClimate -w -g -p -m SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" interpolation="idw" lowercut=0 uppercut=50000\
            #~ region=-1 alt=900 resolution=2 legend1="$legend" lowBarCol=0.0997619 upBarCol=40.49238
        #~ wait
    #~ fi
    # Change in % fruit attacked NEG
    #~ if [ $i -eq 30 ] ; then
        #~ # Set run
        #~ directory="03_DeltaInfestNEG_BW_outliers"
        #~ parameter="$i"
        #~ legend="Delta infestation NEG"
        #~ # Run GIS routine
        #~ medPresentClimate -u -g -p -m SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" interpolation="idw" lowercut=-5000 uppercut=0\
            #~ region=-1 alt=900 resolution=2 legend1="$legend"
        #~ wait
    #~ fi
    # Change in olive oil profit (no aid) POS
    #~ if [ $i -eq 19 ] ; then
        #~ # Set run
        #~ directory="04_DeltaProfitPOS_BW_outliers"
        #~ parameter="$i"
        #~ legend="Delta profit POS"
        #~ # Run GIS routine
        #~ medPresentClimate -w -g -p -m SaveDir="$directory" longitude=5 latitude=6 year=11\
            #~ parameter="$parameter" interpolation="idw" lowercut=0 uppercut=50000\
            #~ region=-1 alt=900 resolution=2 legend1="$legend" lowBarCol=0.06739467 upBarCol=807.9007
        #~ wait
    #~ fi
    # Change in olive oil profit (no aid) NEG
    if [ $i -eq 19 ] ; then
        # Set run
        directory="04_DeltaProfitNEG_BW_fisher"
        parameter="$i"
        legend="Delta profit NEG"
        # Run GIS routine
        medPresentClimate -u -g -p -m SaveDir="$directory" longitude=5 latitude=6 year=11\
            parameter="$parameter" interpolation="idw" lowercut=-5000 uppercut=0\
            region=-1 alt=900 resolution=2 legend1="$legend" lowBarCol=-350.1798 upBarCol=-0.6018674
        wait
    fi
done
exit 0

