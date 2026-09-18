#!/usr/bin/env python3
#
# AUTHOR(S):    Luigi Ponti quartese gmail com
#
# PURPOSE:      
#
# NOTE:         
#
# Copyright:    (c) 2021-2024 CASAS (Center for the Analysis
#                   of Sustainable Agricultural Systems).
#                   https://www.casasglobal.org/).
#
#               SPDX-License-Identifier: GPL-3.0-or-later

""" Library of functionality reeated to interpolation. """

import pandas as pd

from typing import Optional
from io import StringIO
import constants as k

import grass.script as grass  # noqa E402


def select_interpolation_points(digital_elevation_map,
                                altitude_cap: Optional[float] = None,
                                lower_bound: Optional[float] = None,
                                upper_bound: Optional[float] = None):
    """ Extract vector points greater than cutting point, since some values
        (e.g., bloom day <= 0) may be of little or no meaning. Enable user to
        exclude from interpolation those vector points located at altitude
        greater than an threshold value and/or with point value greater than
        or equal to a threshold.

        Raises ValueError when no imported (imp_*) vector maps exist or
        when the extraction produces no selected (sel_*) vector maps.

        Args:
            digital_elevation_map (str): Raster map used to sample the
                elevation of the interpolation points.
            altitude_cap (float, optional): Exclude stations above this
                altitude (meters).
            lower_bound (float, optional): Exclude points with value
                below this cutting point.
            upper_bound (float, optional): Exclude points with value
                above this cutting point.

        Returns:
            None."""
    vector_list = grass.list_strings(type="vector",
                                     pattern=f"{k.IMPORTED_PREFIX}*",
                                     mapset=".")
    if not vector_list:
        raise ValueError(
            f"No '{k.IMPORTED_PREFIX}*' vector maps found in the current "
            f"mapset. Did the ASCII files of '{k.IMPORTED_PREFIX}*' succeed "
            "in the lat/long location and get projected to the mapping "
            "location?")
    for vector_map in vector_list:
        # list_strings() may include the '@mapset' suffix, which is not
        # valid inside SQL identifiers used by v.extract.
        plain_map_name = vector_map.split("@")[0]
        grass.run_command("v.db.addcolumn",
                          map=vector_map,
                          columns="elevation double precision")
        grass.run_command("v.what.rast",
                          map=vector_map,
                          raster=digital_elevation_map,
                          column="elevation")
        # Combine, in a single query (as in the legacy scripts), the
        # value cutting points and, optionally, the altitude cap. The
        # value column is the name of the imported parameter, i.e., the
        # imported vector name without the 'imp_' prefix.
        base_map_name = plain_map_name.replace(k.IMPORTED_PREFIX, "", 1)
        sql_conditions = []
        if lower_bound is not None:
            sql_conditions.append(f"({base_map_name} >= {lower_bound})")
        if upper_bound is not None:
            sql_conditions.append(f"({base_map_name} <= {upper_bound})")
        if altitude_cap is not None:
            sql_conditions.append(f"(elevation < {altitude_cap})")
        sql_formula = " and ".join(sql_conditions)
        output_map = plain_map_name.replace(k.IMPORTED_PREFIX,
                                            k.SELECTED_PREFIX, 1)
        grass.run_command("v.extract", overwrite=True,
                          input=vector_map,
                          output=output_map,
                          where=sql_formula)
        topo_info = grass.vector_info_topo(output_map)
        no_of_features = sum(
            topo_info.get(key, 0)
            for key in ("points", "lines", "boundaries", "centroids")
        )
        if no_of_features == 0:
            raise ValueError(
                f"No feature was extracted into '{output_map}' by "
                "v.extract. All stations were dropped, because they are "
                "outside the current computational region or excluded by "
                f"the cutting points '{sql_formula}'. Check that the "
                "station coordinates fall inside the region bounds and "
                "that the projection of the mapping location matches the "
                "stations (a misspecified location CRS reprojects the "
                "stations far away, leaving nothing inside the region).")
    selected = grass.list_strings(type="vector",
                                  pattern=f"{k.SELECTED_PREFIX}*",
                                  mapset=".")
    if not selected:
        raise ValueError(
            f"No '{k.SELECTED_PREFIX}*' vector maps were produced by "
            "v.extract. Check that the value cutting points and the "
            f"altitude cap {altitude_cap} do not exclude all stations, "
            "that the digital elevation model "
            f"'{digital_elevation_map}' has values at the stations, "
            "and that the station coordinates are inside the current "
            "computational region (v.extract drops features outside it).")


def interpolate_points_idw(vector_layer: Optional[str] = 1,
                           number_of_points: Optional[int] = 3,
                           power: Optional[float] = 2.0):
    """ Generate interpolated raster surface from vector point data based on
        inverse distance weighting using v.surf.idw GRASS GIS command.

        Raises ValueError when no selected (sel_*) vector map exists.

        Args:
            vector_layer (str, optional): Layer of the input vector to
                use. Defaults to 1.
            number_of_points (int, optional): Number of points to use
                for the interpolation. Defaults to 3.
            power (float, optional): Power of the interpolation weight.
                Defaults to 2.0.

        Returns:
            tuple: (abs_max_idw, abs_min_idw) float values of the
                global maximum and minimum of the interpolated
                rasters."""
    vector_list = grass.list_strings(type="vector",
                                     pattern=f"{k.SELECTED_PREFIX}*",
                                     mapset=".")
    if not vector_list:
        raise ValueError(
            f"No '{k.SELECTED_PREFIX}*' vector maps found in the current "
            "mapset. 'select_interpolation_points()' must be run first to "
            "create the interpolation point vectors.")
    raster_stats = {}
    max_values = []
    min_values = []
    for vector_map in vector_list:
        map_name = vector_map.split("@")[0]
        base_map_name = map_name.replace(k.SELECTED_PREFIX, "", 1)
        output_map = map_name.replace(k.SELECTED_PREFIX,
                                      k.IDW_PREFIX, 1)
        grass.run_command("v.surf.idw", overwrite=True,
                          flags="n",
                          input=vector_map,
                          layer=vector_layer,
                          column=f"{base_map_name}",
                          output=output_map,
                          npoints=number_of_points,
                          power=power)
        # Clip interpolated raster to mapping region using map
        # calculator because r.mask does not work with v.surf.idw
        # see https://trac.osgeo.org/grass/ticket/3363
        calc_expression_mask = (f"{output_map} = "
                                f"if ({k.REGION_RASTER}, "
                                f"{output_map}, null())")
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

        Raises ValueError when no selected (sel_*) vector map exists.

        Args:
            vector_layer (str, optional): Layer of the input vector to
                use. Defaults to "1".
            avg_west_distance (float, optional): Average west-east
                distance between points; if None it is estimated with
                get_distance_points_bspline().
            avg_north_distance (float, optional): Average north-south
                distance between points; if None it is estimated with
                get_distance_points_bspline().
            method (str, optional): "bicubic" or "bilinear".
                Defaults to "bicubic".
            smoothing_parameter (float, optional): Tykhonov
                regularization (lambda) parameter; if None it is
                obtained by cross validation.

        Returns:
            tuple: (abs_max_bspline, abs_min_bspline) float values of
                the global maximum and minimum of the interpolated
                rasters."""
    vector_list = grass.list_strings(type="vector",
                                     pattern=f"{k.SELECTED_PREFIX}*",
                                     mapset=".")
    if not vector_list:
        raise ValueError(
            f"No '{k.SELECTED_PREFIX}*' vector maps found in the current "
            "mapset. 'select_interpolation_points()' must be run first to "
            "create the interpolation point vectors.")
    compute_distance_between_points = (avg_west_distance or
                                       avg_north_distance) is None
    compute_smoothing_parameter = smoothing_parameter is None
    raster_stats = {}
    max_values = []
    min_values = []
    for vector_map in vector_list:
        map_name = vector_map.split("@")[0]
        base_map_name = map_name.replace(k.SELECTED_PREFIX, "", 1)
        output_map = map_name.replace(k.SELECTED_PREFIX,
                                      k.BSPLINE_PREFIX, 1)
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
                          mask=k.REGION_RASTER,
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
        assigned to ew_step and ns_step.

        Args:
            input_vector_map (str): Name of the input vector map.
            output_raster_map (str): Name of the temporary output
                raster map.
            column_name (str): Attribute column used for interpolation.
            vector_layer (str, optional): Layer of the input vector to
                use. Defaults to "1".

        Returns:
            tuple: (avg_west_distance, avg_north_distance) float
                values of the average east-west and north-south
                distances between points."""
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
        method, and assign the resulting value to lambda_i (smoothing).

        Args:
            input_vector_map (str): Name of the input vector map.
            output_raster_map (str): Name of the temporary output
                raster map.
            column_name (str): Attribute column used for interpolation.
            avg_west_distance (float): Average east-west distance
                between points.
            avg_north_distance (float): Average north-south distance
                between points.
            method (str): "bicubic" or "bilinear".
            vector_layer (str, optional): Layer of the input vector to
                use. Defaults to "1".

        Returns:
            float: The selected smoothing (lambda_i) parameter."""
    cross_validation_output = grass.read_command(
        "v.surf.bspline",
        overwrite=True,
        flags="c",
        input=input_vector_map,
        layer=vector_layer,
        column=f"{column_name}",
        raster_output=output_raster_map,
        mask=k.REGION_RASTER,
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
    outfile_path = k.REPORT_DIR
    outfile_name = f"{column_name}_cross_validation.txt"
    outfile = outfile_path / outfile_name
    cross_validation_output = (
        "Cross validation for\new_step (average west distance) = "
        f"{avg_west_distance} and\n"
        "ns_step (average north distance) = "
        f"{avg_north_distance}\n"
        "Selected lambda_i (smoothing parameter) = "
        f"{smoothing_parameter} (minimizes {minimizer_column})\n\n"
        f"{cross_validation_output}")
    with open(outfile, 'w') as f:
        f.write(cross_validation_output)
    return smoothing_parameter
