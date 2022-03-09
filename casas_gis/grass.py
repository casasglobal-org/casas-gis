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
import constants as k
import cleanup
import interpolation as surf

from dotenv import load_dotenv
from typing import Optional

load_dotenv()  # needed for grass_session

from grass_session import Session  # noqa E402
import grass.script as grass  # noqa E402

grassbin = os.getenv("GRASSBIN")


def ascii_to_vector(tmp_dir=k.TMP_DIR):
    """ Import ASCII files generated in input.py module
        to a vector file in a given GRASS GIS location. """
    print('\nImport text files in temporary directory to vector maps:\n')
    pathlist = pathlib.Path(tmp_dir).rglob('*.txt')
    for path in pathlist:
        filename = pathlib.Path(path).name
        mapname = pathlib.Path(path).stem
        grass.run_command("v.in.ascii",
                          input=pathlib.Path(tmp_dir).joinpath(filename),
                          output=f"{k.IMPORTED_PREFIX}{mapname}",
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
                                       tmp_dir=k.TMP_DIR):
    """ Project imported vector from a latitude/longitude unprojected
        GRASS GIS location to a projected location where most GIS
        processing including mapping will occurr. """
    print('\nProject imported vectors to mappinsg location:\n')
    pathlist = pathlib.Path(tmp_dir).rglob('*.txt')
    for path in pathlist:
        mapname = pathlib.Path(path).stem
        grass.run_command("v.proj",
                          input=f"{k.IMPORTED_PREFIX}{mapname}",
                          location=source_location,
                          mapset=source_mapset,
                          output=f"{k.IMPORTED_PREFIX}{mapname}")
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
                      output=k.REGION_RASTER,
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
        calc_expression_crop = (f"mask_crop = if (({k.REGION_RASTER},")
    if (crop_area is not None) and (crop_fraction_cap is not None):
        # Select cells where land fraction covered by crop is above cap
        calc_expression_crop = (f"mask_crop = if (({k.REGION_RASTER} &&"
                                f" {crop_area} > {crop_fraction_cap}),")
    else:
        # Select cells where crop is present (value = 1)
        calc_expression_crop = (f"mask_crop = if (({k.REGION_RASTER} &&"
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
    outfile_path = k.PS_DIR or outfile_path
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
vlines {k.mapping_data["coastline"]}
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


# In general, do each step for all maps
# and then map them all together with d.out.file
# That way, you can get combined raster statistics
# for all rasters that will be mapped (useful for
# figuring out the extent of single legend used for
# multiple maps).


def make_maps(fig_width: float,
              fig_height: float,
              background_color: Optional[str] = k.NO_BG_COLOR,
              file_types: Optional[list] = None,
              interpolation_method: Optional[str] = None):
    """ Currently only png and ps (PostScript) formats are supported. """
    try:
        if any(f not in k.SUPPORTED_FILE_TYPES for f in file_types):
            raise NotImplementedError("\nNot implemented error:\n"
                                      "Only PNG and PostScript output"
                                      " is implmenented!\n"
                                      "Please select PNG and/or PostScript"
                                      " output.\n")
    except NotImplementedError as nie:
        print(nie)
    extensions = [k.PNG] if file_types is None else file_types
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
                  background_color: Optional[str] = k.NO_BG_COLOR):
    """ Cycle through interpolated surfaces and generate maps. """
    mapping_mapset = k.mapping_session["mapset"]
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
        outfile = k.PNG_DIR / f"{idw_raster}.{extension}"
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
        outfile = k.PNG_DIR / f"{bspline_raster}.{extension}"
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
    mapping_mapset = k.mapping_session["mapset"]
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
        outfile = k.PS_DIR / f"{idw_raster}.{extension}"
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
        outfile = k.PS_DIR / f"{bspline_raster}.{extension}"
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
    with Session(**k.latlong_session):
        cleanup.print_grass_environment()
        cleanup.clean_up_vectors()
        ascii_to_vector()
        cleanup.list_vector_maps()
    with Session(**k.mapping_session):
        cleanup.list_vector_maps()
        cleanup.clean_up_vectors()
        project_vector_to_current_location(
            source_location=k.latlong_session["location"],
            source_mapset=k.latlong_session["mapset"])
        set_mapping_region(map_of_subregions="andalusia_provinces",
                           column_name='iso_3166_2',
                           selected_subregions=("ES-CA,ES-H,ES-AL,ES-GR,"
                                                "ES-MA,ES-SE,ES-CO,ES-J"))
        set_crop_area("elevation_1KMmd_GMTEDmd_andalusia",
                      900,
                      "olive_HarvestedAreaFraction_andalusia",
                      0.3)
        surf.select_interpolation_points("elevation_1KMmd_GMTEDmd_andalusia",
                                         altitude_cap=2000,
                                         lower_bound=0)
        surf.interpolate_points_idw(vector_layer=1,
                                    number_of_points=3,
                                    power=2.0)
        surf.interpolate_points_bspline(vector_layer=1,
                                        method="bicubic")
        fig_width, fig_height = set_output_image(2)
        make_maps(fig_width,
                  fig_height,
                  file_types=["png", "ps"])
