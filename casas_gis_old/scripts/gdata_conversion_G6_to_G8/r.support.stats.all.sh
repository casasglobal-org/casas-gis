#!/bin/bash
#
############################################################################
#
# MODULE:     r.support.stats.all.sh
#             called by process_grass6data_casas.sh
# AUTHOR(S):  Markus Neteler
# PURPOSE:    update statistics of all raster maps in current mapset
# COPYRIGHT:  (C) 2024 by Markus Neteler and the GRASS Development Team
#
#		This program is free software under the GNU General Public
#		License (>=v2). Read the file COPYING that comes with GRASS
#		for details.
#
#############################################################################

#%Module
#%  description: Update statistics of all raster maps in current mapset.
#%  keyword: raster
#%  keyword: statistics
#%end

if  [ -z "$GISBASE" ] ; then
 echo "You must be in GRASS GIS to run this program." >&2
 exit 1
fi

# fail early
#set -e  # commented to avoid stop at r.external error

# get current mapset name as a var
eval $(g.gisenv)
# echo $LOCATION_NAME
# echo $MAPSET

export GRASS_MESSAGE_FORMAT=plain

NUM=$(g.list type=raster mapset=. | wc -l)
g.message message="Recomputing raster statistics for $NUM raster maps..."

RASTMAPLIST=$(g.list type=raster mapset=.)
for RASTMAP in $RASTMAPLIST ; do
    g.region raster=$RASTMAP@$MAPSET  # needed for r.support -s?
    r.support -s $RASTMAP@$MAPSET
done
