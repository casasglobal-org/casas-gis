#!/usr/bin/env python3
#
# AUTHOR(S):    Luigi Ponti quartese gmail com
# AUTHOR(S):    Luca Delucchi, luca delucchi fmach it, Fondazione Edmund Mach
# AUTHOR(S):    big-pickle AI model
#
# PURPOSE:      Compute needed stats, generate boxplot whiskers and
#               color rules, compute differences between model runs.
#
# NOTE:         Migrated from casas_gis_old/scripts/get_boxplot_stats.sh,
#               casas_gis_old/PerlScripts/getBoxplotColorRule.pl and
#               casas_gis_old/PerlScripts/SubtractOutput.pl
#
# Copyright:    (c) 2021-2024 CASAS (Center for the Analysis
#                   of Sustainable Agricultural Systems).
#                   https://www.casasglobal.org/).
#
#               SPDX-License-Identifier: GPL-3.0-or-later

"""Compute needed stats, generate plots, etc.
pandas will come in handy.
Marginal analysis?
https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.GeneralizedPoissonResults.get_margeff.html
https://python.quantecon.org/ols.html
probably equivalent to
https://cran.r-project.org/web/packages/margins/vignettes/Introduction.html
"""

import os
from pathlib import Path

import pandas as pd

import constants as k


def raster_statistics(
    map_pattern: str = f"{k.IDW_PREFIX}*",
    output_subdir: str = None,
    extended: bool = False,
):
    """Write univariate statistics for the interpolated raster maps to
    text reports (based on r.univar), as the legacy grass_scripts
    did with "r.univar -e".

    Args:
        map_pattern (str): Pattern of raster maps to process. Defaults
            to f"{k.IDW_PREFIX}*".
        output_subdir (str, optional): Subdirectory of
            constants.REPORT_DIR where reports are written; defaults
            to the report directory itself.
        extended (bool): Whether to compute extended statistics
            (r.univar -ge). Defaults to False.

    Returns:
        list: Names of the raster maps that were processed."""
    import grass.script as grass

    output_dir = k.REPORT_DIR if output_subdir is None else k.REPORT_DIR / output_subdir
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    raster_list = grass.list_strings(type="raster", pattern=map_pattern, mapset=".")
    for raster_map in raster_list:
        outfile = Path(output_dir) / f"{raster_map}_stats.txt"
        flags = "ge" if extended else "e"
        stats_text = grass.read_command(
            "r.univar", flags=flags, map=raster_map, output="-"
        )
        print(f"\nSaving statistics for raster {raster_map} " f"to {outfile}\n")
        with open(outfile, "w") as f:
            f.write(f"# Raster statistics for raster {raster_map} #\n\n")
            f.write(stats_text)
    return raster_list


def compute_boxplot_whiskers(raster_map: str):
    """Compute boxplot whiskers (and absolute min/max) for a raster map,
    based on r.univar extended statistics. Port of the perl one-liners
    used in scripts/get_boxplot_stats.sh:
    lower whisker = max(min(x), Q1 - 1.5 * IQR)
    upper whisker = min(max(x), Q3 + 1.5 * IQR)

    Args:
        raster_map (str): Name of the raster map to analyze.

    Returns:
        tuple: (whisker_low, whisker_high, abs_min, abs_max) float
            values."""
    import grass.script as grass

    univar = grass.parse_command("r.univar", flags="ge", map=raster_map)
    abs_min = float(univar["min"])
    abs_max = float(univar["max"])
    first_quartile = float(univar["first_quartile"])
    third_quartile = float(univar["third_quartile"])
    iqr = third_quartile - first_quartile
    whisker_low = max(abs_min, first_quartile - 1.5 * iqr)
    whisker_high = min(abs_max, third_quartile + 1.5 * iqr)
    print(
        f"\nRaster {raster_map}:\n"
        f"  absolute min: {abs_min}\n"
        f"  absolute max: {abs_max}\n"
        f"  first quartile: {first_quartile}\n"
        f"  third quartile: {third_quartile}\n"
        f"  IQR: {iqr}\n"
        f"  whiskers: {whisker_low} and {whisker_high}\n"
    )
    return whisker_low, whisker_high, abs_min, abs_max


# Viridis-derived color list, as in getBoxplotColorRule.pl
_BOXPLOT_COLORS = (
    "255:255:204-217:240:163-217:240:163-173:221:142"
    "-173:221:142-120:198:121-120:198:121-65:171:93"
    "-65:171:93-35:132:67-35:132:67-0:90:50"
)
_OUTLIER_LOW_COLOR = "255:255:204"
_OUTLIER_HIGH_COLOR = "0:90:50"


def write_boxplot_color_rule(
    raster_map: str,
    whisker_low: float,
    whisker_high: float,
    abs_min: float,
    abs_max: float,
    divergent: bool = False,
    percent: bool = False,
    colors: str = _BOXPLOT_COLORS,
):
    """Write a GRASS GIS color rules file based on boxplot whiskers and
    apply it to the raster map. Port of getBoxplotColorRule.pl.
    When divergent is True the color scale is centered at zero.

    Args:
        raster_map (str): Name of the raster map that will use the
            rule.
        whisker_low (float): Lower boxplot whisker value.
        whisker_high (float): Upper boxplot whisker value.
        abs_min (float): Absolute minimum raster value (outlier low).
        abs_max (float): Absolute maximum raster value (outlier high).
        divergent (bool): Whether the scale is centered at zero.
            Defaults to False.
        percent (bool): Whether to write the rule values as percents.
            Defaults to False.
        colors (str): Colors separated by "-" of the form "R:G:B".
            Defaults to _BOXPLOT_COLORS.

    Returns:
        pathlib.Path: Path of the written color rule file."""
    colors_list = colors.split("-")
    num_of_colors = len(colors_list)
    num_of_bands = num_of_colors - 1
    half_num_of_bands = int(num_of_bands / 2)
    scale_center = 0

    coefficients = _build_coefficients(
        min_val=whisker_low,
        max_val=whisker_high,
        num_of_colors=num_of_colors,
        num_of_bands=num_of_bands,
        half_num_of_bands=half_num_of_bands,
        scale_center=scale_center,
        divergent=divergent,
    )

    rule_lines = [f"# Viridis modified for raster {raster_map}"]
    if not divergent:
        # Outlier low (values between absolute min and low whisker)
        if abs_min != whisker_low:
            rule_lines.append(_format_rule(abs_min, _OUTLIER_LOW_COLOR, percent))
            rule_lines.append(_format_rule(whisker_low, _OUTLIER_LOW_COLOR, percent))
        for coeff, color in zip(coefficients, colors_list):
            rule_lines.append(_format_rule(coeff, color, percent))
        # Outlier high (values between high whisker and absolute max)
        if abs_max != whisker_high:
            rule_lines.append(_format_rule(whisker_high, _OUTLIER_HIGH_COLOR, percent))
            rule_lines.append(_format_rule(abs_max, _OUTLIER_HIGH_COLOR, percent))
    else:
        if abs_min != whisker_low:
            rule_lines.append(_format_rule(abs_min, _OUTLIER_LOW_COLOR, percent))
            rule_lines.append(_format_rule(whisker_low, _OUTLIER_LOW_COLOR, percent))
        for coeff, color in zip(coefficients, colors_list):
            rule_lines.append(_format_rule(coeff, color, percent))
        if abs_max != whisker_high:
            rule_lines.append(_format_rule(whisker_high, _OUTLIER_HIGH_COLOR, percent))
            rule_lines.append(_format_rule(abs_max, _OUTLIER_HIGH_COLOR, percent))
    rule_lines.append("end\n")

    outfile = k.COLOR_DIR / f"{raster_map}_boxplot_color_rule.txt"
    with open(outfile, "w") as f:
        f.write("\n".join(rule_lines))
    print(f"\nColor rule written to {outfile}\n")
    return outfile


def _build_coefficients(
    min_val,
    max_val,
    num_of_colors,
    num_of_bands,
    half_num_of_bands,
    scale_center,
    divergent,
):
    """Build array of value coefficients for each color in the rule.

    Args:
        min_val (float): Minimum value of the color scale.
        max_val (float): Maximum value of the color scale.
        num_of_colors (int): Number of colors in the rule.
        num_of_bands (int): Number of bands (colors minus one).
        half_num_of_bands (int): Half the number of bands.
        scale_center (float): Center of the scale for divergent rules
            (normally zero).
        divergent (bool): Whether the scale is centered at
            scale_center.

    Returns:
        list: Value coefficient for each color in the rule."""
    coefficients = []
    if not divergent:
        base_coeff = 1 / num_of_bands
        coefficients.append(min_val)
        for i in range(1, num_of_bands):
            coefficients.append(min_val + i * base_coeff * (max_val - min_val))
        coefficients.append(max_val)
    elif min_val < 0:
        # Divergent rule with negative values, centered at scale_center.
        base_coeff = 1 / half_num_of_bands
        coefficients.append(min_val)
        for i in range(half_num_of_bands - 1, 0, -1):
            coefficients.append(
                i * base_coeff * (min_val - scale_center) + scale_center
            )
        if num_of_colors % 2 == 1:
            coefficients.append(scale_center)
        else:
            coefficients.extend([scale_center, scale_center])
        for i in range(1, half_num_of_bands):
            coefficients.append(
                i * base_coeff * (max_val - scale_center) + scale_center
            )
        coefficients.append(max_val)
    else:
        base_coeff = 1 / half_num_of_bands
        coefficients.append(min_val)
        for i in range(1, half_num_of_bands):
            coefficients.append(i * base_coeff * (scale_center - min_val))
        if num_of_colors % 2 == 1:
            coefficients.append(scale_center)
        else:
            coefficients.extend([scale_center, scale_center])
        for i in range(1, half_num_of_bands):
            coefficients.append(
                scale_center + i * base_coeff * (max_val - scale_center)
            )
        coefficients.append(max_val)
    return coefficients


def _format_rule(value, color, percent):
    """Format a GRASS color rule line.

    Args:
        value (float): Value at which the color applies.
        color (str): Color of the form "R:G:B".
        percent (bool): Whether to append a percent sign to the value.

    Returns:
        str: A single GRASS color rule line."""
    value_text = f"{value:.3f}"
    if percent:
        return f"{value_text}% {color}"
    return f"{value_text} {color}"


def boxplot_stats_and_color(
    raster_map: str,
    divergent: bool = False,
    percent: bool = False,
    save_stats: bool = True,
):
    """Port of scripts/get_boxplot_stats.sh: compute boxplot whiskers
    for a raster map, write stats report and generate a color rule.

    Args:
        raster_map (str): Name of the raster map to analyze.
        divergent (bool): Whether the color scale is centered at zero.
            Defaults to False.
        percent (bool): Whether to write the color rule in percents.
            Defaults to False.
        save_stats (bool): Whether to write the statistics report
            file. Defaults to True.

    Returns:
        tuple: (whisker_low, whisker_high, abs_min, abs_max) float
            values."""
    import grass.script as grass

    whisker_low, whisker_high, abs_min, abs_max = compute_boxplot_whiskers(raster_map)
    if save_stats:
        outfile = k.REPORT_DIR / f"{raster_map}_stats.txt"
        stats_text = grass.read_command(
            "r.univar", flags="ge", map=raster_map, output="-"
        )
        with open(outfile, "w") as f:
            f.write(f"# Boxplot stats for raster {raster_map} #\n\n")
            f.write(f"{stats_text}\n\n")
            f.write(f"Ends of whiskers are {whisker_low} and " f"{whisker_high}\n")
    write_boxplot_color_rule(
        raster_map,
        whisker_low,
        whisker_high,
        abs_min,
        abs_max,
        divergent=divergent,
        percent=percent,
    )
    apply_boxplot_color_rule(raster_map)
    return whisker_low, whisker_high, abs_min, abs_max


def apply_boxplot_color_rule(raster_map: str):
    """Apply the boxplot color rule file of a raster map to it.

    Args:
        raster_map (str): Name of the raster map to color.

    Returns:
        None."""
    import grass.script as grass

    color_rule = k.COLOR_DIR / f"{raster_map}_boxplot_color_rule.txt"
    grass.run_command("r.colors", map=raster_map, rules=color_rule)


def compute_model_output_delta(
    work_dir: str, warm_file: str, obs_file: str, diff_file: str, ncols_first: int = 11
):
    """Compute the difference between a warming and an observed weather
    scenario in CASAS model outputs, and save a new CASAS-mappable
    file. Port of SubtractOutput.pl. Files are expected to have the
    same number of rows and columns.

    Args:
        work_dir (str): Directory containing the input and output
            files.
        warm_file (str): Name of the warming scenario file.
        obs_file (str): Name of the observed scenario file.
        diff_file (str): Name of the difference output file.
        ncols_first (int): Number of leading columns left unchanged
            (e.g., file, date, longitude, latitude, year). Defaults
            to 11.

    Returns:
        pandas.DataFrame: Dataframe of the computed differences."""
    warm_df = pd.read_csv(os.path.join(work_dir, warm_file), sep="\t")
    obs_df = pd.read_csv(os.path.join(work_dir, obs_file), sep="\t")
    diff_df = compute_delta(warm_df, obs_df, ncols_first=ncols_first)
    diff_path = os.path.join(work_dir, diff_file)
    diff_df.to_csv(diff_path, sep="\t", index=False)
    print(f"\nDifference file written to {diff_path}\n")
    return diff_df


def compute_delta(warm_df: pd.DataFrame, obs_df: pd.DataFrame, ncols_first: int = 11):
    """Subtract numeric columns of the warming dataframe from the
    observed dataframe, keeping the first ncols_first columns
    (e.g., file, date, longitude, latitude, year) unchanged and
    using the observed values for non-numeric columns.

    Args:
        warm_df (pandas.DataFrame): Warming scenario output.
        obs_df (pandas.DataFrame): Observed scenario output.
        ncols_first (int): Number of leading columns kept unchanged.
            Defaults to 11.

    Returns:
        pandas.DataFrame: Dataframe with the computed differences."""
    diff_df = obs_df.copy()
    numeric_columns = diff_df.columns.tolist()[ncols_first:]
    for col in numeric_columns:
        if pd.api.types.is_numeric_dtype(diff_df[col]) and col in warm_df.columns:
            diff_df[col] = warm_df[col].astype(float) - obs_df[col].astype(float)
    return diff_df
