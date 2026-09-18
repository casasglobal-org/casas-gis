#!/usr/bin/env python3
#
# AUTHOR(S):    Luigi Ponti quartese gmail com
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

import os
import pathlib

# define GRASS DATABASE
# Prefer GRASSDATA, then the GISDBASE of an active GRASS session.
grassdata = os.environ.get("GRASSDATA") or os.environ.get("GISDBASE")
if grassdata is None:
    try:
        import grass.script as grass

        grassdata = grass.gisenv()["GISDBASE"]
    except Exception:
        # Allow importing the package without a GRASS installation,
        # e.g., for unit tests or while not inside a GRASS session.
        grassdata = str(pathlib.Path.home() / "grassdata")
grassdata = pathlib.Path(grassdata)
gisdb = grassdata
print(gisdb)
