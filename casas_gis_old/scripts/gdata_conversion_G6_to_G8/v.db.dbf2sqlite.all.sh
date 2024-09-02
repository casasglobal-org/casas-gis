#!/bin/bash
#
############################################################################
#
# MODULE:       v.db.dbf2sqlite.all.sh, based on v.convert.all (GRASS GIS 6.4)
# AUTHOR(S):    Markus Neteler
# PURPOSE:      - rebuilds topology for all vector maps in current mapset
#               - converts all old DBF-based GRASS GIS vector maps to SQLite DB
#                 in current mapset. See:
#                 https://grasswiki.osgeo.org/wiki/Convert_all_GRASS_6_vector_maps_to_GRASS_7
#               - removes empty dbf/ directory
# REQUIREMENTS: patched v.db.reconnect.all.py (fatal -> warning),
#               see v.db.reconnect.all.py.diff
# COPYRIGHT:    (C) 2024 by Markus Neteler and the GRASS Development Team
#
#		This program is free software under the GNU General Public
#		License (>=v2). Read the file COPYING that comes with GRASS
#		for details.
#
#############################################################################

#%Module
#%  description: Converts all old DBF-based GRASS GIS vector maps to SQLite DB in current mapset.
#%  keyword: vector
#%  keyword: DBF
#%  keyword: SQLite
#%end

if  [ -z "$GISBASE" ] ; then
 echo "You must be in GRASS GIS to run this program." >&2
 exit 1
fi

# fail early
set -e

# get current mapset name as a var
eval $(g.gisenv)
# echo $LOCATION_NAME
# echo $MAPSET

# check if the current mapset is still DBF based
eval $(db.connect -g)
# if no longer DBF then quit this conversion script
if test "$driver" != "dbf"
then
    g.message message="Rebuilding topology for all vector maps in current mapset ... (1/1)"
    # rebuild topology for all vector maps in current mapset
    v.build.all
    # attribute tables: nothing to do as SQLite already active in mapset
    # still rm dbf/ dir, but only when empty (GRASS GIS vars from g.gisenv above)
    [ "$(ls -A ${GISDBASE}/${LOCATION_NAME}/${MAPSET}/dbf 2>&1 /dev/null)" ] || rmdir ${GISDBASE}/${LOCATION_NAME}/${MAPSET}/dbf
    g.message message="DBF driver not active in <${LOCATION_NAME}/${MAPSET}> (DB driver <$driver> found)"
    g.message message="Skipping this mapset..."
    exit 0
else
    # so we convert attibute tables to SQLite...
    g.message message="Rebuilding topology for all vector maps in current mapset ... (1/3)"
    # first rebuild topology for all vector maps in current mapset
    v.build.all

    g.message message="Define SQLite backend for vector maps in current mapset ... (2/3)"
    # define new default DB connection (switch from DBF to SQLite)
    db.connect -d

    # print to verify new DB connection settings (should be SQLite)
    db.connect -p

    g.message message="Transfer all attribute tables from DBF to SQLite and clean old DBF tables in current mapset ... (3/3)"
    # transfer all attribute tables from DBF to SQLite and clean old DBF tables
    v.db.reconnect.all -cd
    
    # rm dbf/ dir, but only when empty (GRASS GIS vars from g.gisenv above)
    [ "$(ls -A ${GISDBASE}/${LOCATION_NAME}/${MAPSET}/dbf 2>&1 /dev/null)" ] || rmdir ${GISDBASE}/${LOCATION_NAME}/${MAPSET}/dbf
fi

exit 0


## test all vector maps in a mapset individually:
# g.list type=vector mapset=. ; VECTMAPLIST=$(g.list type=vector mapset=.) ; eval $(g.gisenv) ; for VECTMAP in $VECTMAPLIST ; do v.db.connect -g $VECTMAP@$MAPSET  | cut -d'|' -f5 | grep sqlite > /dev/null || echo "$VECTMAP@$MAPSET is not DBF connected" ; done
