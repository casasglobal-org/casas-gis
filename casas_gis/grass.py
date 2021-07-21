""" Geospatial functionality accessed through GRASSS GIS
    https://grass.osgeo.org/grass79/manuals/libpython/index.html
    Ideas for cloud implmentation:
    https://actinia.mundialis.de/api_docs/
    https://actinia.mundialis.de/tutorial/
    https://grasswiki.osgeo.org/wiki/GRASS_and_Python
    https://baharmon.github.io/python-in-grass
    https://grasswiki.osgeo.org/wiki/GRASS_Python_Scripting_Library
    """


""" GRASS enviornment
https://grasswiki.osgeo.org/wiki/Working_with_GRASS_without_starting_it_explicitly

See also issue #15 https://github.com/luisponti/casas-gis/issues/15

export GISBASE=/Applications/GRASS-8.0.app/Contents/Resources
export GISRC=$HOME.grass8
export PATH="$GISBASE/bin:$GISBASE/scripts:$PATH"
export PYTHONPATH=

If the GRASS libraries are shared libraries, the loader needs to be able 
to find them. This normally means that LD_LIBRARY_PATH (Linux, Solaris), 
DYLD_LIBRARY_PATH (MacOSX) or PATH (Windows) need to contain $GISBASE/lib

export DYLD_LIBRARY_PATH="$GISBASE/lib:$DYLD_LIBRARY_PATH"


"""

import os
import sys
import atexit
# from grass_session import Session
# see https://github.com/zarch/grass-session
# http://osgeo-org.1560.x6.nabble.com/Using-grass-libraries-in-python-outside-of-GRASS-td5442894.html
# http://osgeo-org.1560.x6.nabble.com/issue-with-grass-session-on-MacOSX-Cannot-find-GRASS-GIS-start-script-td5376619.html
import grass.script as grass


# Clenaup routine?
# See https://grasswiki.osgeo.org/wiki/Converting_Bash_scripts_to_Python

# GRSASS setup:  Setup, initialization, and clean-up functions that can be
#  used in Python scripts to setup a GRASS environment and session without
#  using grassXY (i.e., hardcoding a specific GRASS version).
# https://grass.osgeo.org/grass78/manuals/libpython/script.html#module-script.setup

# https://grasswiki.osgeo.org/wiki/Working_with_GRASS_without_starting_it_explicitly#Python:_GRASS_GIS_7_with_existing_location

# path to the GRASS GIS launch script
# Windows
grass7path = r'C:\OSGeo4W\apps\grass\grass-7.8.dev'
grass7bin_win = r'C:\OSGeo4W\bin\grass78dev.bat'
# Linux
grass7bin_lin = 'grass78'
# MacOSX
grass7bin_mac = '/Applications/GRASS-7.9.app/'
print(grass7bin_mac)

# DATA
# define GRASS DATABASE
# add your path to grassdata (GRASS GIS database) directory
gisdb = os.path.join(os.path.expanduser("~"), "grassdata")
# the following path is the default path on MS Windows
# gisdb = os.path.join(os.path.expanduser("~"), "Documents/grassdata")
print(gisdb)


# specify (existing) location and mapset
location = "latlong_medgold"
mapset = "medgold"

# Check platform
if sys.platform.startswith('linux'):
    # we assume that the GRASS GIS start script is available and in the PATH
    # query GRASS 7 itself for its GISBASE
    grass7bin = grass7bin_lin
elif sys.platform.startswith('win'):
    grass7bin = grass7bin_win
elif sys.platform.startswith('darwin'):
    grass7bin = grass7bin_win
else:
    OSError('Platform not configured.')

print(sys.platform)

breakpoint()


def main():
    """ Run just one GRASS command to test all required environment.
    """
    input_file = options['infile']
    imported_map = options['outmap']

    grass.run_command("v.in.ascii",
                      input=input_file,
                      output=imported_map,
                      fs="\t", x=1, y=2, z=0)


if __name__ == "__main__":
    options, flags = grass.parser()
    main()