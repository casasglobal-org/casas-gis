#!/bin/sh

#~ US-GIS

#~ Rasters:
#~ US_dem US_conterm_60_315_10 natural_earth_color.composite

#~ Vectors:
#~ US_states_Mex world_bounds US_conterm_lakes_wwf

# Change mapset
g.mapset mapset=luigi2 location=AEA_US

# Copy rasters
g.copy rast=US_dem@luigi,US_dem
g.copy rast=US_conterm_60_315_10@luigi,US_conterm_60_315_10
g.copy rast=natural_earth_color.composite@luigi,natural_earth_color.composite

# Copy vectors
g.copy vect=US_states_Mex@luigi,US_states_Mex
g.copy vect=world_bounds@luigi,world_bounds
g.copy vect=US_conterm_lakes_wwf@luigi,US_conterm_lakes_wwf

exit 0
