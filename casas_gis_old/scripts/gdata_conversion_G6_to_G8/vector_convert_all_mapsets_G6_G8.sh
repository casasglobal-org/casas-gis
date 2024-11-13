#!/bin/bash
#
############################################################################
#
# MODULE:     vector_convert_all_mapsets_G6_G8.sh
#             called by process_grass6data_casas.sh
# AUTHOR(S):  Markus Neteler
# PURPOSE:    converts all mapsets in current directory tree from
#             old DBF-based GRASS GIS vector maps to SQLite DB
# COPYRIGHT:  (C) 2024 by Markus Neteler and the GRASS Development Team
#
#		This program is free software under the GNU General Public
#		License (>=v2). Read the file COPYING that comes with GRASS
#		for details.
#
#############################################################################

# fail early
set -e

export GRASS_MESSAGE_FORMAT=plain

# log stdout and stderr into: conversion_vector.log
# also show all in the terminal

echo "Start: $(date)"
# initiate new file
echo "Start: $(date)" > conversion_vector.log

cd ~/grass6data_casas/

for LOC_MAPSET in $(find . -name WIND | sed 's+/WIND++g'); do
    echo "########### START Processing <$LOC_MAPSET>"
    grass8.dev "$LOC_MAPSET" --exec v.db.dbf2sqlite.all.sh
    echo "########### END Processing <$LOC_MAPSET>"
done 2>&1 | tee -a conversion_vector.log

echo "End: $(date)"
echo "End: $(date)" >> conversion_vector.log

echo "

Conversion in all mapsets done.
Log file written to <conversion_vector.log>
"
exit 0
