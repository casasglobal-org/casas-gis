#######
# casas-gis - an open source software based on GRASS GIS, for importing
# ASCII output files from CASAS Global (http://www.casasglobal.org/)
# physiologically based demographic models (PBDMs) to a GRASS monitor after
# interpolation, saving the resulting map to an image file (currently png
# and ps), and further processing and analysis. This a Python rewrite of
# a set of bash shell scripts originally developed by Luigi Ponti starting
# in 2005 at University of California, Berkeley.
#
# Copyright (c) 2005-2022 Luigi Ponti quartese gmail.com and CASAS Global
# (Center for the Analysis of Sustainable Agricultural Systems Global
# http://www.casasglobal.org/).
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# AUTHOR(S):    Luca Delucchi, luca delucchi fmach it, Fondazione Edmund Mach
# AUTHOR(S):    big-pickle AI model
#
#######


"""Geospatial functionality accessed through GRASSS GIS
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
    """Import ASCII files generated in input.py module
    to a vector file in a given GRASS GIS location.

    Args:
        tmp_dir (pathlib.Path, optional): Directory containing the
            tab-separated text files to import. Defaults to
            constants.TMP_DIR.

    Raises:
        ValueError: When no text file is imported.

    Returns:
        None."""
    print("\nImport text files in temporary directory to vector maps:\n")
    pathlist = pathlib.Path(tmp_dir).rglob("*.txt")
    for path in pathlist:
        filename = pathlib.Path(path).name
        mapname = pathlib.Path(path).stem
        grass.run_command(
            "v.in.ascii",
            input=pathlib.Path(tmp_dir).joinpath(filename),
            output=f"{k.IMPORTED_PREFIX}{mapname}",
            skip=1,
            separator="tab",
            x=1,
            y=2,
            z=0,
            columns=f"lon double precision, \
                          lat double precision, \
                          {mapname} double precision",
        )
    print("\nChecking if the imported vectors are there:\n")
    grass.run_command("g.list", flags="p", verbose=True, type="vector", mapset=".")
    if not grass.list_strings(type="vector",
                              pattern=f"{k.IMPORTED_PREFIX}*",
                              mapset="."):
        raise ValueError(
            f"No '{k.IMPORTED_PREFIX}*' vector maps were imported. Check "
            f"that the temporary directory '{tmp_dir}' contains the "
            "tab-separated text files produced by 'select_variable()'.")


def project_vector_to_current_location(
    source_location, source_mapset, tmp_dir=k.TMP_DIR
):
    """Project imported vector from a latitude/longitude unprojected
    GRASS GIS location to a projected location where most GIS
    processing including mapping will occur.

    Args:
        source_location (str): Name of the source (lat/long) GRASS
            location containing the imported vectors.
        source_mapset (str): Name of the source mapset.
        tmp_dir (pathlib.Path, optional): Directory containing the
            temporary text files whose stem matches the vector names.
            Defaults to constants.TMP_DIR.

    Raises:
        ValueError: When no projected vector map is found in the
            mapping location.

    Returns:
        None."""
    print("\nProject imported vectors to mapping location:\n")
    pathlist = pathlib.Path(tmp_dir).rglob("*.txt")
    for path in pathlist:
        mapname = pathlib.Path(path).stem
        grass.run_command(
            "v.proj",
            input=f"{k.IMPORTED_PREFIX}{mapname}",
            location=source_location,
            mapset=source_mapset,
            output=f"{k.IMPORTED_PREFIX}{mapname}",
        )
    print("\nChecking if the imported vectors are there:\n")
    grass.run_command("g.list", flags="p", verbose=True, type="vector", mapset=".")
    if not grass.list_strings(type="vector",
                              pattern=f"{k.IMPORTED_PREFIX}*",
                              mapset="."):
        raise ValueError(
            f"No '{k.IMPORTED_PREFIX}*' vector maps were found in the "
            "mapping location after 'v.proj'. Check that the vectors "
            f"exist in the source location '{source_location}' and "
            f"mapset '{source_mapset}' and that the projection succeeded.")


def set_mapping_region(
    map_of_subregions, column_name, selected_subregions: Optional[str] = None
):
    """Define GRASS GIS region for computations mapping, including
    geographical extent and spatial resolution.
    The 'field type' argument can be 'CHARACTER' or 'INTEGER'.

    Args:
        map_of_subregions (str): Vector map of the administrative
            subregions used to set the region.
        column_name (str): Attribute column of map_of_subregions
            containing the subregion identifiers.
        selected_subregions (str, optional): Comma separated list of
            subregions to map; when None all subregions are used.

    Returns:
        None."""
    if selected_subregions is not None:
        list_of_selected_subregions = selected_subregions.split(",")
        sql_conditions = []
        columns = grass.vector_columns(map_of_subregions, getDict=True)
        column_type = columns[column_name]["type"]
        for subregion in list_of_selected_subregions:
            if column_type == "CHARACTER":
                sql_conditions.append(f"({column_name} = '{subregion}')")
            else:
                sql_conditions.append(f"({column_name} = {subregion})")
        sql_formula = " or ".join(sql_conditions)
        grass.run_command(
            "v.extract",
            overwrite=True,
            input=map_of_subregions,
            output="selected_region",
            where=sql_formula,
        )
        map_of_subregions = "selected_region"
        grass.run_command("g.region", vector=map_of_subregions)
        grass.run_command(
            "g.region",
            n=k.region["subset"]["north"],
            s=k.region["subset"]["south"],
            e=k.region["subset"]["east"],
            w=k.region["subset"]["west"],
        )
        grass.run_command("g.region", res=k.region["full"]["resolution"], flags="a")
    else:
        grass.run_command("g.region", vector=map_of_subregions)
        grass.run_command(
            "g.region",
            n=k.region["full"]["north"],
            s=k.region["full"]["south"],
            e=k.region["full"]["east"],
            w=k.region["full"]["west"],
        )
        grass.run_command("g.region", res=k.region["subset"]["resolution"], flags="a")
    grass.run_command(
        "v.to.rast",
        overwrite=True,
        input=map_of_subregions,
        output=k.REGION_RASTER,
        use="val",
        value=1,
    )
    # Return “g.region -gu” as a dictionary
    grass_region = grass.region()
    print(grass_region)


def set_crop_area(
    digital_elevation_map,
    max_altitude,
    crop_area: Optional[str] = None,
    crop_fraction_cap: Optional[float] = None,
):
    """Use various olive growing areas for masking model output (i.e., map
    model output only inside olive growing areas obtained from various
    sources). Note that when crop_fraction_cap is not None, the function
    will look for a crop_area raster map where each cell value is the
    fraction of area in that cell that is covered by a certain crop.

    Args:
        digital_elevation_map (str): Raster map of the digital
            elevation model used to build the masks.
        max_altitude (float): Maximum altitude (meters) kept in the
            elevation mask.
        crop_area (str, optional): Raster map of the crop growing
            areas; when None the whole mapping region is used.
        crop_fraction_cap (float, optional): Select only cells where
            the fraction of area covered by the crop is above this
            cap; otherwise crop cells with value equal to one are
            selected.

    Returns:
        None."""
    if crop_area is None:
        # Just use the whole mapping region from set_mapping_region()
        calc_expression_crop = f"mask_crop = if (({k.REGION_RASTER},"
    if (crop_area is not None) and (crop_fraction_cap is not None):
        # Select cells where land fraction covered by crop is above cap
        calc_expression_crop = (
            f"mask_crop = if (({k.REGION_RASTER} &&"
            f" {crop_area} > {crop_fraction_cap}),"
        )
    else:
        # Select cells where crop is present (value = 1)
        calc_expression_crop = (
            f"mask_crop = if (({k.REGION_RASTER} &&" f" {crop_area} == 1),"
        )
    # Put altitude values in crop area selected above, otherwise no data.
    calc_expression_crop += f" {digital_elevation_map}, null())"
    grass.mapcalc(calc_expression_crop, overwrite=True)
    calc_expression_altitude = (
        "mask_crop_elevation ="
        f" if (mask_crop < {max_altitude}, mask_crop,"
        " null())"
    )
    grass.mapcalc(calc_expression_altitude, overwrite=True)


def set_output_image(fig_resolution, smart_legend_position: Optional[bool] = False):
    """Set size of output image based on rows and columns of the GRASS
    computational region and a resolution integer value. A resolution of
    one means one pixel will be shown in the output image for each cell
    of the current GRASS region. A resolution of two will double the
    resolution.

    Args:
        fig_resolution (int): Number of output pixels per region cell.
        smart_legend_position (bool, optional): Whether to leave room
            for the legend on the right or on the bottom of the map
            depending on the region shape. Defaults to False.

    Returns:
        tuple: (fig_width, fig_height, number_of_cols,
            number_of_rows) integers."""
    # Output image size in pixels (this is for PNG or other raster output)
    grass_region = grass.region()
    number_of_cols = grass_region["cols"]
    number_of_rows = grass_region["rows"]
    if smart_legend_position and (number_of_cols >= number_of_rows):
        # Make room on the right
        fig_width = number_of_cols + (
            number_of_cols * k.legend_settings["room_for_bottom_legend"]
        )
        fig_width *= fig_resolution
        fig_height = number_of_rows * fig_resolution
    else:
        # Make room on the bottom
        fig_width = number_of_cols * fig_resolution
        fig_height = number_of_rows + (
            number_of_rows * k.legend_settings["room_for_bottom_legend"]
        )
        fig_height *= fig_resolution

    return fig_width, fig_height, number_of_cols, number_of_rows
    # Use frames for more deterministic location of elements such as title
    # on top and legend at bottom?


def write_psmap_instructions(
    interpolated_raster: str,
    selected_points: str,
    fig_width: float,
    fig_height: float,
    outfile_name: str,
    n_of_cols: int,
    n_of_rows: int,
    outfile_path: Optional[os.PathLike] = None,
    margin: Optional[float] = 0.1,
):
    """Generates text file including mapping instructions to serve as input
    to ps.map GRASS GIS command.

    Args:
        interpolated_raster (str): Name of the interpolated raster map.
        selected_points (str): Name of the selected points vector map.
        fig_width (float): Width of the output image in pixels.
        fig_height (float): Height of the output image in pixels.
        outfile_name (str): Base name of the ps.map instruction file.
        n_of_cols (int): Number of columns of the computational region.
        n_of_rows (int): Number of rows of the computational region.
        outfile_path (os.PathLike, optional): Directory where the
            instruction file is written; defaults to constants.PS_DIR.
        margin (float, optional): Map margin. Defaults to 0.1.

    Returns:
        pathlib.Path: Path of the written ps.map instruction file."""
    outfile_path = k.PS_DIR or outfile_path
    outfile_name = f"{outfile_name}.psmap"
    outfile = outfile_path / outfile_name
    for prefix in k.INTERPOLATION_PREFIXES:
        print(interpolated_raster)
        if interpolated_raster.startswith(prefix):
            drape_map_name = interpolated_raster.replace(prefix, k.DRAPE_PREFIX, 1)
    grass.run_command(
        "r.shade",
        overwrite=True,
        flags="c",
        shade={k.mapping_data["shaded_relief"]},
        color=interpolated_raster,
        output=drape_map_name,
        brighten=0,
    )
    # Need to find a way to place legend and text nicely
    # Another idea could be have different pieces of pasmap_file
    # that are combined according to specific context/options.
    # https://grass.osgeo.org/grass80/manuals/ps.map.html
    paper_width, paper_height, bottom_legend = map_legend(
        extension=k.PS,
        fig_width=fig_width,
        fig_height=fig_height,
        n_of_cols=n_of_cols,
        n_of_rows=n_of_rows,
    )
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

    with open(outfile, "w") as f:
        f.write(psmap_file)
        return outfile


# In general, do each step for all maps
# and then map them all together with d.out.file
# That way, you can get combined raster statistics
# for all rasters that will be mapped (useful for
# figuring out the extent of single legend used for
# multiple maps).


def make_maps(
    fig_width: float,
    fig_height: float,
    number_of_cols: int,
    number_of_rows: int,
    background_color: Optional[str] = k.NO_BG_COLOR,
    file_types: Optional[list] = None,
    interpolation_method: Optional[str] = None,
    color_rule: Optional[str] = "panoply.txt",
):
    """Currently only png and ps (PostScript) formats are supported.

    Args:
        fig_width (float): Width of the output image in pixels.
        fig_height (float): Height of the output image in pixels.
        number_of_cols (int): Number of columns of the computational
            region.
        number_of_rows (int): Number of rows of the computational
            region.
        background_color (str, optional): Background color of the
            output images. Defaults to constants.NO_BG_COLOR.
        file_types (list, optional): Output formats, e.g., ["png",
            "ps"]. Defaults to None (all supported types).
        interpolation_method (str, optional): Name of the
            interpolation method; currently unused.
        color_rule (str, optional): Name of the color rule file used
            for the maps. Defaults to "panoply.txt".

    Returns:
        None."""
    try:
        if any(f not in k.SUPPORTED_FILE_TYPES for f in file_types):
            raise NotImplementedError(
                "\nNot implemented error:\n"
                "Only PNG and PostScript output"
                " is implemented!\n"
                "Please select PNG and/or PostScript"
                " output.\n"
            )
    except NotImplementedError as nie:
        print(nie)
    extensions = [k.PNG] if file_types is None else file_types
    for extension in extensions:
        if extension == "png":
            make_png_maps(
                extension=extension,
                fig_width=fig_width,
                fig_height=fig_height,
                number_of_cols=number_of_cols,
                number_of_rows=number_of_rows,
                background_color=background_color,
                color_rule=color_rule,
            )
        elif extension == "ps":
            make_ps_maps(
                extension=extension,
                fig_width=fig_width,
                fig_height=fig_height,
                number_of_cols=number_of_cols,
                number_of_rows=number_of_rows,
            )
        # map_legend() here ???
        # See func def below


def make_png_maps(
    extension: str,
    fig_width: float,
    fig_height: float,
    number_of_cols: int,
    number_of_rows: int,
    background_color: Optional[str] = k.NO_BG_COLOR,
    color_rule: Optional[str] = "panoply.txt",
):
    """Cycle through interpolated surfaces and generate PNG maps.

    Args:
        extension (str): Output file extension, i.e. "png".
        fig_width (float): Width of the output image in pixels.
        fig_height (float): Height of the output image in pixels.
        number_of_cols (int): Number of columns of the computational
            region.
        number_of_rows (int): Number of rows of the computational
            region.
        background_color (str, optional): Background color of the
            output images. Defaults to constants.NO_BG_COLOR.
        color_rule (str, optional): Name of the color rule file used
            for the maps. Defaults to "panoply.txt".

    Returns:
        None."""
    mapping_mapset = k.mapping_session["mapset"]
    sel_vector_list = get_map_list_from_pattern(
        map_type="vector", pattern="sel_*", mapping_mapset=mapping_mapset
    )
    idw_rasters_list = get_map_list_from_pattern(
        map_type="raster", pattern="idw_*", mapping_mapset=mapping_mapset
    )
    bspline_rasters_list = get_map_list_from_pattern(
        map_type="raster", pattern="bspline_*", mapping_mapset=mapping_mapset
    )
    for surf_raster_list in (idw_rasters_list, bspline_rasters_list):
        loop_and_map_png(
            extension=extension,
            surf_raster_list=surf_raster_list,
            sel_vector_list=sel_vector_list,
            fig_width=fig_width,
            fig_height=fig_height,
            number_of_cols=number_of_cols,
            number_of_rows=number_of_rows,
            background_color=background_color,
            color_rule=color_rule,
        )


def make_ps_maps(
    extension: str,
    fig_width: float,
    fig_height: float,
    number_of_cols: int,
    number_of_rows: int,
):
    """Cycle through interpolated surfaces and generate PostScript maps.

    Args:
        extension (str): Output file extension, i.e. "ps".
        fig_width (float): Width of the output image in pixels.
        fig_height (float): Height of the output image in pixels.
        number_of_cols (int): Number of columns of the computational
            region.
        number_of_rows (int): Number of rows of the computational
            region.

    Returns:
        None."""
    mapping_mapset = k.mapping_session["mapset"]
    sel_vector_list = get_map_list_from_pattern(
        map_type="vector", pattern="sel_*", mapping_mapset=mapping_mapset
    )
    idw_rasters_list = get_map_list_from_pattern(
        map_type="raster", pattern="idw_*", mapping_mapset=mapping_mapset
    )
    bspline_rasters_list = get_map_list_from_pattern(
        map_type="raster", pattern="bspline_*", mapping_mapset=mapping_mapset
    )
    for surf_raster_list in (idw_rasters_list, bspline_rasters_list):
        loop_and_map_ps(
            extension=extension,
            surf_raster_list=surf_raster_list,
            sel_vector_list=sel_vector_list,
            fig_width=fig_width,
            fig_height=fig_height,
            number_of_cols=number_of_cols,
            number_of_rows=number_of_rows,
        )


def loop_and_map_png(
    extension: str,
    surf_raster_list: list,
    sel_vector_list: list,
    fig_width: float,
    fig_height: float,
    number_of_cols: int,
    number_of_rows: int,
    background_color: Optional[str] = k.NO_BG_COLOR,
    color_rule: Optional[str] = "panoply.txt",
):
    """Loop over interpolated raster maps and render one PNG map each.

    Args:
        extension (str): Output file extension, i.e. "png".
        surf_raster_list (list): Names of the interpolated raster
            maps to render.
        sel_vector_list (list): Names of the selected points vector
            maps (same length as surf_raster_list).
        fig_width (float): Width of the output image in pixels.
        fig_height (float): Height of the output image in pixels.
        number_of_cols (int): Number of columns of the computational
            region.
        number_of_rows (int): Number of rows of the computational
            region.
        background_color (str, optional): Background color of the
            output images. Defaults to constants.NO_BG_COLOR.
        color_rule (str, optional): Name of the color rule file used
            for the maps. Defaults to "panoply.txt".

    Returns:
        None."""
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
        clr.set_color_rule(raster_map=idw_raster, color_rule=color_rule)

        grass.run_command(
            "d.mon",
            overwrite=True,
            start=extension,
            width=fig_width,
            height=fig_height,
            bgcolor=background_color,
            output=outfile,
        )
        shaded_relief = k.mapping_data.get("shaded_relief")
        if shaded_relief is not None:
            grass.run_command("d.his", i=shaded_relief, h=idw_raster)
        coastline = k.mapping_data.get("coastline")
        if coastline is not None:
            grass.run_command(
                "d.vect",
                map=coastline["map_name"],
                color=coastline["color"],
                width=coastline["width"],
            )
        admin_divisions = k.mapping_data.get("admin_divisions")
        if admin_divisions is not None:
            grass.run_command(
                "d.vect",
                map=admin_divisions["map_name"],
                type="boundary",
                color="black",
                width=3,
            )
        grass.run_command(
            "d.vect",
            map=sel_vector,
            type="point",
            color="white",
            fill_color="black",
            icon="basic/point",
            size=15,
            width=2,
        )
        draw_map_box()
        map_legend(
            extension=extension,
            map_name=idw_raster,
            fig_width=fig_width,
            fig_height=fig_height,
            n_of_cols=number_of_cols,
            n_of_rows=number_of_rows,
        )
        grass.run_command("d.mon", stop=extension)


def loop_and_map_ps(
    extension: str,
    surf_raster_list: list,
    sel_vector_list: list,
    fig_width: float,
    fig_height: float,
    number_of_cols: int,
    number_of_rows: int,
):
    """Loop over interpolated raster maps and render one PostScript map
    each using ps.map.

    Args:
        extension (str): Output file extension, i.e. "ps".
        surf_raster_list (list): Names of the interpolated raster
            maps to render.
        sel_vector_list (list): Names of the selected points vector
            maps (same length as surf_raster_list).
        fig_width (float): Width of the output image in pixels.
        fig_height (float): Height of the output image in pixels.
        number_of_cols (int): Number of columns of the computational
            region.
        number_of_rows (int): Number of rows of the computational
            region.

    Returns:
        None."""
    for idw_raster, sel_vector in zip(surf_raster_list, sel_vector_list):
        outfile = k.PS_DIR / f"{idw_raster}.{extension}"
        ps_instructions_file = write_psmap_instructions(
            interpolated_raster=idw_raster,
            selected_points=sel_vector,
            outfile_name=idw_raster,
            fig_width=fig_width,
            fig_height=fig_height,
            n_of_cols=number_of_cols,
            n_of_rows=number_of_rows,
        )
        grass.run_command(
            "ps.map",
            overwrite=True,
            flags="e",
            input=ps_instructions_file,
            output=outfile,
        )


def get_map_list_from_pattern(map_type: str, pattern: str, mapping_mapset: str):
    """Return map names of the given mapset matching a pattern.

    Args:
        map_type (str): Type of maps, e.g., "raster" or "vector".
        pattern (str): Map name pattern, e.g., "idw_*".
        mapping_mapset (str): Name of the mapset whose maps are
            listed.

    Returns:
        list: Names of the matching maps."""
    map_dict = grass.list_grouped(type=map_type, pattern=pattern)
    return map_dict[f"{mapping_mapset}"]


def export_geotiff(
    raster_map: str,
    output_dir: Optional[pathlib.Path] = None,
    overwrite: Optional[bool] = True,
):
    """Export an interpolated raster map to GeoTIFF using r.out.gdal,
    as the legacy grass_scripts did with the -t flag.

    Args:
        raster_map (str): Name of the raster map to export.
        output_dir (pathlib.Path, optional): Directory where the file
            is written; defaults to constants.OUT_DIR.
        overwrite (bool, optional): Whether to delete an existing
            output file. Defaults to True.

    Returns:
        pathlib.Path: Path of the exported GeoTIFF file."""
    output_dir = output_dir or k.OUT_DIR
    outfile = pathlib.Path(output_dir) / f"{raster_map}.tif"
    if overwrite and outfile.exists():
        outfile.unlink()
    grass.run_command(
        "r.out.gdal",
        overwrite=True,
        input=raster_map,
        output=outfile,
        format="GTiff",
        type="Float32",
        createopt="COMPRESS=DEFLATE",
    )
    print(f"\nGeoTIFF exported to {outfile}\n")
    return outfile


def export_all_geotiffs(
    output_dir: Optional[pathlib.Path] = None, pattern: Optional[str] = None
):
    """Export all interpolated rasters (idw_* and bspline_*) to GeoTIFF
    files.

    Args:
        output_dir (pathlib.Path, optional): Directory where the files
            are written; defaults to constants.OUT_DIR.
        pattern (str, optional): Map name pattern used to filter the
            rasters. Defaults to None (all maps in the mapping mapset).

    Returns:
        list: Paths of the exported GeoTIFF files."""
    mapping_mapset = k.mapping_session["mapset"]
    pattern = pattern or "*"
    rasters = get_map_list_from_pattern(
        map_type="raster", pattern=pattern, mapping_mapset=mapping_mapset
    )
    exported = []
    for raster_map in rasters:
        if raster_map.startswith(k.IDW_PREFIX) or raster_map.startswith(
            k.BSPLINE_PREFIX
        ):
            exported.append(export_geotiff(raster_map, output_dir))
    return exported


def map_legend(
    extension: str,
    fig_width: float,
    fig_height: float,
    n_of_cols: int,
    n_of_rows: int,
    map_name: Optional[str] = None,
    smart_legend_position: Optional[bool] = False,
):
    """Draw the legend on a PNG map or compute paper size and legend
    position for a PostScript map.

    Args:
        extension (str): Output format, either "png" or "ps".
        fig_width (float): Width of the output image in pixels.
        fig_height (float): Height of the output image in pixels.
        n_of_cols (int): Number of columns of the computational region.
        n_of_rows (int): Number of rows of the computational region.
        map_name (str, optional): Raster map drawn in the legend
            (only used for "png"). Defaults to None.
        smart_legend_position (bool, optional): Whether to choose the
            legend position from the map shape. Defaults to False.

    Returns:
        tuple or None: For "ps" returns (paper_width, paper_height,
            bottom_legend); for "png" returns None."""
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
        grass.run_command(
            "d.legend",
            flags="st",
            raster=map_name,
            color="black",
            labelnum=5,
            at=legend_coords,
            font="Arial",
        )
    elif extension == "ps":
        # Compute paper size and legend position
        bottom_legend = True
        if smart_legend_position and (n_of_cols >= n_of_rows):
            # make room for legend on the right
            paper_width = (k.BASE_PAPER_SIDE * (fig_width / fig_height)) + (
                k.BASE_PAPER_SIDE * k.legend_settings["room_for_bottom_legend"]
            )
            paper_height = k.BASE_PAPER_SIDE
            bottom_legend = False
        else:
            # make room for legend below map
            paper_width = k.BASE_PAPER_SIDE
            paper_height = (k.BASE_PAPER_SIDE * (fig_height / fig_width)) + (
                k.BASE_PAPER_SIDE * k.legend_settings["room_for_bottom_legend"]
            )
        return paper_width, paper_height, bottom_legend


def draw_map_box(width: Optional[int] = 2, bordercolor: Optional[str] = "black"):
    """Draw a border and graticule inside the map frame.

    Args:
        width (int, optional): Width of the border line. Defaults to 2.
        bordercolor (str, optional): Color of the border line.
            Defaults to "black".

    Returns:
        None."""
    grass.run_command(
        "d.grid",
        flags="wn",
        size="5:0:0",
        color="black",
        width=width,
        bordercolor=bordercolor,
    )


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
            source_mapset=k.latlong_session["mapset"],
        )
        set_mapping_region(
            map_of_subregions=k.mapping_data["admin_divisions"]["map_name"],
            column_name=k.mapping_data["admin_divisions"]["column"],
            selected_subregions=",".join(
                k.mapping_data["admin_divisions"]["division_names"][:10]
            ),
        )
        set_crop_area(
            k.mapping_data["digital_elevation"],
            900,
            k.mapping_data["crop"]["harvest_area_fraction"],
            0.3,
        )
        surf.select_interpolation_points(
            k.mapping_data["digital_elevation"], altitude_cap=2000, lower_bound=0
        )
        abs_max_idw, abs_min_idw = surf.interpolate_points_idw(
            vector_layer=1, number_of_points=3, power=2.0
        )
        # surf.interpolate_points_bspline(vector_layer=1,
        #                                 method="bicubic")
        fig_width, fig_height, number_of_cols, number_of_rows = set_output_image(1)
        make_maps(
            fig_width=fig_width,
            fig_height=fig_height,
            number_of_cols=number_of_cols,
            number_of_rows=number_of_rows,
            background_color="white",
            file_types=["png", "ps"],
        )
