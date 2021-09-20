""" Geospatial functionality accessed through GRASSS GIS
    https://grasswiki.osgeo.org/wiki/Category:Python
    https://grass.osgeo.org/grass79/manuals/libpython/index.html
    Ideas for cloud implmentation:
    https://actinia.mundialis.de/api_docs/
    https://actinia.mundialis.de/tutorial/
    See a also
    https://grasswiki.osgeo.org/wiki/GRASS_and_Python
    https://baharmon.github.io/python-in-grass
    """

import os
import sys

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()  # needed for grass_session

from grass_session import Session  # noqa E402
import grass.script as grass  # noqa E402

grassbin = os.getenv("GRASSBIN")

# Clenaup routine?
# See https://grasswiki.osgeo.org/wiki/Converting_Bash_scripts_to_Python

TMP_DIR = os.path.join(os.getcwd(), 'casas_gis/tmp')
os.makedirs(TMP_DIR, exist_ok=True)

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


def print_grass_environment(gisdb, location, mapset):
    """ Print current GIS environmental variables. """
    with Session(gisdb=gisdb, location=location, mapset=mapset):
        print('\nCurrent GIS environmental variables:\n')
        print(grass.parse_command("g.gisenv", flags="s"))


def list_vector_maps(gisdb, location, mapset):
    """ List vector maps in current location. """
    with Session(gisdb=gisdb, location=location, mapset=mapset):
        print('\nVector maps in current location and mapset:\n')
        grass.run_command("g.list",
                          flags="p", verbose=True,
                          type="vector", mapset="."
                          )


def clean_up_vectors(gisdb, location, mapset):
    """ Clean up GIS files that are no longer needed. """
    with Session(gisdb=gisdb, location=location, mapset=mapset):
        print('\nRemove previously imported vector maps:\n')
        grass.run_command("g.remove",
                          flags="f", verbose=True,
                          type="vector", pattern="map*"
                          )


def ascii_to_vector(gisdb, location, mapset, tmp_dir=TMP_DIR):
    """ Import ASCII files generated in input.py module
        to a vector file in a given GRASS GIS location. """
    with Session(gisdb=gisdb, location=location, mapset=mapset):
        print('\nImport text files in temporary directory to vector maps:\n')
        pathlist = Path(TMP_DIR).rglob('*.txt')
        for path in pathlist:
            filename = os.path.basename(path)
            mapname = os.path.splitext(os.path.basename(path))[0]
            grass.run_command("v.in.ascii",
                              input=os.path.join(tmp_dir, filename),
                              output=f"map{mapname}",
                              skip=1,
                              separator='tab',
                              x=1, y=2, z=0,
                              columns=f"lon double precision, \
                                lat double precision, \
                                {mapname} double precision"
                              )
        print('\nChecking if the imported vectors are there:\n')
        grass.run_command("g.list",
                          flags="p", verbose=True,
                          type="vector", mapset=".")


if __name__ == "__main__":
    print_grass_environment(gisdb, location, mapset)
    clean_up_vectors(gisdb, location, mapset)
    ascii_to_vector(gisdb, location, mapset, tmp_dir=TMP_DIR)
    list_vector_maps(gisdb, location, mapset)
