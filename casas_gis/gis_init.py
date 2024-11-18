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

import pathlib

# define GRASS DATABASE
# add your path to grassdata (GRASS GIS database) directory
gisdb = pathlib.Path.home() / "grassdata"
# the following path is the default path on MS Windows
# gisdb = os.path.join(os.path.expanduser("~"), "Documents/grassdata")
print(gisdb)
