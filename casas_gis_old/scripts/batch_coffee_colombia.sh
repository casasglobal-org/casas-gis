#!/bin/sh
#
# Batch run medPresentClimate CASAS GIS
#
# Run from Colombia shell with following command
# "C:\Program Files (x86)\GRASS GIS 6.4.4\msys\bin\sh.exe" batch_coffee_colombia.sh
#
# Author: Luigi Ponti
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 02 October 2019

# NASA Panoply
# "4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0"

# The following column names were found:

# 1. file
# 2. days
# 3. Path_Archivo
# 4. Longitude
# 5. Latitude
# 6. meandamnum
# 7. meanripemass
# 8. meanTdda
# 9. meanRain
# 10. meanLangl
# 11. displaydays
# 12. year

# Number of rows is 1483.

# Run test with first file sent byUMNG
# -x if an overall compound legend is needed
run_test_coffee() {

    for i in 6 7 8 9 10; do
        # 6. meandamnum
        if [ $i -eq 6 ]; then
            # Set run
            directory="colombia_coffee_meandamnum_crop_extent"
            parameter="$i"
            legend="meandamnum"
            # Run GIS routine
            map.pbdm.colombia -r -p SaveDir="$directory" \
                longitude=4 latitude=5 year=12 parameter="$parameter" \
                interpolation=bspline numpoints=3 legend1="$legend" \
                colorRuleRegular="4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0" \
                lowercut=0 uppercut=0 departments=all crop=coffee cropthreshold=0.01 alt=10000 resolution=1
            wait
        fi

        # 7. meanripemass
        if [ $i -eq 7 ]; then
            # Set run
            directory="colombia_coffee_meanripemass_crop_extent"
            parameter="$i"
            legend="meanripemass"
            # Run GIS routine
            map.pbdm.colombia -r -p SaveDir="$directory" \
                longitude=4 latitude=5 year=12 parameter="$parameter" \
                interpolation=bspline numpoints=3 legend1="$legend" \
                colorRuleRegular="4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0" \
                lowercut=0 uppercut=0 departments=all crop=coffee cropthreshold=0.01 alt=10000 resolution=1
            wait
        fi

        # 8. meanTdda
        if [ $i -eq 8 ]; then
            # Set run
            directory="colombia_coffee_meanTdda_crop_extent"
            parameter="$i"
            legend="meanTdda"
            # Run GIS routine
            map.pbdm.colombia -r -p SaveDir="$directory" \
                longitude=4 latitude=5 year=12 parameter="$parameter" \
                interpolation=bspline numpoints=3 legend1="$legend" \
                colorRuleRegular="4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0" \
                lowercut=0 uppercut=0 departments=all crop=coffee cropthreshold=0.01 alt=10000 resolution=1
            wait
        fi

        # 9. meanRain
        if [ $i -eq 9 ]; then
            # Set run
            directory="colombia_coffee_meanRain_crop_extent"
            parameter="$i"
            legend="meanRain"
            # Run GIS routine
            map.pbdm.colombia -r -p SaveDir="$directory" \
                longitude=4 latitude=5 year=12 parameter="$parameter" \
                interpolation=bspline numpoints=3 legend1="$legend" \
                colorRuleRegular="4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0" \
                lowercut=0 uppercut=0 departments=all crop=coffee cropthreshold=0.01 alt=10000 resolution=1
            wait
        fi

        # 10. meanLangl
        if [ $i -eq 10 ]; then
            # Set run
            directory="colombia_coffee_meanLangl_crop_extent"
            parameter="$i"
            legend="meanLangl"
            # Run GIS routine
            map.pbdm.colombia -r -p SaveDir="$directory" \
                longitude=4 latitude=5 year=12 parameter="$parameter" \
                interpolation=bspline numpoints=3 legend1="$legend" \
                colorRuleRegular="4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0" \
                lowercut=0 uppercut=0 departments=all crop=coffee cropthreshold=0.01 alt=10000 resolution=1
            wait
        fi
    done
}

# The following column names were found:

# 1. file
# 2. days
# 3. Path_Archivo
# 4. Longitude
# 5. Latitude
# 6. meandamnum
# 7. meanripemass
# 8. meanTdda
# 9. meanRain
# 10. meanLangl
# 11. displaydays
# 12. year

# Number of rows is 1483.

# Run test with first file sent byUMNG
# -x if an overall compound legend is needed
run_test_coffee_no_crop_constraint() {

    for i in 6 7 8 9 10; do
        # 6. meandamnum
        if [ $i -eq 6 ]; then
            # Set run
            directory="colombia_coffee_meandamnum_full_extent"
            parameter="$i"
            legend="meandamnum"
            # Run GIS routine
            map.pbdm.colombia -r -p SaveDir="$directory" \
                longitude=4 latitude=5 year=12 parameter="$parameter" \
                interpolation=bspline numpoints=3 legend1="$legend" \
                colorRuleRegular="4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0" \
                lowercut=0 uppercut=0 departments=all crop=none cropthreshold=0.01 alt=10000 resolution=1
            wait
        fi

        # 7. meanripemass
        if [ $i -eq 7 ]; then
            # Set run
            directory="colombia_coffee_meanripemass_full_extent"
            parameter="$i"
            legend="meanripemass"
            # Run GIS routine
            map.pbdm.colombia -r -p SaveDir="$directory" \
                longitude=4 latitude=5 year=12 parameter="$parameter" \
                interpolation=bspline numpoints=3 legend1="$legend" \
                colorRuleRegular="4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0" \
                lowercut=0 uppercut=0 departments=all crop=none cropthreshold=0.01 alt=10000 resolution=1
            wait
        fi

        # 8. meanTdda
        if [ $i -eq 8 ]; then
            # Set run
            directory="colombia_coffee_meanTddav_full_extent"
            parameter="$i"
            legend="meanTdda"
            # Run GIS routine
            map.pbdm.colombia -r -p SaveDir="$directory" \
                longitude=4 latitude=5 year=12 parameter="$parameter" \
                interpolation=bspline numpoints=3 legend1="$legend" \
                colorRuleRegular="4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0" \
                lowercut=0 uppercut=0 departments=all crop=none cropthreshold=0.01 alt=10000 resolution=1
            wait
        fi

        # 9. meanRain
        if [ $i -eq 9 ]; then
            # Set run
            directory="colombia_coffee_meanRain_full_extent"
            parameter="$i"
            legend="meanRain"
            # Run GIS routine
            map.pbdm.colombia -r -p SaveDir="$directory" \
                longitude=4 latitude=5 year=12 parameter="$parameter" \
                interpolation=bspline numpoints=3 legend1="$legend" \
                colorRuleRegular="4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0" \
                lowercut=0 uppercut=0 departments=all crop=none cropthreshold=0.01 alt=10000 resolution=1
            wait
        fi

        # 10. meanLangl
        if [ $i -eq 10 ]; then
            # Set run
            directory="colombia_coffee_meanLangl_full_extent"
            parameter="$i"
            legend="meanLangl"
            # Run GIS routine
            map.pbdm.colombia -r -p SaveDir="$directory" \
                longitude=4 latitude=5 year=12 parameter="$parameter" \
                interpolation=bspline numpoints=3 legend1="$legend" \
                colorRuleRegular="4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0" \
                lowercut=0 uppercut=0 departments=all crop=none cropthreshold=0.01 alt=10000 resolution=1
            wait
        fi
    done
}

run_test_coffee_no_crop_constraint

exit 0
