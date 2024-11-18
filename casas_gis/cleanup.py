#!/usr/bin/env python3
#
# AUTHOR(S):    Luigi Ponti quartese gmail com
#
# PURPOSE:      
#
# NOTE:         
#
# COPYRIGHT:    (c) 2021-2024 CASAS (Center for the Analysis
#                   of Sustainable Agricultural Systems).
#                   https://www.casasglobal.org/).
#
#               SPDX-License-Identifier: GPL-3.0-or-later

# Clenaup routine?
# See https://grasswiki.osgeo.org/wiki/Converting_Bash_scripts_to_Python

import os
import constants as k

from dotenv import load_dotenv

load_dotenv()  # needed for grass_session

from grass_session import Session  # noqa E402
import grass.script as grass  # noqa E402

grassbin = os.getenv("GRASSBIN")


def print_grass_environment():
    """ Print current GIS environmental variables. """
    print('\nCurrent GIS environmental variables:\n')
    grass_env = grass.parse_command("g.gisenv", flags="n")
    for key, value in grass_env.items():
        print('{:16}{}'.format(f"{key}:", value))


def list_vector_maps():
    """ List vector maps in current location. """
    grass_env = grass.parse_command("g.gisenv", flags="n")
    print(f"\nVector maps in location '{grass_env['LOCATION_NAME']}'"
          f" and mapset '{grass_env['MAPSET']}':\n")
    grass.run_command("g.list",
                      flags="p", verbose=True,
                      type="vector", mapset=".")


def clean_up_vectors():
    """ Clean up GIS files that are no longer needed. """
    print('\nRemove previously imported vector maps:\n')
    grass.run_command("g.remove",
                      flags="f", verbose=True,
                      type="vector", pattern=f"{k.IMPORTED_PREFIX}*")
    grass.run_command("g.remove",
                      flags="f", verbose=True,
                      type="vector", pattern=f"{k.SELECTED_PREFIX}*")


def clean_up_rasters():
    grass.run_command("g.remove",
                      flags="f", verbose=True,
                      type="raster", pattern=f"{k.IDW_PREFIX}*")
    grass.run_command("g.remove",
                      flags="f", verbose=True,
                      type="raster", pattern=f"{k.BSPLINE_PREFIX}*")
