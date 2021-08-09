""" Geospatial functionality accessed through GRASSS GIS
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

with Session(gisdb=gisdb, location=location, mapset=mapset):
    # run something in PERMANENT mapset:
    print(grass.parse_command("g.gisenv", flags="s"))
    # List GIS maps in current location
    grass.run_command("g.list", flags="f", type="vector", mapset=".")
    grass.run_command("g.remove", flags="f", type="vector", pattern="map*")
    # Import ASCII files generated in input.py module
    filename = "Olive_30set19_00002_Bloomday.txt"
    filepath = os.path.join(TMP_DIR, filename)
    mapname = os.path.splitext(os.path.basename(filepath))[0]
    grass.run_command("v.in.ascii",
                      input=os.path.join(TMP_DIR, filename),
                      output=f"map{mapname}",
                      skip=1,
                      separator='tab',
                      x=1, y=2, z=0,
                      columns=f"lon double precision, \
                          lat double precision, \
                          {mapname} double precision"
                      )
    # Check if the imported vector is there
    grass.run_command("g.list", flags="f", type="vector", mapset=".")

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