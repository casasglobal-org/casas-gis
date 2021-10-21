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

from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

load_dotenv()  # needed for grass_session

from grass_session import Session  # noqa E402
import grass.script as grass  # noqa E402

grassbin = os.getenv("GRASSBIN")

# Clenaup routine?
# See https://grasswiki.osgeo.org/wiki/Converting_Bash_scripts_to_Python

# Temporary directory for text files
TMP_DIR = os.path.join(os.getcwd(), 'casas_gis/tmp')
os.makedirs(TMP_DIR, exist_ok=True)
# Directory for GIS output files
OUT_DIR = os.path.join(os.getcwd(), 'casas_gis/out')
os.makedirs(OUT_DIR, exist_ok=True)

# DATA
# define GRASS DATABASE
# add your path to grassdata (GRASS GIS database) directory
gisdb = os.path.join(os.path.expanduser("~"), "grassdata")
# the following path is the default path on MS Windows
# gisdb = os.path.join(os.path.expanduser("~"), "Documents/grassdata")
print(gisdb)

# Specify (existing) locations and mapsets
latlong_session = {"gisdb": f"{gisdb}",
                   "location": "latlong_medgold",
                   "mapset": "medgold"}
mapping_session = {"gisdb": f"{gisdb}",
                   "location": "laea_andalusia",
                   "mapset": "medgold"}


def print_grass_environment():
    """ Print current GIS environmental variables. """
    print('\nCurrent GIS environmental variables:\n')
    grass_env = grass.parse_command("g.gisenv", flags="n")
    for key, value in grass_env.items():
        print('{:16}{}'.format(f"{key}:", value))


def list_vector_maps():
    """ List vector maps in current location. """
    grass_env = grass.parse_command("g.gisenv", flags="n")
    print(f"\nVector maps in location '{grass_env['LOCATION_NAME']}'"
          f" and mapset '{grass_env['MAPSET']}':\n")
    grass.run_command("g.list",
                      flags="p", verbose=True,
                      type="vector", mapset=".")


def clean_up_vectors():
    """ Clean up GIS files that are no longer needed. """
    print('\nRemove previously imported vector maps:\n')
    grass.run_command("g.remove",
                      flags="f", verbose=True,
                      type="vector", pattern="map*")


def ascii_to_vector(tmp_dir=TMP_DIR):
    """ Import ASCII files generated in input.py module
        to a vector file in a given GRASS GIS location. """
    print('\nImport text files in temporary directory to vector maps:\n')
    pathlist = Path(tmp_dir).rglob('*.txt')
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
                          {mapname} double precision")
    print('\nChecking if the imported vectors are there:\n')
    grass.run_command("g.list",
                      flags="p", verbose=True,
                      type="vector", mapset=".")


def project_vector_to_current_location(source_location, source_mapset,
                                       tmp_dir=TMP_DIR):
    """ Project imported vector from a latitude/longitude unprojected
        GRASS GIS location to a projected location where most GIS
        processing including mapping will occurr. """
    print('\nProject imported vectors to mappinsg location:\n')
    pathlist = Path(tmp_dir).rglob('*.txt')
    for path in pathlist:
        mapname = os.path.splitext(os.path.basename(path))[0]
        grass.run_command("v.proj",
                          input=f"map{mapname}",
                          location=source_location,
                          mapset=source_mapset,
                          output=f"map{mapname}")
    print('\nChecking if the imported vectors are there:\n')
    grass.run_command("g.list",
                      flags="p", verbose=True,
                      type="vector", mapset=".")


def set_mapping_region(map_of_subregions,
                       column_name,
                       selected_subregions: Optional[str] = None):
    """ Define GRASS GIS region for computations mapping, including
        geographical extent and spatial resolution.
        The 'field type' argumeent can be 'CHARACTER' or 'INTEGER' """
    if selected_subregions is not None:
        list_of_selected_subregions = selected_subregions.split(",")
        sql_conditions = []
        columns = grass.vector_columns(map_of_subregions, getDict=True)
        column_type = columns[column_name]['type']
        for subregion in list_of_selected_subregions:
            if column_type == "CHARACTER":
                sql_conditions.append(f"({column_name}='{subregion}')")
            else:
                sql_conditions.append(f"({column_name}={subregion})")
        sql_formula = " or ".join(sql_conditions)
        grass.run_command("v.extract", overwrite=True,
                          input=map_of_subregions,
                          output="selected_region",
                          where=sql_formula)
        map_of_subregions = "selected_region"
    grass.run_command("g.region",
                      vector=map_of_subregions)
    grass.run_command("v.to.rast", overwrite=True,
                      input=map_of_subregions,
                      output="mapping_region",
                      use="val",
                      value=1)
    grass.run_command("g.region",
                      n="n+7000", s="s-7000", e="e+7000", w="w-7000")
    grass.run_command("g.region", res=1000, flags="a")
    # Return “g.region -gu” as a dictionary
    grass_region = grass.region()
    print(grass_region)


def set_crop_area(digital_elevation_map,
                  max_altitude,
                  crop_area: Optional[str] = None,
                  crop_fraction_cap: Optional[float] = None):
    """ Use various olive growing areas for masking model output (i.e., map
        model output only inside olive growing areas obtained from various
        sources. Note that when crop_fraction_cap is not None, the function
        will look for a crop_area raster map where each cell value is the
        fraction of area in that cell that is covered by a certain crop. """
    if crop_area is None:
        # Just use the whole mapping region from set_mapping_region()
        calc_expression_crop = ("mask_crop = if ((mapping_region,")
    if (crop_area is not None) and (crop_fraction_cap is not None):
        # Select cells where land fraction covered by crop is above cap
        calc_expression_crop = ("mask_crop = if ((mapping_region &&"
                                f" {crop_area} > {crop_fraction_cap}),")
    else:
        # Select cells where crop is present (value = 1)
        calc_expression_crop = ("mask_crop = if ((mapping_region &&"
                                f" {crop_area} == 1),")
    # Put altitude values in crop area selected above, otherwise no data.
    calc_expression_crop += f" {digital_elevation_map}, null())"
    grass.mapcalc(calc_expression_crop, overwrite=True)
    calc_expression_altitude = ("mask_crop_elevation ="
                                f" if (mask_crop < {max_altitude}, mask_crop,"
                                " null())")
    grass.mapcalc(calc_expression_altitude, overwrite=True)


def set_output_image(fig_resolution):
    """Set size of output image based on the size of the GIS computational
    region and a resolution integer value. Resolution = 1 mean """
    # Output image size in pixels
    grass_region = grass.region()
    number_of_cols = grass_region['cols']
    number_of_rows = grass_region['rows']
    # header = footer = number_of_rows * 0.15
    fig_width = number_of_cols * fig_resolution
    fig_height = (number_of_rows + (number_of_rows * 0.5)) * fig_resolution
    return fig_width, fig_height
    # Display driver variables
    # os.environ['GRASS_FONT'] = 'Arial'
    # os.environ['GRASS_RENDER_TEXT_SIZE'] = 12
    # file_extensions = [".png", ".ps", ".pdf", ".svg"]
    # Output file -- needs to be moved to a different function
    # outfile = os.path.join(OUT_DIR, f"{outfile_name}.png")
    # os.environ['GRASS_RENDER_FILE'] = outfile


# e.g. select which points to use in mapping
# In general, do each step for all maps
# and then map them all together with d.out.file
# That way, you can get combined raster statistics
# for all rasters that will be mapped (useful for
# figure out extent of single legend).

# e.g. select which points to use in mapping
# In general, do each step for all maps
# and then map them all together with d.out.file
# That way, you can get combined raster statistics
# for all rasters that will be mapped (useful for
# figure out extent of single legend).


def make_map(outfile_name,
             fig_width,
             fig_height,
             bg_color: Optional[str] = None,
             file_types: Optional[str] = None):
    background_color = ["none"] if bg_color is None else bg_color
    extensions = ["png"] if file_types is None else file_types.split(",")
    for extension in extensions:
        outfile = os.path.join(OUT_DIR, f"{outfile_name}.{extension}")
        grass.run_command("d.mon", overwrite=True,
                          start="cairo",
                          width=fig_width,
                          height=fig_height,
                          bgcolor=background_color,
                          output=outfile)
        grass.run_command("d.rast",
                          map="elevation_1KMmd_GMTEDmd_andalusia")
        # all other display commands
        grass.run_command("d.mon", stop="cairo")


if __name__ == "__main__":
    # with Session(**latlong_session):
    #     print_grass_environment()
    #     clean_up_vectors()
    #     ascii_to_vector()
    #     list_vector_maps()
    with Session(**mapping_session):
        # list_vector_maps()
        # clean_up_vectors()
        # project_vector_to_current_location(
        #     source_location=latlong_session["location"],
        #     source_mapset=latlong_session["mapset"])
        set_mapping_region(map_of_subregions="andalusia_provinces",
                           column_name='iso_3166_2',
                           selected_subregions=("ES-CA,ES-H,ES-AL,ES-GR,"
                                                "ES-MA,ES-SE,ES-CO,ES-J"))
        set_crop_area("elevation_1KMmd_GMTEDmd_andalusia",
                      900,
                      "olive_HarvestedAreaFraction_andalusia",
                      0.3)
        fig_width, fig_height = set_output_image(2)
        make_map("test_figure",
                 fig_width,
                 fig_height,
                 file_types="png,ps,pdf")
