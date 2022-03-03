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
import pandas as pd

from dotenv import load_dotenv
from typing import Optional
from io import StringIO

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

# Directory for report files
REPORT_DIR = OUT_DIR / "reports"
pathlib.Path(REPORT_DIR).mkdir(parents=True, exist_ok=True)


# Output file extensions
# See 162. Enumerations in Pybites book
PNG = "png"
PS = "ps"
EPS = "eps"
PDF = "pdf"
SVG = "svg"
SUPPORTED_FILE_TYPES = {PNG, PS}

IDW = "idw"
BSPLINE = "bspline"
INTERPOLATION_METHODS = {IDW, BSPLINE}

IMPORTED_PREFIX = "imp_"
SELECTED_PREFIX = "sel_"
IDW_PREFIX = "idw_"
BSPLINE_PREFIX = "bspline_"
REGION_RASTER = "mapping_region"
NO_BG_COLOR = "none"

# DATA
# define GRASS DATABASE
# add your path to grassdata (GRASS GIS database) directory
gisdb = pathlib.Path.home() / "grassdata"
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


def write_psmap_instructions(interpolated_raster: str,
                             selected_points: str,
                             outfile_name: str,
                             outfile_path: Optional[os.PathLike] = None):
    """ Generates text file including mapping instructions to serve as input
        to ps.map GRASS GIS command. Returns output file name with path. """
    outfile_path = PS_DIR or outfile_path
    outfile_name = f"{outfile_name}.psmap"
    outfile = outfile_path / outfile_name
    psmap_file = f"""# GRASS GIS ps.map instruction file
border y
    color black
    width 1
    end

# Main raster
raster {interpolated_raster}

# Some boundary lines
vlines {mapping_data["coastline"]}
    type line
    color grey
    width 1
    lpos 0
    end

# Input points
vpoints {selected_points}
    type point
    color white
    fcolor black
    width 0.5
    symbol basic/circle
    size 7
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
    raster_stats = {}
    max_values = []
    min_values = []
    for vector_map in vector_list:
        map_name = vector_map.split("@")[0]
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
        # Clip interpolated raster to mapping region using map
        # calculator becuase r.mask does not work with v.surf.idw
        # see https://trac.osgeo.org/grass/ticket/3363
        calc_expression_mask = (f"{output_map} = "
                                f"if ({REGION_RASTER}, {output_map}, null())")
        grass.mapcalc(calc_expression_mask, overwrite=True)
        raster_stats[output_map] = grass.parse_command("r.univar",
                                                       flags=("ge"),
                                                       map=output_map)
        max_values.append(raster_stats[output_map]["max"])
        min_values.append(raster_stats[output_map]["min"])
    abs_max_idw = max(max_values)
    abs_min_idw = min(min_values)
    # This is testing code that may go away at some point
    print("Absolute (idw) raster max is ", max(max_values))
    print("Absolute (idw) raster min is ", min(min_values))

    return abs_max_idw, abs_min_idw


def interpolate_points_bspline(vector_layer: Optional[str] = "1",
                               avg_west_distance: Optional[float] = None,
                               avg_north_distance: Optional[float] = None,
                               method: Optional[str] = "bicubic",
                               smoothing_parameter: Optional[float] = None):
    """ Generate interpolated raster surface from vector point data based on
        bicubic or bilinear spline interpolation with Tykhonov regularization
        using v.surf.bspline GRASS GIS command. See also
        https://lists.osgeo.org/pipermail/grass-user/2010-February/054868.html
        """
    vector_list = grass.list_strings(type="vector",
                                     pattern=f"{SELECTED_PREFIX}*",
                                     mapset=".")
    compute_distance_between_points = (avg_west_distance or
                                       avg_north_distance) is None
    compute_smoothing_parameter = smoothing_parameter is None
    raster_stats = {}
    max_values = []
    min_values = []
    for vector_map in vector_list:
        map_name = vector_map.split("@")[0]
        base_map_name = map_name.replace(SELECTED_PREFIX, "", 1)
        output_map = map_name.replace(SELECTED_PREFIX,
                                      BSPLINE_PREFIX, 1)
        if compute_distance_between_points:
            distance_pair = get_distance_points_bspline(
                input_vector_map=vector_map,
                output_raster_map=output_map,
                column_name=base_map_name)
            avg_west_distance, avg_north_distance = distance_pair
        if compute_smoothing_parameter:
            smoothing_parameter = cross_validate_bspline(
                input_vector_map=vector_map,
                output_raster_map=output_map,
                column_name=base_map_name,
                avg_west_distance=avg_west_distance,
                avg_north_distance=avg_north_distance,
                method=method,
                vector_layer=vector_layer)
        grass.run_command("v.surf.bspline", overwrite=True,
                          verbose=True,
                          input=vector_map,
                          layer=vector_layer,
                          column=base_map_name,
                          raster_output=output_map,
                          mask=REGION_RASTER,
                          ew_step=avg_west_distance,
                          ns_step=avg_north_distance,
                          method=method,
                          lambda_i=smoothing_parameter)
        # Remember to implement min-max check (lines 620-630 in gis script).
        vector_stats = grass.parse_command("v.univar",
                                           flags=("ge"),
                                           map=vector_map,
                                           layer=vector_layer,
                                           type="point",
                                           column=base_map_name)
        vector_max = vector_stats["max"]
        vector_min = vector_stats["min"]
        calc_expression_minmax = (f"{output_map} = "
                                  f"if (({output_map} < {vector_max}) && "
                                  f"({output_map} > {vector_min}), "
                                  f"{output_map}, null())")
        grass.mapcalc(calc_expression_minmax, overwrite=True)
        raster_stats[output_map] = grass.parse_command("r.univar",
                                                       flags=("ge"),
                                                       map=output_map)
        max_values.append(raster_stats[output_map]["max"])
        min_values.append(raster_stats[output_map]["min"])
    abs_max_bspline = max(max_values)
    abs_min_bspline = min(min_values)
    # This is testing code that may go away at some point
    print("Absolute (bspline) raster max is ", abs_max_bspline)
    print("Absolute (bspline) raster min is ", abs_min_bspline)

    return abs_max_bspline, abs_min_bspline


def get_distance_points_bspline(input_vector_map: str,
                                output_raster_map: str,
                                column_name: str,
                                vector_layer: Optional[str] = "1"):
    """ Run v.surf.bspline with the -e flag first to get estimated mean
        distance between points. That needs to be multiplied by two and
        assigned to ew_step and ns_step. """
    distance_output = grass.read_command("v.surf.bspline",
                                         overwrite=True,
                                         flags="e",
                                         input=input_vector_map,
                                         layer=vector_layer,
                                         column=column_name,
                                         raster_output=output_raster_map)
    distance = distance_output.split()
    # use tuple unpacking? (Bob 2021-12-15)
    decimal_distance = float(distance[-1])
    avg_west_distance = avg_north_distance = decimal_distance * 2
    return avg_west_distance, avg_north_distance


def cross_validate_bspline(input_vector_map: str,
                           output_raster_map: str,
                           column_name: str,
                           avg_west_distance: float,
                           avg_north_distance: float,
                           method: str,
                           vector_layer: Optional[str] = "1"):
    """ Run v.surf.bspline with the -c flag to find the best Tykhonov
        regularizing parameter using a "leave-one-out" cross validation
        method, and assign the resulting value to lambda_i (smoothing). """
    cross_validation_output = grass.read_command(
        "v.surf.bspline",
        overwrite=True,
        flags="c",
        input=input_vector_map,
        layer=vector_layer,
        column=f"{column_name}",
        raster_output=output_raster_map,
        mask=REGION_RASTER,
        ew_step=avg_west_distance,
        ns_step=avg_north_distance,
        method=method)
    # https://stackoverflow.com/a/22605281
    cross_validation_text_buffer = StringIO(cross_validation_output)
    cross_validation_df = pd.read_csv(
        cross_validation_text_buffer, sep='|')
    # https://stackoverflow.com/a/21607530
    cross_validation_df = cross_validation_df.rename(
        columns=lambda x: x.strip())
    # https://stackoverflow.com/a/61801746
    minimizer_column = "rms"
    smoothing_parameter = cross_validation_df.loc[
        cross_validation_df[minimizer_column].idxmin()]["lambda"]
    # Print cross validation report
    outfile_path = REPORT_DIR
    outfile_name = f"{column_name}_cross_validation.txt"
    outfile = outfile_path / outfile_name
    cross_validation_output = (
        "Cross validation for\new_step (average west distance) = "
        f"{avg_west_distance} and\n"
        "ns_step (average west distance) = "
        f"{avg_north_distance}\n"
        "Selected lambda_i (smoothing parameter) = "
        f"{smoothing_parameter} (minimizes {minimizer_column})\n\n"
        f"{cross_validation_output}")
    with open(outfile, 'w') as f:
        f.write(cross_validation_output)
    return smoothing_parameter


# In general, do each step for all maps
# and then map them all together with d.out.file
# That way, you can get combined raster statistics
# for all rasters that will be mapped (useful for
# figuring out the extent of single legend used for
# multiple maps).


def make_maps(fig_width: float,
              fig_height: float,
              background_color: Optional[str] = NO_BG_COLOR,
              file_types: Optional[list] = None,
              interpolation_method: Optional[str] = None):
    """ Currently only png and ps (PostScript) formats are supported. """
    try:
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
            make_png_maps(extension=extension,
                          fig_width=fig_width,
                          fig_height=fig_height,
                          background_color=background_color)
        elif extension == "ps":
            make_ps_maps(extension=extension)

        # draw_map_legend() here ???
        # See func def below


def make_png_maps(extension: str,
                  fig_width: float,
                  fig_height: float,
                  background_color: Optional[str] = NO_BG_COLOR):
    """ Cycle through interpolated surfaces and generate maps. """
    mapping_mapset = mapping_session["mapset"]
    sel_vector_list = get_map_list_from_pattern(
        map_type="vector",
        pattern="sel_*",
        mapping_mapset=mapping_mapset)
    idw_rasters_list = get_map_list_from_pattern(
        map_type="raster",
        pattern="idw_*",
        mapping_mapset=mapping_mapset)
    bspline_rasters_list = get_map_list_from_pattern(
        map_type="raster",
        pattern="bspline_*",
        mapping_mapset=mapping_mapset)
    # The two for loops could be one function?
    for idw_raster, sel_vector in zip(idw_rasters_list, sel_vector_list):
        outfile = PNG_DIR / f"{idw_raster}.{extension}"
        grass.run_command("d.mon", overwrite=True,
                          start=extension,
                          width=fig_width,
                          height=fig_height,
                          bgcolor=background_color,
                          output=outfile)
        grass.run_command("d.his",
                          i="SR_HR_andalusia_clip_250m",
                          h=idw_raster)
        grass.run_command("d.vect",
                          map="andalusia_provinces",
                          type="boundary",
                          color="black",
                          width=3)
        grass.run_command("d.vect",
                          map=sel_vector,
                          type="point",
                          color="white",
                          fill_color="black",
                          icon="basic/point",
                          size=15,
                          width=2)
        # Legned?
        grass.run_command("d.mon", stop=extension)
    for bspline_raster, sel_vector in zip(bspline_rasters_list,
                                          sel_vector_list):
        outfile = PNG_DIR / f"{bspline_raster}.{extension}"
        grass.run_command("d.mon", overwrite=True,
                          start=extension,
                          width=fig_width,
                          height=fig_height,
                          bgcolor=background_color,
                          output=outfile)
        grass.run_command("d.his",
                          i="SR_HR_andalusia_clip_250m",
                          h=bspline_raster)
        grass.run_command("d.vect",
                          map="andalusia_provinces",
                          type="boundary",
                          color="black",
                          width=3)
        grass.run_command("d.vect",
                          map=sel_vector,
                          type="point",
                          color="white",
                          fill_color="black",
                          icon="basic/point",
                          size=15,
                          width=2)
        # Legned?
        grass.run_command("d.mon", stop=extension)


def make_ps_maps(extension: str):
    """ Cycle through interpolated surfaces and generate maps. """
    mapping_mapset = mapping_session["mapset"]
    idw_rasters_list = get_map_list_from_pattern(
        map_type="raster",
        pattern="idw_*",
        mapping_mapset=mapping_mapset)
    bspline_rasters_list = get_map_list_from_pattern(
        map_type="raster",
        pattern="bspline_*",
        mapping_mapset=mapping_mapset)
    sel_vector_list = get_map_list_from_pattern(
        map_type="vector",
        pattern="sel_*",
        mapping_mapset=mapping_mapset)
    for idw_raster, sel_vector in zip(idw_rasters_list, sel_vector_list):
        outfile = PS_DIR / f"{idw_raster}.{extension}"
        ps_instructions_file = write_psmap_instructions(
            interpolated_raster=idw_raster,
            selected_points=sel_vector,
            outfile_name=idw_raster)
        grass.run_command("ps.map", overwrite=True,
                          flags="e",
                          input=ps_instructions_file,
                          output=outfile)
    for bspline_raster, sel_vector in zip(bspline_rasters_list,
                                          sel_vector_list):
        outfile = PS_DIR / f"{bspline_raster}.{extension}"
        ps_instructions_file = write_psmap_instructions(
            interpolated_raster=bspline_raster,
            selected_points=sel_vector,
            outfile_name=bspline_raster)
        grass.run_command("ps.map", overwrite=True,
                          flags="e",
                          input=ps_instructions_file,
                          output=outfile)


def get_map_list_from_pattern(map_type: str,
                              pattern: str,
                              mapping_mapset: str):
    map_dict = grass.list_grouped(type=map_type, pattern=pattern)
    return map_dict[f"{mapping_mapset}"]


def draw_map_legend(extension: str,
                    ):
    if extension == "png":
        pass

    elif extension == "ps":
        pass


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
                                   method="bicubic")
        fig_width, fig_height = set_output_image(2)
        make_maps(fig_width,
                  fig_height,
                  file_types=["png", "ps"])
