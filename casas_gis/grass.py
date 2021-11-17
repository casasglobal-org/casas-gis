""" Geospatial functionality accessed through GRASSS GIS
    https://grasswiki.osgeo.org/wiki/Category:Python
    https://grass.osgeo.org/grass79/manuals/libpython/index.html
    Ideas for cloud implmentation:
    https://actinia.mundialis.de/api_docs/
    https://actinia.mundialis.de/tutorial/
    See a also
    https://grasswiki.osgeo.org/wiki/GRASS_and_Python
    https://baharmon.github.io/python-in-grass
    https://amitness.com/2019/12/migrating-to-pathlib/
    """

import os
import pathlib

from dotenv import load_dotenv
from typing import Optional

load_dotenv()  # needed for grass_session

from grass_session import Session  # noqa E402
import grass.script as grass  # noqa E402

grassbin = os.getenv("GRASSBIN")

# Clenaup routine?
# See https://grasswiki.osgeo.org/wiki/Converting_Bash_scripts_to_Python

# Temporary directory for text files
TMP_DIR = pathlib.Path(__file__).parent / "tmp"
pathlib.Path(TMP_DIR).mkdir(parents=True, exist_ok=True)

# Directory for GIS output files
OUT_DIR = pathlib.Path(__file__).parent / "out"
pathlib.Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

# Output file extensions
# See 162. Enumerations in Pybites book
PNG = "png"
PS = "ps"
EPS = "eps"
PDF = "pdf"
SVG = "svg"

IMPORTED_PREFIX = "imp_"
NO_BG_COLOR = "none"

# DATA
# define GRASS DATABASE
# add your path to grassdata (GRASS GIS database) directory
gisdb = pathlib.Path.home().joinpath('grassdata')
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

# Add here another dictionary with GIS mapping data
# for a particular mapping session, e.g.,
mapping_data = {"digital_elevation": "elevation_1KMmd_GMTEDmd_andalusia",
                "shaded relief": "SR_HR_andalusia_clip_250m",
                "coastline": "ne_10m_coastline_andalusia",
                # etc.
                "": "",
                }


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
                      type="vector", pattern=f"{IMPORTED_PREFIX}*")


def ascii_to_vector(tmp_dir=TMP_DIR):
    """ Import ASCII files generated in input.py module
        to a vector file in a given GRASS GIS location. """
    print('\nImport text files in temporary directory to vector maps:\n')
    pathlist = pathlib.Path(tmp_dir).rglob('*.txt')
    for path in pathlist:
        filename = pathlib.Path(path).name
        mapname = pathlib.Path(path).stem
        grass.run_command("v.in.ascii",
                          input=pathlib.Path(tmp_dir).joinpath(filename),
                          output=f"{IMPORTED_PREFIX}{mapname}",
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
    pathlist = pathlib.Path(tmp_dir).rglob('*.txt')
    for path in pathlist:
        mapname = pathlib.Path(path).stem
        grass.run_command("v.proj",
                          input=f"{IMPORTED_PREFIX}{mapname}",
                          location=source_location,
                          mapset=source_mapset,
                          output=f"{IMPORTED_PREFIX}{mapname}")
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
                sql_conditions.append(f"({column_name} = '{subregion}')")
            else:
                sql_conditions.append(f"({column_name} = {subregion})")
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
        sources). Note that when crop_fraction_cap is not None, the function
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
    """ Set size of output image based on rows and colums of the GRASS
        computational region and a resolution integer value. A resolution of
        one means one pixel will be shown in the output image for each cell
        of the current GRASS region. A resolution of two will double the
        resolution. """
    # Output image size in pixels
    grass_region = grass.region()
    number_of_cols = grass_region['cols']
    number_of_rows = grass_region['rows']
    fig_width = number_of_cols * fig_resolution
    fig_height = (number_of_rows + (number_of_rows * 0.5)) * fig_resolution
    return fig_width, fig_height
    # Use frames for more deterministic location of elements such as title
    # on top and legend at bottom?


def write_psmap_instructions(outfile_name,
                             outfile_path: Optional[os.PathLike] = None):
    """ Generates text file including mapping instructions to serve as input
        to ps.map GRASS GIS command. Returns output file name with path. """
    outfile_path = OUT_DIR or outfile_path
    outfile_name = f"{outfile_name}.psmap"
    outfile = outfile_path / outfile_name
    psmap_file = f"""
border y
    color black
    width 1
    end

# Main raster
# cum_pup_tuta_nasa_gt1_shaded_relief cum_pup_tuta_nasa_eu_med_gt1
raster {mapping_data["shaded relief"]}

# Legend elements for raster
# {mapping_data["shaded relief"]}

colortable y
    raster {mapping_data["shaded relief"]}
    where 0.7 6.6
    # range 1 211
    # height 0.2
    width 2.7
    font Helvetica
    fontsize 16
    end

text 1.55% -26% cumulative pupae m^-2 y^-1
    color black
    width 1
    # background white
    fontsize 14
    ref lower left
    end

vlegend
    where 4 6.3
    border none
    font Helvetica
    fontsize 14
    width 0.7
    cols 1
    end

# Lines of general use (e.g., coastline)

vlines {mapping_data["coastline"]}
    type line
    color grey
    width 1
    lpos 0
    end

"""
    with open(outfile, 'w') as f:
        f.write(psmap_file)
    return outfile


def select_interpolation_points(digital_elevation_map,
                                altitude_cap: Optional[float] = None,
                                lower_bound: Optional[float] = None,
                                upper_bound: Optional[float] = None):
    """ Extract vector points greater than cutting point, since some values
        (e.g., bloom day <= 0) may be of little or no meaning. Enable user to
        exclude from interpolation those verctor points located at altitude
        greater than an threshold value and/or with point value point greaer
        than or equal to a threshold. """
    vector_list = grass.list_strings(type="vector",
                                     pattern=f"{IMPORTED_PREFIX}*",
                                     mapset=".")
    for vector_map in vector_list:
        grass.run_command("v.db.addcolumn",
                          map=vector_map,
                          columns="elevation double precision")
        grass.run_command("v.what.rast",
                          map=vector_map,
                          raster=digital_elevation_map,
                          column="elevation")
        sql_conditions = []
        if altitude_cap is not None:
            sql_conditions.append(f"(elevation < {altitude_cap})")
        elif upper_bound is not None:
            sql_conditions.append(f"({vector_map} <= {upper_bound})")
        elif lower_bound is not None:
            sql_conditions.append(f"({vector_map} >= {lower_bound})")
        sql_formula = " and ".join(sql_conditions)

        grass.run_command("v.extract", overwrite=True,
                          input=vector_map,
                          output=f"selected_{vector_map}",
                          where=sql_formula)

# e.g. select which points to use in mapping
# In general, do each step for all maps
# and then map them all together with d.out.file
# That way, you can get combined raster statistics
# for all rasters that will be mapped (useful for
# figure out the extent of single legend used for
# multiple maps).


def make_png_map(outfile_name,
                 fig_width,
                 fig_height,
                 bg_color: Optional[str] = None,
                 file_types: Optional[list] = None):
    """ Currently only PNG is supported (e.g., no file_types as argument). """
    background_color = bg_color or [NO_BG_COLOR]
    extensions = [PNG] if file_types is None else file_types
    for extension in extensions:
        outfile = pathlib.Path(OUT_DIR).joinpath(f"{outfile_name}.{extension}")
        grass.run_command("d.mon", overwrite=True,
                          start=extension,
                          width=fig_width,
                          height=fig_height,
                          bgcolor=background_color,
                          output=outfile)
        grass.run_command("d.rast",
                          map="elevation_1KMmd_GMTEDmd_andalusia")
        grass.run_command("d.vect",
                          map="andalusia_provinces",
                          type="boundary",
                          color="black",
                          width=3)
        # all commands but the last should have GRASS_RENDER_PS_TRAILER=FALSE
        # include more display commands here:
        grass.run_command("d.vect",
                          map="mapOlive_30set19_00002_OfPupSum",
                          type="point",
                          color="150:0:0",
                          size=20)
        grass.run_command("d.mon", stop=extension)


if __name__ == "__main__":
    # The following groups of functions may become a specialized function
    # to which a GRASS session and a dictionary of (constant?) parameters
    # are fed, so that the different current variants of the GIS scripts
    # are run transparently for e.g., Italy, Europe, North America, etc.
    with Session(**latlong_session):
        print_grass_environment()
        clean_up_vectors()
        ascii_to_vector()
        list_vector_maps()
    with Session(**mapping_session):
        list_vector_maps()
        clean_up_vectors()
        project_vector_to_current_location(
            source_location=latlong_session["location"],
            source_mapset=latlong_session["mapset"])
        set_mapping_region(map_of_subregions="andalusia_provinces",
                           column_name='iso_3166_2',
                           selected_subregions=("ES-CA,ES-H,ES-AL,ES-GR,"
                                                "ES-MA,ES-SE,ES-CO,ES-J"))
        set_crop_area("elevation_1KMmd_GMTEDmd_andalusia",
                      900,
                      "olive_HarvestedAreaFraction_andalusia",
                      0.3)
        select_interpolation_points("elevation_1KMmd_GMTEDmd_andalusia",
                                    altitude_cap=2000,
                                    lower_bound=0)
        fig_width, fig_height = set_output_image(2)
        make_png_map("test_figure",
                     fig_width,
                     fig_height)
        write_psmap_instructions("text")
