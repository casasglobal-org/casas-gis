#!/bin/bash
#
# Batch run MedPresentClimate CASAS GIS
#
# Developed for the figures of the Ziska chapter.
#
# OLD:
#  To run it from 64-SVN DOS text, please enter
#  "%GRASS_SH%" batch_oliveProtheusWin.sh
# NEW:
#  grass84 $HOME/data/casas/grass8data_casas/latlong/luigi/ --exec $HOME/software/casas-gis/casas_gis_old/scripts/batch_OliveProtheus.sh
#
# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2012 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 10 March 2012
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

#~ 28. OfPupSum

#~ Number of rows is 1008.

## IMPORTANT NOTE ##
# To map only within outliers, the range=min,max option in d.legend
# needs to be enabled in the GIS script MedPresentClimate using
# the two whiskers of the R box plot (see boxplot.stats() in R).

for i in 19 28 30; do
    # Cumulative olive fly pupae
    #~ if [ $i -eq 28 ] ; then
    #~ # Set run
    #~ directory="01_Cumulative_pupae_BW_fisher2"
    #~ parameter="$i"
    #~ legend="Cumulative olive fly pupae"
    #~ # Run GIS routine
    #~ MedPresentClimate -g -p -m save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" interpolation="idw" lowercut=0 uppercut=50000\
    #~ region=-1 alt=900 resolution=2 legend1="$legend" low_bar_col=0.001666667 up_bar_col=8315.186
    #~ wait
    #~ fi
    # Change in olive fly pupae POS
    #~ if [ $i -eq 28 ] ; then
    #~ # Set run
    #~ directory="02_DeltaPupaePOS_BW_outliers"
    #~ parameter="$i"
    #~ legend="Delta pupae POS"
    #~ # Run GIS routine
    #~ MedPresentClimate -w -g -p -m save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" interpolation="idw" lowercut=0 uppercut=50000\
    #~ region=-1 alt=900 resolution=2 legend1="$legend" low_bar_col=37.645 up_bar_col=5147.558
    #~ wait
    #~ fi
    # Change in olive fly pupae NEG
    #~ if [ $i -eq 28 ] ; then
    #~ # Set run
    #~ directory="02_DeltaPupaeNEG_BW_outliers"
    #~ parameter="$i"
    #~ legend="Delta pupae NEG"
    #~ # Run GIS routine
    #~ MedPresentClimate -u -w -g -p -m save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" interpolation="idw" lowercut=-5000 uppercut=0\
    #~ region=-1 alt=900 resolution=2 legend1="$legend" low_bar_col=-3115.578 up_bar_col=-6.420238
    #~ wait
    #~ fi
    # Change in % fruit attacked POS
    #~ if [ $i -eq 30 ] ; then
    #~ # Set run
    #~ directory="03_DeltaInfestPOS_BW_outliers"
    #~ parameter="$i"
    #~ legend="Delta infestation POS"
    #~ # Run GIS routine
    #~ MedPresentClimate -w -g -p -m save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" interpolation="idw" lowercut=0 uppercut=50000\
    #~ region=-1 alt=900 resolution=2 legend1="$legend" low_bar_col=0.0997619 up_bar_col=40.49238
    #~ wait
    #~ fi
    # Change in % fruit attacked NEG
    #~ if [ $i -eq 30 ] ; then
    #~ # Set run
    #~ directory="03_DeltaInfestNEG_BW_outliers"
    #~ parameter="$i"
    #~ legend="Delta infestation NEG"
    #~ # Run GIS routine
    #~ MedPresentClimate -u -g -p -m save_directory="$directory" longitude=5 latitude=6 year=11\
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
    #~ MedPresentClimate -w -g -p -m save_directory="$directory" longitude=5 latitude=6 year=11\
    #~ parameter="$parameter" interpolation="idw" lowercut=0 uppercut=50000\
    #~ region=-1 alt=900 resolution=2 legend1="$legend" low_bar_col=0.06739467 up_bar_col=807.9007
    #~ wait
    #~ fi
    # Change in olive oil profit (no aid) NEG
    if [ $i -eq 19 ]; then
        # Set run
        directory="04_DeltaProfitNEG_BW_fisher"
        parameter="$i"
        legend="Delta profit NEG"
        # Run GIS routine
        MedPresentClimate -u -g -p -m save_directory="$directory" longitude=5 latitude=6 year=11 parameter="$parameter" interpolation="idw" lowercut=-5000 uppercut=0 region=-1 alt=900 resolution=2 legend1="$legend" low_bar_col=-350.1798 up_bar_col=-0.6018674
        wait
    fi
done
exit 0
