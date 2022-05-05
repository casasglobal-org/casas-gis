import pathlib

# define GRASS DATABASE
# add your path to grassdata (GRASS GIS database) directory
gisdb = pathlib.Path.home() / "grassdata"
# the following path is the default path on MS Windows
# gisdb = os.path.join(os.path.expanduser("~"), "Documents/grassdata")
print(gisdb)
