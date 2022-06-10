""" Geospatial functionality accessed through GRASSS GIS
    https://grasswiki.osgeo.org/wiki/Category:Python
    https://grass.osgeo.org/grass79/manuals/libpython/index.html
    Ideas for cloud implementation:
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
import color as clr

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
        processing including mapping will occur. """
    print('\nProject imported vectors to mapping location:\n')
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
        The 'field type' argument can be 'CHARACTER' or 'INTEGER' """
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
                          n=k.region["subset"]["north"],
                          s=k.region["subset"]["south"],
                          e=k.region["subset"]["east"],
                          w=k.region["subset"]["west"])
        grass.run_command("g.region",
                          res=k.region["full"]["resolution"],
                          flags="a")
    else:
        grass.run_command("g.region",
                          vector=map_of_subregions)
        grass.run_command("g.region",
                          n=k.region["full"]["north"],
                          s=k.region["full"]["south"],
                          e=k.region["full"]["east"],
                          w=k.region["full"]["west"])
        grass.run_command("g.region",
                          res=k.region["subset"]["resolution"],
                          flags="a")
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


def set_output_image(fig_resolution,
                     smart_legend_position: Optional[bool] = False):
    """ Set size of output image based on rows and columns of the GRASS
        computational region and a resolution integer value. A resolution of
        one means one pixel will be shown in the output image for each cell
        of the current GRASS region. A resolution of two will double the
        resolution. """
    # Output image size in pixels (this is for PNG or other raster output)
    grass_region = grass.region()
    number_of_cols = grass_region['cols']
    number_of_rows = grass_region['rows']
    if smart_legend_position and (number_of_cols >= number_of_rows):
        # Make room on the right
        fig_width = (number_of_cols + (number_of_cols *
                     k.legend_settings["room_for_bottom_legend"]))
        fig_width *= fig_resolution
        fig_height = number_of_rows * fig_resolution
    else:
        # Make room on the botton
        fig_width = number_of_cols * fig_resolution
        fig_height = (number_of_rows + (number_of_rows *
                      k.legend_settings["room_for_bottom_legend"]))
        fig_height *= fig_resolution

    return fig_width, fig_height, number_of_cols, number_of_rows
    # Use frames for more deterministic location of elements such as title
    # on top and legend at bottom?


def write_psmap_instructions(interpolated_raster: str,
                             selected_points: str,
                             fig_width: float,
                             fig_height: float,
                             outfile_name: str,
                             outfile_path: Optional[os.PathLike] = None,
                             margin: Optional[float] = 0.1):
    """ Generates text file including mapping instructions to serve as input
        to ps.map GRASS GIS command. Returns output file name with path. """
    outfile_path = k.PS_DIR or outfile_path
    outfile_name = f"{outfile_name}.psmap"
    outfile = outfile_path / outfile_name
    for prefix in k.INTERPOLATION_PREFIXES:
        print(interpolated_raster)
        if interpolated_raster.startswith(prefix):
            drape_map_name = interpolated_raster.replace(prefix,
                                                         k.DRAPE_PREFIX, 1)
    grass.run_command("r.shade", overwrite=True,
                      flags="c",
                      shade={k.mapping_data["shaded_relief"]},
                      color=interpolated_raster,
                      output=drape_map_name,
                      brighten=0)
    # Need to find a way to place legend and text nicely
    # Another idea could be have different pieces of pasmap_file
    # that are combined according to specific context/options.
    # https://grass.osgeo.org/grass80/manuals/ps.map.html
    (paper_width, paper_height,
     bottom_legend) = map_legend(extension=k.PS,
                                 fig_width=fig_width,
                                 fig_height=fig_height,
                                 n_of_cols=number_of_cols,
                                 n_of_rows=number_of_rows)
    left_margin = right_margin = bottom_margin = top_margin = margin
    if bottom_legend:
        # legend goes below map
        legend_x = paper_width * 0.10
        legend_y = paper_height * 0.75
        legend_width = paper_width * 0.8
        legend_height = paper_height * 0.04
        top_margin = (paper_height - paper_width) * 0.5
    else:
        # legend goes to the right
        legend_x = paper_width * 0.75
        legend_y = paper_height * 0.10
        legend_width = paper_width * 0.04
        legend_height = paper_height * 0.8
        left_margin = (paper_width - paper_height) * 0.5
    # https://unicode-table.com/en/
    sample_text = "this is sample text"
    psmap_file = f"""
        # GRASS GIS ps.map instruction file

        paper
            width {paper_width}
            height {paper_height}
            left {left_margin}
            right {right_margin}
            bottom {bottom_margin}
            top {top_margin}
        end

        border y
            color black
            width 1
        end

        # Main raster
        raster {drape_map_name}

        # Legend
        colortable y
            raster {interpolated_raster}
            where {legend_x} {legend_y}
            # range 1 211
            # height 0.2
            # cols 10
            width {legend_width}
            height {legend_height}
            font Helvetica
            # fontsize 12
        end

        text 50% -40% {sample_text}
            color black
            # width 1
            # background white
            # fontsize 12
            # ref lower left
        end

        # Input points
        vpoints {selected_points}
            type point
            color white
            fcolor black
            width 0.5
            symbol basic/circle
            size 2
        end

        # Some boundary lines
        vlines {k.mapping_data["target_region"]["map_name"]}
            type boundary
            color black
            width 3
            lpos 0
        end

        # Some boundary lines
        vlines {k.mapping_data["admin_divisions"]["map_name"]}
            type boundary
            color black
            width 1
            lpos 0
        end

        # Some boundary lines
        vlines {k.mapping_data["countries"]["map_name"]}
            type boundary
            color grey
            width 2
            lpos 0
        end

        # Some boundary lines
        vlines {k.mapping_data["coastline"]["map_name"]}
            type boundary
            color grey
            width 3
            lpos 0
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
              number_of_cols: int,
              number_of_rows: int,
              background_color: Optional[str] = k.NO_BG_COLOR,
              file_types: Optional[list] = None,
              interpolation_method: Optional[str] = None):
    """ Currently only png and ps (PostScript) formats are supported. """
    try:
        if any(f not in k.SUPPORTED_FILE_TYPES for f in file_types):
            raise NotImplementedError("\nNot implemented error:\n"
                                      "Only PNG and PostScript output"
                                      " is implemented!\n"
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
                          number_of_cols=number_of_cols,
                          number_of_rows=number_of_rows,
                          background_color=background_color)
        elif extension == "ps":
            make_ps_maps(extension=extension,
                         fig_width=fig_width,
                         fig_height=fig_height)
        # map_legend() here ???
        # See func def below


def make_png_maps(extension: str,
                  fig_width: float,
                  fig_height: float,
                  number_of_cols: int,
                  number_of_rows: int,
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
    for surf_raster_list in (idw_rasters_list, bspline_rasters_list):
        loop_and_map_png(extension=extension,
                         surf_raster_list=surf_raster_list,
                         sel_vector_list=sel_vector_list,
                         fig_width=fig_width,
                         fig_height=fig_height,
                         number_of_cols=number_of_cols,
                         number_of_rows=number_of_rows,
                         background_color=background_color)


def make_ps_maps(extension: str,
                 fig_width: float,
                 fig_height: float):
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
    for surf_raster_list in (idw_rasters_list, bspline_rasters_list):
        loop_and_map_ps(extension=extension,
                        surf_raster_list=surf_raster_list,
                        sel_vector_list=sel_vector_list,
                        fig_width=fig_width,
                        fig_height=fig_height)


def loop_and_map_png(extension: str,
                     surf_raster_list: list,
                     sel_vector_list: list,
                     fig_width: float,
                     fig_height: float,
                     number_of_cols: int,
                     number_of_rows: int,
                     background_color: Optional[str] = k.NO_BG_COLOR):
    # Debugging code follows as a reminder that when no PNG monitor is
    # running, the monitor variable is as string of length == zero.
    monitor = grass.read_command("d.mon", flags="p", quiet=True).strip()
    print("This is current monitor: ", monitor)
    print("This is length of monitor var: ", len(monitor))
    # Sometimes the PNG monitor remains open (e.g., app runs with error)
    # and needs to be closed before the for loop below starts.
    if len(monitor) > 0:
        grass.run_command("d.mon", stop=extension)
    # There should probably be a way to adjust vector line size depending on
    # fig_width,fig_height or maybe number_of_cols,number_of_rows (rescale)
    for idw_raster, sel_vector in zip(surf_raster_list, sel_vector_list):
        outfile = k.PNG_DIR / f"{idw_raster}.{extension}"
        clr.set_color_rule(raster_map=idw_raster,
                           color_rule="panoply.txt")

        grass.run_command("d.mon", overwrite=True,
                          start=extension,
                          width=fig_width,
                          height=fig_height,
                          bgcolor=background_color,
                          output=outfile)
        grass.run_command("d.his",
                          i=k.mapping_data["shaded_relief"],
                          h=idw_raster)
        grass.run_command("d.vect",
                          map=k.mapping_data["coastline"]["map_name"],
                          color=k.mapping_data["coastline"]["color"],
                          width=k.mapping_data["coastline"]["width"])
        grass.run_command("d.vect",
                          map=k.mapping_data["admin_divisions"]["map_name"],
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
        draw_map_box()
        map_legend(extension=extension,
                   map_name=idw_raster,
                   fig_width=fig_width,
                   fig_height=fig_height,
                   n_of_cols=number_of_cols,
                   n_of_rows=number_of_rows)
        grass.run_command("d.mon", stop=extension)


def loop_and_map_ps(extension: str,
                    surf_raster_list: list,
                    sel_vector_list: list,
                    fig_width: float,
                    fig_height: float):
    for idw_raster, sel_vector in zip(surf_raster_list, sel_vector_list):
        outfile = k.PS_DIR / f"{idw_raster}.{extension}"
        ps_instructions_file = write_psmap_instructions(
            interpolated_raster=idw_raster,
            selected_points=sel_vector,
            outfile_name=idw_raster,
            fig_width=fig_width,
            fig_height=fig_height)
        grass.run_command("ps.map", overwrite=True,
                          flags="e",
                          input=ps_instructions_file,
                          output=outfile)


def get_map_list_from_pattern(map_type: str,
                              pattern: str,
                              mapping_mapset: str):
    map_dict = grass.list_grouped(type=map_type, pattern=pattern)
    return map_dict[f"{mapping_mapset}"]


def map_legend(extension: str,
               fig_width: float,
               fig_height: float,
               n_of_cols: int,
               n_of_rows: int,
               map_name: Optional[str] = None,
               smart_legend_position: Optional[bool] = False):
    # sourcery skip: assign-if-exp, switch
    # Check fig_width, fig_height and
    # if n_of_cols >= n_of_rows then legend goes to bottom
    # if n_of_cols < n_of_rows the legend goes to right
    # See set_output_image()
    # bottom,top,left,right as % of screen coordinates (0,0 is lower left)
    if extension == "png":
        if smart_legend_position and (n_of_cols < n_of_rows):
            legend_coords = (20, 80, 86, 90)
        else:
            legend_coords = (6, 10, 20, 80)
        grass.run_command("d.legend",
                          flags="st",
                          raster=map_name,
                          color="black",
                          labelnum=5,
                          at=legend_coords,
                          font="Arial")
    elif extension == "ps":
        # Compute paper size and legend position
        bottom_legend = True
        if smart_legend_position and (n_of_cols >= n_of_rows):
            # make room for legend on the right
            paper_width = ((k.BASE_PAPER_SIDE * (fig_width / fig_height)) +
                           (k.BASE_PAPER_SIDE *
                            k.legend_settings["room_for_bottom_legend"]))
            paper_height = k.BASE_PAPER_SIDE
            bottom_legend = False
        else:
            # make room for legend below map
            paper_width = k.BASE_PAPER_SIDE
            paper_height = ((k.BASE_PAPER_SIDE * (fig_height / fig_width)) +
                            (k.BASE_PAPER_SIDE *
                             k.legend_settings["room_for_bottom_legend"]))
        return paper_width, paper_height, bottom_legend


def draw_map_box(width: Optional[int] = 2,
                 bordercolor: Optional[str] = "black"):
    grass.run_command("d.grid",
                      flags="wn",
                      size="5:0:0",
                      color="black",
                      width=width,
                      bordercolor=bordercolor)


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
        cleanup.clean_up_rasters()
        project_vector_to_current_location(
            source_location=k.latlong_session["location"],
            source_mapset=k.latlong_session["mapset"])
        set_mapping_region(
            map_of_subregions=k.mapping_data["admin_divisions"]["map_name"],
            column_name=k.mapping_data["admin_divisions"]["column"],
            selected_subregions=",".join(k.mapping_data["admin_divisions"]
                                                       ["division_names"]
                                                       [:10])
            )
        set_crop_area(k.mapping_data["digital_elevation"],
                      900,
                      k.mapping_data["crop"]["harvest_area_fraction"],
                      0.3)
        surf.select_interpolation_points(k.mapping_data["digital_elevation"],
                                         altitude_cap=2000,
                                         lower_bound=0)
        (abs_max_idw, abs_min_idw) = surf.interpolate_points_idw(
            vector_layer=1,
            number_of_points=3,
            power=2.0)
        # surf.interpolate_points_bspline(vector_layer=1,
        #                                 method="bicubic")
        (fig_width, fig_height,
         number_of_cols, number_of_rows) = set_output_image(1)
        make_maps(
                  fig_width=fig_width,
                  fig_height=fig_height,
                  number_of_cols=number_of_cols,
                  number_of_rows=number_of_rows,
                  background_color="white",
                  file_types=["png", "ps"])
