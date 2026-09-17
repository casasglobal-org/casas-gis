#!/usr/bin/env python3
#
# AUTHOR(S):    Luigi Ponti quartese gmail com
# AUTHOR(S):    Luca Delucchi, luca delucchi fmach it, Fondazione Edmund Mach
# AUTHOR(S):    big-pickle AI model
#
# PURPOSE:      Color related stuff.
#               Select color scheme, adjust to data, etc.
#
# NOTE:         Migrated from casas_gis_old/PerlScripts/multiColorRule.pl
#               and casas_gis_old/PerlScripts/rangeColorRule.pl
#
# Copyright:    (c) 2021-2024 CASAS (Center for the Analysis
#                   of Sustainable Agricultural Systems).
#                   https://www.casasglobal.org/).
#
#               SPDX-License-Identifier: GPL-3.0-or-later

"""Color related stuff.
Select color scheme, adjust to data, etc."""

# https://matplotlib.org/stable/tutorials/colors/colormaps.html
# https://colorcet.holoviz.org/
# https://jiffyclub.github.io/palettable/
# https://seaborn.pydata.org/

import constants as k


def set_color_rule(raster_map: str, color_rule: str):
    """Apply a color rule file (in constants.COLOR_DIR) to a raster
    map using r.colors.

    Args:
        raster_map (str): Name of the raster map to color.
        color_rule (str): Name of the color rule file stored in
            constants.COLOR_DIR.

    Returns:
        None."""
    import grass.script as grass

    grass.run_command(
        "r.colors",
        # flags="ge",
        map=raster_map,
        rules=k.COLOR_DIR / color_rule,
    )


def write_color_rule(
    color_rule: str,
    low_cut: float = None,
    hi_cut: float = None,
    divergent: bool = False,
    min_value: float = None,
    max_value: float = None,
    outfile_name: str = "customColorRule",
):
    """Write a GRASS GIS color rule file from a color string (colors
    separated by "-", of the form "R:G:B") and value range, as done
    by multiColorRule.pl. When divergent is True the color scale is
    centered at zero.

    Args:
        color_rule (str): Colors separated by "-" of the form "R:G:B".
        low_cut (float, optional): Lower cut for the value range; if
            given and above min_value it becomes the scale minimum.
        hi_cut (float, optional): Upper cut for the value range; if
            given and below max_value it becomes the scale maximum.
        divergent (bool): Whether to center the scale at zero.
            Defaults to False.
        min_value (float, optional): Minimum value of the data range.
            Required to build a balanced rule.
        max_value (float, optional): Maximum value of the data range.
            Required to build a balanced rule.
        outfile_name (str): Name of the rule file written to
            constants.COLOR_DIR. Defaults to "customColorRule".

    Returns:
        pathlib.Path: Path of the written color rule file."""
    colors = color_rule.split("-")
    num_of_colors = len(colors)
    num_of_bands = num_of_colors - 1
    half_num_of_bands = (num_of_colors - 1) / 2

    if min_value is None or max_value is None:
        raise ValueError(
            "min_value and max_value are required to build " "a balanced color rule."
        )
    if low_cut is not None and low_cut > min_value:
        min_value = low_cut
    if hi_cut is not None and hi_cut < max_value:
        max_value = hi_cut

    coefficients = _build_coefficients(
        min_value, max_value, num_of_colors, num_of_bands, half_num_of_bands, divergent
    )

    rule_lines = []
    for coeff, color in zip(coefficients, colors):
        rule_lines.append(f"{coeff} {color}")
    rule_lines.append("end")

    outfile = k.COLOR_DIR / outfile_name
    with open(outfile, "w") as f:
        f.write("\n".join(rule_lines))
    print(f"\nColor rule written to {outfile}\n")
    return outfile


def apply_color_rule(
    raster_map: str,
    color_rule: str,
    low_cut: float = None,
    hi_cut: float = None,
    divergent: bool = False,
    min_value: float = None,
    max_value: float = None,
):
    """Compute the min/max of the raster (if not given) and apply a
    color rule whose range spans the data.

    Args:
        raster_map (str): Name of the raster map to color.
        color_rule (str): Color rule string of colors separated by "-".
        low_cut (float, optional): Lower cut for the value range.
        hi_cut (float, optional): Upper cut for the value range.
        divergent (bool): Whether to center the scale at zero.
            Defaults to False.
        min_value (float, optional): Minimum data value; if None it is
            computed from the raster statistics.
        max_value (float, optional): Maximum data value; if None it is
            computed from the raster statistics.

    Returns:
        None."""
    import grass.script as grass

    if min_value is None or max_value is None:
        univar = grass.parse_command("r.univar", flags="ge", map=raster_map)
        min_value = float(univar["min"])
        max_value = float(univar["max"])
    rule_file = write_color_rule(
        color_rule=color_rule,
        low_cut=low_cut,
        hi_cut=hi_cut,
        divergent=divergent,
        min_value=min_value,
        max_value=max_value,
    )
    grass.run_command("r.colors", map=raster_map, rules=rule_file)


def _build_coefficients(
    min_value, max_value, num_of_colors, num_of_bands, half_num_of_bands, divergent
):
    """Build array of value coefficients for each color in the rule.

    Args:
        min_value (float): Minimum value of the color scale.
        max_value (float): Maximum value of the color scale.
        num_of_colors (int): Number of colors in the rule.
        num_of_bands (int): Number of bands (colors minus one).
        half_num_of_bands (float): Half the number of bands, used for
            divergent scales.
        divergent (bool): Whether the scale is centered at zero.

    Returns:
        list: Value coefficient for each color in the rule."""
    coefficients = []
    if not divergent:
        base_coeff = 1 / num_of_bands
        coefficients.append(min_value)
        for i in range(1, num_of_bands):
            coefficients.append(min_value + i * base_coeff * (max_value - min_value))
        coefficients.append(max_value)
    else:
        base_coeff = 1 / half_num_of_bands
        coefficients.append(min_value)
        for i in range(int(half_num_of_bands) - 1, 0, -1):
            coefficients.append(i * base_coeff * min_value)
        if num_of_colors % 2 == 1:
            coefficients.append(0)
        else:
            coefficients.extend([0, 0])
        for i in range(1, int(half_num_of_bands)):
            coefficients.append(i * base_coeff * max_value)
        coefficients.append(max_value)
    return coefficients


def create_color_rule_from_raster(
    raster_map: str, color_rule: str, output_name: str = None, divergent: bool = True
):
    """Create a color rule file from a raster map and return the path.
    This is the high-level helper used to build balanced color rules
    before mapping.

    Args:
        raster_map (str): Name of the raster map used to compute the
            min/max of the data.
        color_rule (str): Color rule string of colors separated by "-".
        output_name (str, optional): Name of the rule file written to
            constants.COLOR_DIR. Defaults to
            "{raster_map}_color_rule.txt".
        divergent (bool): Whether to center the scale at zero.
            Defaults to True.

    Returns:
        pathlib.Path: Path of the written color rule file."""
    import grass.script as grass

    univar = grass.parse_command("r.univar", flags="ge", map=raster_map)
    min_value = float(univar["min"])
    max_value = float(univar["max"])
    output_name = output_name or f"{raster_map}_color_rule.txt"
    return write_color_rule(
        color_rule=color_rule,
        divergent=divergent,
        min_value=min_value,
        max_value=max_value,
        outfile_name=output_name,
    )


def apply_color_rule_average_color_scale(
    raster_map: str,
    color_rule: str,
    value_range_low: float = None,
    value_range_up: float = None,
    divergent: bool = True,
):
    """Apply a divergent (zero centered) color rule to a raster map.
    Kept for compatibility with legacy "color_rule_divergent" calls.

    Args:
        raster_map (str): Name of the raster map to color.
        color_rule (str): Color rule string of colors separated by "-".
        value_range_low (float, optional): Minimum value of the scale.
        value_range_up (float, optional): Maximum value of the scale.
        divergent (bool): Whether to center the scale at zero.
            Defaults to True.

    Returns:
        None."""
    apply_color_rule(
        raster_map=raster_map,
        color_rule=color_rule,
        divergent=divergent,
        min_value=value_range_low,
        max_value=value_range_up,
    )


if __name__ == "__main__":
    # Example: write a NASA Panoply divergent color rule.
    panoply = (
        "4:14:216-32:80:255-65:150:255-109:193:255"
        "-134:217:255-156:238:255-175:245:255-206:255:255"
        "-255:254:71-255:235:0-255:196:0-255:144:0"
        "-255:72:0-255:0:0-213:0:0-158:0:0"
    )
    write_color_rule(
        panoply,
        min_value=-100,
        max_value=100,
        divergent=True,
        outfile_name="panoply_divergent.txt",
    )
