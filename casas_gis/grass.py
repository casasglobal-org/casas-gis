""" Geospatial functionality accessed through GRASSS GIS
    https://grass.osgeo.org/grass79/manuals/libpython/index.html 
    Ideas for cloud implmentation:
    https://actinia.mundialis.de/api_docs/
    https://actinia.mundialis.de/tutorial/
    https://grasswiki.osgeo.org/wiki/GRASS_and_Python
    """
import os
import sys
import atexit
import grass.script as gs


# Clenaup routine?
# See https://grasswiki.osgeo.org/wiki/Converting_Bash_scripts_to_Python

# GRSASS setup:  Setup, initialization, and clean-up functions that can be
#  used in Python scripts to setup a GRASS environment and session without
#  using grassXY (i.e., hardcoding a specific GRASS version).
# https://grass.osgeo.org/grass78/manuals/libpython/script.html#module-script.setup

v.in.ascii input=$i output=map$i fs='\t' x=1 y=2 z=0