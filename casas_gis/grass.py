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

# Directory for PNG output files
PNG_DIR = OUT_DIR / "png"
pathlib.Path(PNG_DIR).mkdir(parents=True, exist_ok=True)

# Directory for PostScript output files
PS_DIR = OUT_DIR / "postscript"
pathlib.Path(PS_DIR).mkdir(parents=True, exist_ok=True)

# Output file extensions
# See 162. Enumerations in Pybites book
PNG = "png"
PS = "ps"
EPS = "eps"
PDF = "pdf"
SVG = "svg"
SUPPORTED_FILE_TYPES = {PNG, PS}

IMPORTED_PREFIX = "imp_"
SELECTED_PREFIX = "sel_"
IDW_PREFIX = "idw_"
BSPLINE_PREFIX = "bspline_"
REGION_RASTER = "mapping_region"
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
                "test_interpolation": "bspline_Olive_30set19_00002_OfPupSum",
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
    grass.run_command("g.remove",
                      flags="f", verbose=True,
                      type="vector", pattern=f"{SELECTED_PREFIX}*")


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
    grass.run_command("g.region",
                      n="n+7000", s="s-7000", e="e+7000", w="w-7000")
    grass.run_command("g.region", res=1000, flags="a")
    grass.run_command("v.to.rast", overwrite=True,
                      input=map_of_subregions,
                      output=REGION_RASTER,
                      use="val",
                      value=1)
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
        calc_expression_crop = (f"mask_crop = if (({REGION_RASTER},")
    if (crop_area is not None) and (crop_fraction_cap is not None):
        # Select cells where land fraction covered by crop is above cap
        calc_expression_crop = (f"mask_crop = if (({REGION_RASTER} &&"
                                f" {crop_area} > {crop_fraction_cap}),")
    else:
        # Select cells where crop is present (value = 1)
        calc_expression_crop = (f"mask_crop = if (({REGION_RASTER} &&"
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
    psmap_file = f"""# GRASS GIS ps.map instruction file
border y
    color black
    width 1
    end

# Main raster
raster {mapping_data["test_interpolation"]}

# Some boundary lines
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
        greater than an threshold value and/or with point value greather than
        or equal to a threshold. """
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
        output_map = vector_map.replace(IMPORTED_PREFIX,
                                        SELECTED_PREFIX, 1)
        grass.run_command("v.extract", overwrite=True,
                          input=vector_map,
                          output=output_map,
                          where=sql_formula)


def interpolate_points_idw(vector_layer: Optional[str] = 1,
                           number_of_points: Optional[int] = 3,
                           power: Optional[float] = 2.0):
    """ Generate interpolated raster surface from vector point data based on
        inverse distance weighting using v.surf.idw GRASS GIS command. """
    vector_list = grass.list_strings(type="vector",
                                     pattern=f"{SELECTED_PREFIX}*",
                                     mapset=".")
    # Clip interpolated raster to mapping region
    grass.run_command("g.copy", overwrite=True,
                      rast=(REGION_RASTER, "MASK"))
    for vector_map in vector_list:
        map_name, mapset_name = vector_map.split("@")
        base_map_name = map_name.replace(SELECTED_PREFIX, "", 1)
        output_map = map_name.replace(SELECTED_PREFIX,
                                      IDW_PREFIX, 1)
        grass.run_command("v.surf.idw", overwrite=True,
                          flags="n",
                          input=vector_map,
                          layer=vector_layer,
                          column=f"{base_map_name}",
                          output=output_map,
                          npoints=number_of_points,
                          power=power)
    grass.run_command("g.remove",
                      flags="f",
                      type="raster",
                      name="MASK")


def interpolate_points_bspline(vector_layer: Optional[str] = "1",
                               ew_step: Optional[float] = None,
                               ns_step: Optional[float] = None,
                               method: Optional[str] = "bicubic",
                               lambda_i: Optional[float] = None):
    """ Generate interpolated raster surface from vector point data based on
        bicubic or bilinear spline interpolation with Tykhonov regularization
        using v.surf.bspline GRASS GIS command. """
    vector_list = grass.list_strings(type="vector",
                                     pattern=f"{SELECTED_PREFIX}*",
                                     mapset=".")
    for vector_map in vector_list:
        map_name = vector_map.split("@")[0]
        base_map_name = map_name.replace(SELECTED_PREFIX, "", 1)
        output_map = map_name.replace(SELECTED_PREFIX,
                                      BSPLINE_PREFIX, 1)
        if ew_step or ns_step is None:
            # https://lists.osgeo.org/pipermail/grass-user/2010-February/054868.html
            # https://grass.osgeo.org/grass80/manuals/v.surf.bspline.html
            # 1. run v.surf.bspline with the -e flag first to get estimated
            #    mean distance between points. That needs to be multiplied by
            #    two and assigned to ew_step and ns_step
            distance_output = grass.read_command("v.surf.bspline",
                                                 overwrite=True,
                                                 flags="e",
                                                 input=vector_map,
                                                 layer=vector_layer,
                                                 column=f"{base_map_name}",
                                                 raster_output=output_map)
            distance = distance_output.split()
            decimal_distance = float(distance[-1])
            ew_step = ns_step = decimal_distance * 2
        # 2. run v.surf.bspline with the -c flag to find the best Tykhonov
        #    regularizing parameter using a "leave-one-out" cross validation
        #    method, and assign the resulting value to lambda_i
        grass.run_command("v.surf.bspline", overwrite=True,
                          input=vector_map,
                          layer=vector_layer,
                          column=f"{base_map_name}",
                          raster_output=output_map,
                          mask=REGION_RASTER,
                          ew_step=ew_step,
                          ns_step=ns_step,
                          method=method,
                          lambda_i=lambda_i)
        print("distance:", ew_step, ns_step)
        # Remember to implement min-max check (lines 620-630 in gis script).


def get_distance_points_bspline(vector_layer: Optional[str] = "1"):
    """ Run v.surf.bspline with the -e flag first to get estimated mean
        distance between points. That needs to be multiplied by two and
        assigned to ew_step and ns_step. """
    pass


def cross_validate_bspline(vector_layer: Optional[str] = None,
                           method: Optional[str] = None):
    """ Run v.surf.bspline with the -c flag to find the best Tykhonov
        regularizing parameter using a "leave-one-out" cross validation
        method, and assign the resulting value to lambda_i. """
    # Parse cross-validation output e.g. by line and get key param values
    # into a list so that it can be selected by an algo such as min
    pass

# e.g. select which points to use in mapping
# In general, do each step for all maps
# and then map them all together with d.out.file
# That way, you can get combined raster statistics
# for all rasters that will be mapped (useful for
# figure out the extent of single legend used for
# multiple maps).


def make_map(outfile_name: str,
             fig_width: float,
             fig_height: float,
             background_color: Optional[str] = NO_BG_COLOR,
             file_types: Optional[list] = None):
    """ Currently only png and ps (PostScript) formats are supported. """
    try:
        # if len(SUPPORTED_FILE_TYPES & set(file_types)) < len(file_types):
        if any(f not in SUPPORTED_FILE_TYPES for f in file_types):
            raise NotImplementedError("\nNot implemented error:\n"
                                      "Only PNG and PostScript output"
                                      " is implmenented!\n"
                                      "Please select PNG and/or PostScript"
                                      " output.\n")
    except NotImplementedError as nie:
        print(nie)
    extensions = [PNG] if file_types is None else file_types
    for extension in extensions:
        if extension == "png":
            outfile = PNG_DIR / f"{outfile_name}.{extension}"
            grass.run_command("d.mon", overwrite=True,
                              start=extension,
                              width=fig_width,
                              height=fig_height,
                              bgcolor=background_color,
                              output=outfile)
            grass.run_command("d.his",
                              i="SR_HR_andalusia_clip_250m",
                              h="bspline_Olive_30set19_00002_OfPupSum")
            grass.run_command("d.vect",
                              map="andalusia_provinces",
                              type="boundary",
                              color="black",
                              width=3)
            grass.run_command("d.vect",
                              map="mapOlive_30set19_00002_OfPupSum",
                              type="point",
                              color="white",
                              fill_color="black",
                              icon="basic/point",
                              size=15,
                              width=2)
            grass.run_command("d.mon", stop=extension)
        elif extension == "ps":
            outfile = PS_DIR / f"{outfile_name}.{extension}"
            ps_instructions_file = write_psmap_instructions("test")
            grass.run_command("ps.map", overwrite=True,
                              flags="e",
                              input=ps_instructions_file,
                              output=outfile)
            outfile.rename(outfile.with_suffix(".eps"))


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
        interpolate_points_idw(vector_layer=1,
                               number_of_points=3,
                               power=2.0)
        interpolate_points_bspline(vector_layer=1,
                                   method="bicubic",
                                   lambda_i=0.01)
        fig_width, fig_height = set_output_image(2)
        make_map("test_figure",
                 fig_width,
                 fig_height,
                 file_types=["png", "ps"])
