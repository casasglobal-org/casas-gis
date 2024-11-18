#!/bin/bash
#
############################################################################
#
# MODULE:       process_grass6data_casas.sh
# AUTHOR(S):    Markus Neteler
# PURPOSE:      Metascript to then run:
#               - vector_convert_all_mapsets_G6_G8.sh which calls
#                  - GRASS GIS and within v.db.dbf2sqlite.all.sh
#               - raster_convert_all_mapsets_G6_G8.sh
#                  - GRASS GIS and within r.support.stats.all.sh
# REQUIREMENTS: patched version of v.db.reconnect.all.py (fatal -> warning)
# COPYRIGHT:    (C) 2024 by Markus Neteler and the GRASS Development Team
#
#		        SPDX-License-Identifier: GPL-2.0-or-later
#
#############################################################################

# cleanup previous run
rm -rf ~/grass6data_casas

# extract ZIP
7z x ~/Downloads/casas_gis_old_grass6data_cleaned.zip

cd ~/grass6data_casas/
# remove garbage (dead, incomplete maps)
rm -rf "AEA_Med/luigi/vector/clc00_v2_code_223_olive_points"
rm -f "AEA_Med/luigi/cats/interpolMinSumLowMu_Plants_18Nov22_Avg (1)"

echo "
Next run (takes ~40 min on Intel Core i7):
 sh ~/software/casas-gis/casas_gis_old/scripts/gdata_conversion_G6_to_G8/vector_convert_all_mapsets_G6_G8.sh

and then run (takes ~15 min on Intel Core i7):
 sh ~/software/casas-gis/casas_gis_old/scripts/gdata_conversion_G6_to_G8/raster_convert_all_mapsets_G6_G8.sh
"
