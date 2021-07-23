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
export GISRC="$HOME.grass8"
export PATH="$GISBASE/bin:$GISBASE/scripts:$PATH"
export PYTHONPATH="$GISBASE/etc/python:$PYTHONPATH"

export DYLD_LIBRARY_PATH="$GISBASE/lib:$DYLD_LIBRARY_PATH"
export LD_LIBRARY_PATH="$GISBASE/lib:$LD_LIBRARY_PATH"
export MANPATH="$MANPATH:$GISBASE/man"

export GRASS_LD_LIBRARY_PATH="$LD_LIBRARY_PATH"
export GRASS_LD_LIBRARY_PATH="$DYLD_LIBRARY_PATH"

If the GRASS libraries are shared libraries, the loader needs to be able 
to find them. This normally means that LD_LIBRARY_PATH (Linux, Solaris), 
DYLD_LIBRARY_PATH (MacOSX) or PATH (Windows) need to contain $GISBASE/lib

"""

import os
import sys
import atexit

# Could the "module level import not at top of file" be fixed using
# a different module that sets environmental variables somewhere else?
grassbin = "/Applications/GRASS-8.0.app/Contents/Resources/bin/grass"
os.environ['GRASSBIN'] = grassbin

from grass_session import Session
# see https://github.com/zarch/grass-session
# http://osgeo-org.1560.x6.nabble.com/Using-grass-libraries-in-python-outside-of-GRASS-td5442894.html
# http://osgeo-org.1560.x6.nabble.com/issue-with-grass-session-on-MacOSX-Cannot-find-GRASS-GIS-start-script-td5376619.html
import grass.script as grass

# Clenaup routine?
# See https://grasswiki.osgeo.org/wiki/Converting_Bash_scripts_to_Python

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

with Session(gisdb=gisdb, location=location, mapset=mapset):
    # run something in PERMANENT mapset:
    print(grass.parse_command("g.gisenv", flags="s"))
    grass.run_command("g.list", flags="f", type="rast,vect")

breakpoint()


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