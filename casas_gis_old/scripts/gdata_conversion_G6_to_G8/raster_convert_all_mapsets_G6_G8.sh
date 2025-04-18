#!/bin/bash
#
############################################################################
#
# MODULE:     raster_convert_all_mapsets_G6_G8.sh
#             called by process_grass6data_casas.sh
# AUTHOR(S):  Markus Neteler
# PURPOSE:    updates raster statistics
# Copyright:  (C) 2024 by Markus Neteler and the GRASS Development Team
#
#		      SPDX-License-Identifier: GPL-2.0-or-later
#
#############################################################################

# fail early
set -e

export GRASS_MESSAGE_FORMAT=plain

# log stdout and stderr into: conversion_raster.log
# also show all in the terminal

echo "Start: $(date)"
# initiate new file
echo "Start: $(date)" > conversion_raster.log

cd ~/grass6data_casas/

for LOC_MAPSET in $(find . -name WIND | sed 's+/WIND++g'); do
    echo "########### START Processing <$LOC_MAPSET>"
    grass8.dev "$LOC_MAPSET" --exec r.support.stats.all.sh
    echo "########### END Processing <$LOC_MAPSET>"
done 2>&1 | tee -a conversion_raster.log

echo "End: $(date)"
echo "End: $(date)" >> conversion_raster.log

echo "

Conversion in all mapsets done.
Log file written to <conversion_raster.log>
"
exit 0
