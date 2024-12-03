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

""" Color related stuff.
    Select color scheme, adjust to data, etc."""

# https://matplotlib.org/stable/tutorials/colors/colormaps.html
# https://colorcet.holoviz.org/
# https://jiffyclub.github.io/palettable/
# https://seaborn.pydata.org/

import constants as k

import grass.script as grass  # noqa E402


def set_color_rule(raster_map: str,
                   color_rule: str):
    grass.run_command("r.colors",
                      # flags="ge",
                      map=raster_map,
                      rules=k.COLOR_DIR / color_rule)
