#!/usr/bin/env python3
#
# AUTHOR(S):    Luigi Ponti quartese gmail com
# AUTHOR(S):    Luca Delucchi, luca delucchi fmach it, Fondazione Edmund Mach
# AUTHOR(S):    big-pickle AI model
#
# PURPOSE:
#
# NOTE:
#
# Copyright:    (c) 2021-2024 CASAS (Center for the Analysis
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
    """Print current GIS environmental variables.

    Returns:
        None."""
    print("\nCurrent GIS environmental variables:\n")
    grass_env = grass.parse_command("g.gisenv", flags="n")
    for key, value in grass_env.items():
        print("{:16}{}".format(f"{key}:", value))


def list_vector_maps():
    """List vector maps in current location.

    Returns:
        None."""
    grass_env = grass.parse_command("g.gisenv", flags="n")
    print(
        f"\nVector maps in location '{grass_env['LOCATION_NAME']}'"
        f" and mapset '{grass_env['MAPSET']}':\n"
    )
    grass.run_command("g.list", flags="p", verbose=True, type="vector", mapset=".")


def clean_up_vectors():
    """Clean up GIS files that are no longer needed.

    Removes previously imported (imp_*) and selected (sel_*) vector
    maps from the current mapset.

    Returns:
        None."""
    print("\nRemove previously imported vector maps:\n")
    try:
        grass.run_command(
            "g.remove",
            flags="f",
            verbose=True,
            type="vector",
            pattern=f"{k.IMPORTED_PREFIX}*",
        )
        grass.run_command(
            "g.remove",
            flags="f",
            verbose=True,
            type="vector",
            pattern=f"{k.SELECTED_PREFIX}*",
        )
    except Exception as e:
        print(f"Error removing vector maps: {e}")


def clean_up_rasters():
    """Remove previously interpolated raster maps (idw_*/bspline_*)
    from the current mapset.

    Returns:
        None."""
    try:
        grass.run_command(
            "g.remove",
            flags="f",
            verbose=True,
            type="raster",
            pattern=f"{k.IDW_PREFIX}*",
        )
        grass.run_command(
            "g.remove",
            flags="f",
            verbose=True,
            type="raster",
            pattern=f"{k.BSPLINE_PREFIX}*",
        )
    except Exception as e:
        print(f"Error removing raster maps: {e}")


def clean_up_tmp():
    """Remove text files left in the temporary directory.

    Returns:
        None."""
    import pathlib

    for path in pathlib.Path(k.TMP_DIR).glob("*.txt"):
        path.unlink()
