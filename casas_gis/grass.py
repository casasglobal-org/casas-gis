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
from grass_session import Session
# see https://github.com/zarch/grass-session
# http://osgeo-org.1560.x6.nabble.com/Using-grass-libraries-in-python-outside-of-GRASS-td5442894.html
# http://osgeo-org.1560.x6.nabble.com/issue-with-grass-session-on-MacOSX-Cannot-find-GRASS-GIS-start-script-td5376619.html
import grass.script import core as gcore


# Clenaup routine?
# See https://grasswiki.osgeo.org/wiki/Converting_Bash_scripts_to_Python

# GRSASS setup:  Setup, initialization, and clean-up functions that can be
#  used in Python scripts to setup a GRASS environment and session without
#  using grassXY (i.e., hardcoding a specific GRASS version).
# https://grass.osgeo.org/grass78/manuals/libpython/script.html#module-script.setup

def main():
    """ Testing one GRASS command for setting up all required
        environment."""
    input_file = options['infile']
    imported_map = options['outmap']

    gcore.run_command("v.in.ascii",
                      input=input_file,
                      output=imported_map,
                      fs="\t", x=1, y=2, z=0)


if __name__ == "__main__":
    options, flags = grass.parser()
    main()