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

import os
import pathlib
import locations as loc

# Select the region to process. The default is "colombia"; set the
# CASAS_REGION environment variable to process another region, e.g.
#   CASAS_REGION=mediterranean python gis.py
# Valid regions are the keys of loc.regions (see locations.py).
_region_name = os.environ.get("CASAS_REGION", "colombia")
if _region_name not in loc.regions:
    raise ValueError(
        f"Unknown CASAS_REGION '{_region_name}'.\n"
        f"Available regions: {', '.join(loc.regions)}"
    )
_region = loc.regions[_region_name]

# Specify (existing) locations and mapsets
latlong_session = _region["latlong_session"]
mapping_session = _region["mapping_session"]
mapping_data = _region["mapping_data"]
legend_settings = _region["legend_settings"]
region = _region["region_settings"]

# Contents of the following dirs should be copied to a results directory
# and cleaned up for the next run?

# Temporary directory for text files
TMP_DIR = pathlib.Path(__file__).parent / "tmp"
pathlib.Path(TMP_DIR).mkdir(parents=True, exist_ok=True)

# Directory for GIS output files
OUT_DIR = pathlib.Path(__file__).parent / "out"
pathlib.Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

# Directory for PNG output files
PNG_DIR = OUT_DIR / "png"
pathlib.Path(PNG_DIR).mkdir(parents=True, exist_ok=True)

# Directory for PostScript output files
PS_DIR = OUT_DIR / "postscript"
pathlib.Path(PS_DIR).mkdir(parents=True, exist_ok=True)

# Directory for report files
REPORT_DIR = OUT_DIR / "reports"
pathlib.Path(REPORT_DIR).mkdir(parents=True, exist_ok=True)

# Directory for color rule files
COLOR_DIR = pathlib.Path(__file__).parent / "color_rules"
# pathlib.Path(REPORT_DIR).mkdir(parents=True, exist_ok=True)

# Output file extensions
# See 162. Enumerations in Pybites book
PNG = "png"
PS = "ps"
EPS = "eps"
PDF = "pdf"
SVG = "svg"
SUPPORTED_FILE_TYPES = {PNG, PS}

IDW = "idw"
BSPLINE = "bspline"
INTERPOLATION_METHODS = {IDW, BSPLINE}

IMPORTED_PREFIX = "imp_"
SELECTED_PREFIX = "sel_"

IDW_PREFIX = "idw_"
BSPLINE_PREFIX = "bspline_"
INTERPOLATION_PREFIXES = {IDW_PREFIX, BSPLINE_PREFIX}

DRAPE_PREFIX = "drape_"
REGION_RASTER = "mapping_region"
NO_BG_COLOR = "none"

BASE_PAPER_SIDE = 5
