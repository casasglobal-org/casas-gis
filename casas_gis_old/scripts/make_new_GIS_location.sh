#!/bin/sh

#~ US-GIS

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2010 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later

#~ Rasters:
#~ US_dem US_conterm_60_315_10 natural_earth_color.composite

#~ Vectors:
#~ US_states_Mex world_bounds US_conterm_lakes_wwf

# Change mapset
g.mapset mapset=luigi2 project=AEA_US

# Copy rasters
g.copy raster=US_dem@luigi,US_dem
g.copy raster=US_conterm_60_315_10@luigi,US_conterm_60_315_10
g.copy raster=natural_earth_color.composite@luigi,natural_earth_color.composite

# Copy vectors
g.copy vector=US_states_Mex@luigi,US_states_Mex
g.copy vector=world_bounds@luigi,world_bounds
g.copy vector=US_conterm_lakes_wwf@luigi,US_conterm_lakes_wwf

exit 0
