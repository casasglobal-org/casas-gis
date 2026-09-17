#!/usr/bin/env python3
#
# AUTHOR(S):    Luigi Ponti quartese gmail com
# AUTHOR(S):    Luca Delucchi, luca delucchi fmach it, Fondazione Edmund Mach
# AUTHOR(S):    big-pickle AI model
#
# PURPOSE:      Batch processing workflows allowing to run the
#               CASAS mapping pipeline for multiple parameters
#               (output variables) in one go.
#
# NOTE:         Migrated from the legacy bash scripts in
#               casas_gis_old/scripts/batch_*.sh
#
# Copyright:    (c) 2021-2024 CASAS (Center for the Analysis
#                   of Sustainable Agricultural Systems).
#                   https://www.casasglobal.org/).
#
#               SPDX-License-Identifier: GPL-3.0-or-later

"""Run the mapping pipeline for a series of parameters, one at a time,
as done by the legacy batch_*.sh bash scripts. Each parameter is a
(numeric) column of the CASAS PBDM ASCII output (e.g., day degrees,
bloom day, rainfall, olive fly pupae, and so on)."""

from dataclasses import dataclass
from typing import Optional

import constants as k
import cleanup
import color as clr
import gis
import interpolation as surf
import input as inp
import report
import stats

from grass_session import Session  # noqa E402
import grass.script as grass  # noqa E402


@dataclass
class BatchParameter:
    """Parameters needed to map a single CASAS PBDM output variable,
    mirroring the command-line options of the legacy grass_scripts
    (e.g., MedPresentClimate, usa, india, ...).

    Args:
        column (int): 1-based column index of the variable in the
            PBDM output.
        variable (str): Variable name, matches a PBDM output column
            header.
        output_dir (str): Sub-directory used for saving results.
        legend (str): Legend text.
        lower_cut (float, optional): Lower cutting point. Defaults to
            0.
        upper_cut (float, optional): Upper cutting point. Defaults to
            0.
        altitude (int, optional): Altitude (m) cap for interpolation
            points. Defaults to 2000.
        region (str, optional): Comma separated codes, "-1" for all.
            Defaults to "-1".
        states (str, optional): Comma separated state codes (usa,
            india). Defaults to None.
        interpolation (str, optional): k.IDW or k.BSPLINE.
            Defaults to k.IDW.
        numpoints (int, optional): Number of points for v.surf.idw.
            Defaults to 3.
        clip (bool, optional): -c: clip to crop area. Defaults to
            False.
        plot (bool, optional): -p: generate histogram/barchart plots.
            Defaults to False.
        mask (bool, optional): -m: mask to crop area. Defaults to
            False.
        yearly (bool, optional): -w: write yearly maps. Defaults to
            False.
        graph (bool, optional): -g: statistics and graphs. Defaults
            to False.
        raster_stats (bool, optional): -r: raster statistics.
            Defaults to False.
        custom (bool, optional): -u: custom color rule. Defaults to
            False.
        diff (bool, optional): -d: difference maps. Defaults to False.
        compound_legend (bool, optional): -x: overall compound legend.
            Defaults to False.
        crop (str, optional): Crop map key, "none" maps over whole
            region. Defaults to None.
        crop_threshold (float, optional): Crop fraction cap. Defaults
            to 0.01.
        color_rule (str, optional): Color rule file name
            (color_rules/). Defaults to None.
        color_rule_divergent (str, optional): Divergent color string.
            Defaults to None.
        low_bar_col (float, optional): Lower bar-chart color.
            Defaults to None.
        up_bar_col (float, optional): Upper bar-chart color.
            Defaults to None.
        spline_step_east (float, optional): B-spline ew_step.
            Defaults to None.
        spline_step_north (float, optional): B-spline ns_step.
            Defaults to None.
        tykhonov_reg (float, optional): B-spline lambda_i.
            Defaults to None.
        idw_power (float, optional): v.surf.idw power. Defaults to
            2.0."""

    column: int  # 1-based column index of the variable in the PBDM output
    variable: str  # variable name, matches a PBDM output column header
    output_dir: str  # sub-directory used for saving results
    legend: str  # legend text
    lower_cut: float = 0
    upper_cut: float = 0
    altitude: int = 2000  # altitude (m) cap for interpolation points
    region: Optional[str] = "-1"  # comma separated codes, "-1" for all
    states: Optional[str] = None  # comma separated state codes (usa, india)
    interpolation: str = k.IDW  # k.IDW or k.BSPLINE
    numpoints: int = 3  # number of points for v.surf.idw
    clip: bool = False  # -c: clip to crop area
    plot: bool = False  # -p: generate histogram/barchart plots
    mask: bool = False  # -m: mask to crop area
    yearly: bool = False  # -w: write yearly maps
    graph: bool = False  # -g: statistics and graphs
    raster_stats: bool = False  # -r: raster statistics
    custom: bool = False  # -u: custom color rule
    diff: bool = False  # -d: difference maps
    compound_legend: bool = False  # -x: overall compound legend
    crop: Optional[str] = None  # crop map key, "none" maps over whole region
    crop_threshold: float = 0.01  # crop fraction cap
    color_rule: Optional[str] = None  # color rule file name (color_rules/)
    color_rule_divergent: Optional[str] = None  # divergent color string
    low_bar_col: Optional[float] = None  # lower bar-chart color
    up_bar_col: Optional[float] = None  # upper bar-chart color
    spline_step_east: Optional[float] = None  # b-spline ew_step
    spline_step_north: Optional[float] = None  # b-spline ns_step
    tykhonov_reg: Optional[float] = None  # b-spline lambda_i
    idw_power: float = 2.0  # v.surf.idw power


# Aliases mapping legacy crop names to region configuration keys.
_CROP_ALIASES = {
    "coffee": "harvest_area_fraction",
    "olive": "harvest_area_fraction",
    "cassava": "harvest_area_fraction",
    "cassava_harvarea": "harvest_area_fraction",
    "grape": "harvest_area_fraction",
    "tomato_harvested": "harvest_area_fraction",
    "tomato_h_temperate": "tomato_temperate",
    "tomato_h_tropical": "tomato_tropical",
    "tomato_h_combined": "tomato_combined",
    "alfalfa_harvested": "alfalfa_harvested",
    "cotton_full": "cotton_full",
    "cotton_irrig": "cotton_irrig",
    "cotton_rainfed": "cotton_rainfed",
    "sigpac_buffered_3km": "area_sigpac_buffered_3km",
    "sigpac_buffered_5km": "area_sigpac_buffered_5km",
    "sigpac_3km": "area_sigpac_3km",
}


def resolve_crop_map(crop: Optional[str]):
    """Return the raster crop area map name for a legacy crop option
    (e.g., 'coffee', 'cotton_irrig', 'sigpac_buffered_3km'), or None
    if no matching map is configured for the current region.

    Args:
        crop (str, optional): Legacy crop option name.

    Returns:
        str or None: Raster crop area map name, or None when no
            matching map is configured."""
    if not crop or crop == "none" or not k.mapping_data.get("crop"):
        return None
    crop_data = k.mapping_data["crop"]
    if crop in crop_data:
        return crop_data[crop]
    key = _CROP_ALIASES.get(crop)
    if key is not None and key in crop_data:
        return crop_data[key]
    return None


# ---------------------------------------------------------------------------
# Olive parameters, Mediterranean Basin (MedPresentClimate) and Andalusia
# ---------------------------------------------------------------------------

# Columns of olive plant and olive fly PBDM output used across the legacy
# olive batch scripts.
OLIVE_PLANT_PARAMETERS = [
    BatchParameter(
        12,
        "dd",
        "DayDegrees",
        "day degrees above 8.3 C",
        lower_cut=0,
        altitude=700,
        region="21,22,23,25,31,32,33,35",
    ),
    BatchParameter(
        13,
        "ddbZero",
        "ddBelowZero",
        "day degrees below 0 C",
        lower_cut=30,
        altitude=10000,
        interpolation=k.IDW,
        region="-1",
    ),
    BatchParameter(
        14,
        "FruWgt",
        "FruitWeight",
        "Fruit weight",
        lower_cut=1,
        interpolation=k.IDW,
        altitude=900,
        mask=True,
    ),
    BatchParameter(
        16,
        "Bloomday",
        "BloomDate",
        "Bloom date",
        lower_cut=1,
        interpolation=k.IDW,
        altitude=900,
        mask=True,
    ),
    BatchParameter(
        17,
        "BloomYr",
        "BloomYears",
        "Years with bloom",
        lower_cut=0,
        interpolation=k.IDW,
        altitude=900,
        mask=True,
    ),
    BatchParameter(
        18,
        "DDBSum",
        "DDBSum",
        "day degrees below 9.1 C",
        lower_cut=0,
        altitude=900,
        region="21,22,23,25,31,32,33,35",
    ),
    BatchParameter(
        20,
        "PrcpYrSum",
        "PrcpYearSum",
        "mm rainfall per year",
        lower_cut=0,
        interpolation=k.IDW,
        altitude=10000,
        mask=True,
    ),
    BatchParameter(
        22,
        "ddbMinus10",
        "ddbMinus10",
        "Day degrees below -10 C",
        lower_cut=1,
        interpolation=k.IDW,
        altitude=10000,
        region="21,22,23,25,31,32,33,35",
    ),
    BatchParameter(
        23,
        "ddbMinus83",
        "ddbMinus83",
        "Day degrees below -8.3 C",
        lower_cut=1,
        interpolation=k.IDW,
        altitude=10000,
        region="-1",
    ),
]

# With-fly (olive fruit fly) parameters.
OLIVE_FLY_PARAMETERS = [
    BatchParameter(
        24,
        "OFEgDays",
        "OFeggDays",
        "olive fly egg days",
        lower_cut=1,
        altitude=700,
        region="21,22,23,25,31,32,33,35",
    ),
    BatchParameter(
        25,
        "OFLrDays",
        "OFlarvaeDays",
        "olive fly larvae days",
        lower_cut=0,
        altitude=700,
        region="21,22,23,25,31,32,33,35",
    ),
    BatchParameter(
        26,
        "OFPuDays",
        "OFpupaeDays",
        "olive fly pupae days",
        lower_cut=0,
        interpolation=k.IDW,
        altitude=700,
        mask=True,
    ),
    BatchParameter(
        27,
        "OFAdDays",
        "OFadultDays",
        "olive fly adult days",
        lower_cut=1,
        altitude=700,
        region="21,22,23,25,31,32,33,35",
    ),
    BatchParameter(
        28,
        "OfPupSum",
        "OFpupaeCumSum",
        "olive fly pupae (cumulative)",
        interpolation=k.IDW,
        altitude=900,
        mask=True,
    ),
    BatchParameter(
        30,
        "PrcntAtkd",
        "PercentFruitAttacked",
        "percent fruit attacked",
        lower_cut=1,
        interpolation=k.IDW,
        altitude=900,
        mask=True,
    ),
]


def run_olive_mediterranean_batch(
    longitude: int = 5, latitude: int = 6, year: int = 11, params=None
):
    """Batch run of the Mediterranean Basin olive workflow, previously
    done by scripts/batch_OliveProtheus.sh.

    Args:
        longitude (int, optional): 1-based column index of longitude
            in the PBDM output. Defaults to 5.
        latitude (int, optional): 1-based column index of latitude in
            the PBDM output. Defaults to 6.
        year (int, optional): 1-based column index of the year in the
            PBDM output. Defaults to 11.
        params (list, optional): BatchParameter objects to run; when
            None the default olive fly parameters are used.

    Returns:
        None."""

    def_params = [
        OLIVE_FLY_PARAMETERS[4],  # OfPupSum (active in legacy)
        BatchParameter(
            30,
            "PrcntAtkd",
            "PercentFruitAttacked",
            "percent fruit attacked",
            lower_cut=1,
            interpolation=k.IDW,
            altitude=900,
            mask=True,
        ),
    ]
    params = params or def_params
    for p in params:
        run_mapping_workflow(p, longitude=longitude, latitude=latitude, year=year)


def run_olive_andalusia_batch(
    longitude: int = 5,
    latitude: int = 6,
    year: int = 11,
    with_fly: bool = False,
    raster_stats: bool = True,
    params=None,
):
    """Batch run of the Andalusia olive workflow for climate change
    scenarios (HadGEM2-ES/RCA4 2071-2100 RCP8.5), previously done by
    scripts/batch_olive_andalusia.sh.

    Args:
        longitude (int, optional): 1-based column index of longitude
            in the PBDM output. Defaults to 5.
        latitude (int, optional): 1-based column index of latitude in
            the PBDM output. Defaults to 6.
        year (int, optional): 1-based column index of the year in the
            PBDM output. Defaults to 11.
        with_fly (bool, optional): Whether to also map olive fruit fly
            parameters. Defaults to False.
        raster_stats (bool, optional): Whether to compute raster
            statistics (currently not passed through). Defaults to
            True.
        params (list, optional): BatchParameter objects to run; when
            None olive plant (and optional fly) parameters are used.

    Returns:
        None."""
    # NOTE: the legacy script used save_directory names that include the
    # climate scenario and province/crop settings (e.g.
    # "olive_HadGEM2_ES_RCA4_2071-2100_rcp8.5_dd").
    if params is None:
        plant = [
            BatchParameter(
                p.column,
                p.variable,
                p.output_dir,
                p.legend,
                lower_cut=0,
                altitude=1000,
                interpolation=k.IDW,
                numpoints=3,
                raster_stats=True,
                plot=True,
                crop="sigpac_buffered_3km",
                crop_threshold=0.20,
            )
            for p in OLIVE_PLANT_PARAMETERS
            if p.variable
            in (
                "dd",
                "ddbZero",
                "FruWgt",
                "Bloomday",
                "BloomYr",
                "DDBSum",
                "ChillHD",
                "PrcpYrSum",
                "ddbMinus83",
            )
        ]
        if with_fly:
            fly = [
                BatchParameter(
                    28,
                    "OfPupSum",
                    "OFpupaeCumSum",
                    "olive fly pupae (cumulative)",
                    lower_cut=0,
                    altitude=1000,
                    interpolation=k.IDW,
                    numpoints=3,
                    raster_stats=True,
                    plot=True,
                    crop="sigpac_buffered_3km",
                    crop_threshold=0.20,
                ),
                BatchParameter(
                    30,
                    "PrcntAtkd",
                    "PercentFruitAttacked",
                    "percent fruit attacked",
                    lower_cut=0,
                    altitude=1000,
                    interpolation=k.IDW,
                    numpoints=3,
                    raster_stats=True,
                    plot=True,
                    crop="sigpac_buffered_3km",
                    crop_threshold=0.20,
                ),
            ]
        else:
            fly = []
        params = plant + fly
    for p in params:
        run_mapping_workflow(p, longitude=longitude, latitude=latitude, year=year)


def run_coffee_colombia_batch(
    longitude: int = 4,
    latitude: int = 5,
    year: int = 12,
    crop: str = "none",
    params=None,
):
    """Batch run of the Colombia coffee workflow, previously done by
    scripts/batch_coffee_colombia.sh. Uses b-spline interpolation and
    the NASA Panoply divergent color rule.

    Args:
        longitude (int, optional): 1-based column index of longitude
            in the PBDM output. Defaults to 4.
        latitude (int, optional): 1-based column index of latitude in
            the PBDM output. Defaults to 5.
        year (int, optional): 1-based column index of the year in the
            PBDM output. Defaults to 12.
        crop (str, optional): Legacy crop option name. Defaults to
            "none".
        params (list, optional): BatchParameter objects to run; when
            None the default coffee parameters are used.

    Returns:
        None."""
    panoply = (
        "4:14:216-32:80:255-65:150:255-109:193:255"
        "-134:217:255-156:238:255-175:245:255-206:255:255"
        "-255:254:71-255:235:0-255:196:0-255:144:0"
        "-255:72:0-255:0:0-213:0:0-158:0:0"
    )
    if params is None:
        params = [
            BatchParameter(
                6,
                "meandamnum",
                "meandamnum",
                "meandamnum",
                lower_cut=0,
                altitude=10000,
                interpolation=k.BSPLINE,
                numpoints=3,
                raster_stats=True,
                plot=True,
                crop=crop,
                crop_threshold=0.01,
                color_rule_divergent=panoply,
            ),
            BatchParameter(
                7,
                "meanripemass",
                "meanripemass",
                "meanripemass",
                lower_cut=0,
                altitude=10000,
                interpolation=k.BSPLINE,
                numpoints=3,
                raster_stats=True,
                plot=True,
                crop=crop,
                crop_threshold=0.01,
                color_rule_divergent=panoply,
            ),
            BatchParameter(
                8,
                "meanTdda",
                "meanTdda",
                "meanTdda",
                lower_cut=0,
                altitude=10000,
                interpolation=k.BSPLINE,
                numpoints=3,
                raster_stats=True,
                plot=True,
                crop=crop,
                crop_threshold=0.01,
                color_rule_divergent=panoply,
            ),
            BatchParameter(
                9,
                "meanRain",
                "meanRain",
                "meanRain",
                lower_cut=0,
                altitude=10000,
                interpolation=k.BSPLINE,
                numpoints=3,
                raster_stats=True,
                plot=True,
                crop=crop,
                crop_threshold=0.01,
                color_rule_divergent=panoply,
            ),
            BatchParameter(
                10,
                "meanLangl",
                "meanLangl",
                "meanLangl",
                lower_cut=0,
                altitude=10000,
                interpolation=k.BSPLINE,
                numpoints=3,
                raster_stats=True,
                plot=True,
                crop=crop,
                crop_threshold=0.01,
                color_rule_divergent=panoply,
            ),
        ]
    for p in params:
        run_mapping_workflow(p, longitude=longitude, latitude=latitude, year=year)


def run_india_cotton_batch(
    longitude: int = 5,
    latitude: int = 6,
    year: int = 11,
    states: str = None,
    crop: str = "cotton_irrig",
    params=None,
):
    """Batch run of the India cotton workflow, previously done by
    scripts/batch_india_cotton.sh. Uses b-spline interpolation with
    the Tykhonov regularization parameter set to 0.05 and a
    spline step of 57000.

    Args:
        longitude (int, optional): 1-based column index of longitude
            in the PBDM output. Defaults to 5.
        latitude (int, optional): 1-based column index of latitude in
            the PBDM output. Defaults to 6.
        year (int, optional): 1-based column index of the year in the
            PBDM output. Defaults to 11.
        states (str, optional): Comma separated state codes.
            Defaults to None.
        crop (str, optional): Legacy crop option name. Defaults to
            "cotton_irrig".
        params (list, optional): BatchParameter objects to run; when
            None the default cotton parameters are used.

    Returns:
        None."""
    if params is None:
        params = [
            BatchParameter(
                17,
                "kg_ha",
                "cotton_yield",
                "kg per ha (cotton area)",
                lower_cut=0,
                altitude=2000,
                states=states,
                interpolation=k.BSPLINE,
                crop=crop,
                clip=True,
                raster_stats=True,
                spline_step_east=57000,
                spline_step_north=57000,
                tykhonov_reg=0.05,
            )
        ]
    for p in params:
        run_mapping_workflow(p, longitude=longitude, latitude=latitude, year=year)


def run_libya_tunisia_screwworm_batch(
    longitude: int = 5,
    latitude: int = 6,
    year: int = 11,
    yearly: bool = False,
    params=None,
):
    """Batch run of the Libya-Tunisia screwworm workflow, previously done
    by scripts/batch_LibyaTunisia_sw_majorRev.sh.

    Args:
        longitude (int, optional): 1-based column index of longitude
            in the PBDM output. Defaults to 5.
        latitude (int, optional): 1-based column index of latitude in
            the PBDM output. Defaults to 6.
        year (int, optional): 1-based column index of the year in the
            PBDM output. Defaults to 11.
        yearly (bool, optional): Whether to write yearly maps.
            Defaults to False.
        params (list, optional): BatchParameter objects to run; when
            None the default screwworm parameters are used.

    Returns:
        None."""
    if params is None:
        params = [
            BatchParameter(
                25,
                "LarvaePerYr",
                "LarvaePerYr",
                "LarvaePerYr",
                lower_cut=0,
                altitude=900,
                interpolation=k.IDW,
                numpoints=7,
                yearly=yearly,
                graph=True,
                low_bar_col=6.183,
                up_bar_col=339.366,
            ),
            BatchParameter(
                26,
                "PuapePerYr",
                "PuapePerYr",
                "PuapePerYr",
                lower_cut=0,
                altitude=900,
                interpolation=k.IDW,
                numpoints=7,
                yearly=yearly,
                graph=True,
                low_bar_col=4.551,
                up_bar_col=249.767,
            ),
            BatchParameter(
                27,
                "AdultsPerYr",
                "AdultsPerYr",
                "AdultsPerYr",
                lower_cut=0,
                altitude=900,
                interpolation=k.IDW,
                numpoints=7,
                yearly=yearly,
                graph=True,
                low_bar_col=2.721,
                up_bar_col=227.218,
            ),
            BatchParameter(
                28,
                "RIxPupae",
                "RIxPupae",
                "RIxPupae",
                lower_cut=0,
                altitude=900,
                interpolation=k.IDW,
                numpoints=7,
                yearly=yearly,
                graph=True,
                low_bar_col=0.02,
                up_bar_col=158.419,
            ),
        ]
    for p in params:
        run_mapping_workflow(p, longitude=longitude, latitude=latitude, year=year)


def run_usa_screwworm_batch(
    longitude: int = 5,
    latitude: int = 6,
    year: int = 11,
    states: str = "TX",
    params=None,
):
    """Batch run of the US screwworm workflow, previously done by
    scripts/batch_USA_screwworm.sh.

    Args:
        longitude (int, optional): 1-based column index of longitude
            in the PBDM output. Defaults to 5.
        latitude (int, optional): 1-based column index of latitude in
            the PBDM output. Defaults to 6.
        year (int, optional): 1-based column index of the year in the
            PBDM output. Defaults to 11.
        states (str, optional): Comma separated state codes.
            Defaults to "TX".
        params (list, optional): BatchParameter objects to run; when
            None the default screwworm parameters are used.

    Returns:
        None."""
    if params is None:
        params = [
            BatchParameter(
                12,
                "rain",
                "rain",
                "rain",
                lower_cut=0,
                upper_cut=2000,
                altitude=2000,
                states=states,
                yearly=True,
                low_bar_col=0.00,
                up_bar_col=2549.70,
            ),
        ]
    for p in params:
        run_mapping_workflow(p, longitude=longitude, latitude=latitude, year=year)


def run_usa_olive_batch(
    longitude: int = 5,
    latitude: int = 6,
    year: int = 11,
    states: str = "HI",
    params=None,
):
    """Batch run of the US/Mexico olive workflow, previously done by
    scripts/batch_USA_olive.sh.

    Args:
        longitude (int, optional): 1-based column index of longitude
            in the PBDM output. Defaults to 5.
        latitude (int, optional): 1-based column index of latitude in
            the PBDM output. Defaults to 6.
        year (int, optional): 1-based column index of the year in the
            PBDM output. Defaults to 11.
        states (str, optional): Comma separated state codes.
            Defaults to "HI".
        params (list, optional): BatchParameter objects to run; when
            None the default olive parameters are used.

    Returns:
        None."""
    if params is None:
        params = [
            BatchParameter(
                20,
                "PrcpYrSum",
                "Prcp_US_Hawaii",
                "mm rainfall per year",
                lower_cut=0,
                altitude=1500,
                states=states,
            ),
        ]
    for p in params:
        run_mapping_workflow(p, longitude=longitude, latitude=latitude, year=year)


def run_swd_europe_batch(
    longitude: int = 5, latitude: int = 6, year: int = 11, params=None
):
    """Batch run of the spotted wing drosophila (SWD) workflow for the
    European/Mediterranean grape region, previously done by
    scripts/batch_swd_EU.sh.

    Args:
        longitude (int, optional): 1-based column index of longitude
            in the PBDM output. Defaults to 5.
        latitude (int, optional): 1-based column index of latitude in
            the PBDM output. Defaults to 6.
        year (int, optional): 1-based column index of the year in the
            PBDM output. Defaults to 11.
        params (list, optional): BatchParameter objects to run; when
            None the default SWD parameters are used.

    Returns:
        None."""
    if params is None:
        params = [
            BatchParameter(
                27,
                "Pupae_Yr",
                "pupae_per_year",
                "pupae per year",
                lower_cut=0,
                altitude=2000,
                interpolation=k.BSPLINE,
                raster_stats=True,
                plot=True,
                low_bar_col=0,
                up_bar_col=1295.219,
            ),
        ]
    for p in params:
        run_mapping_workflow(p, longitude=longitude, latitude=latitude, year=year)


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------


def run_mapping_workflow(
    parameter: BatchParameter,
    longitude: int = 5,
    latitude: int = 6,
    year: int = 11,
    input_dir: str = inp.INPUT_DIR,
    fig_resolution: int = 1,
):
    """Run the whole CASAS mapping pipeline for a single parameter:
    select the variable from the PBDM output, import it to GRASS,
    project, define region and crop area, select interpolation
    points, interpolate and finally render maps and reports.

    Args:
        parameter (BatchParameter): Parameters of the variable to map.
        longitude (int, optional): 1-based column index of longitude
            in the PBDM output. Defaults to 5.
        latitude (int, optional): 1-based column index of latitude in
            the PBDM output. Defaults to 6.
        year (int, optional): 1-based column index of the year in the
            PBDM output. Defaults to 11.
        input_dir (str, optional): Directory with the PBDM output
            files. Defaults to input.INPUT_DIR.
        fig_resolution (int, optional): Number of output pixels per
            region cell. Defaults to 1.

    Returns:
        None."""
    print("\n============================================================\n")
    print(
        f"Mapping parameter '{parameter.variable}' "
        f"(column {parameter.column}): {parameter.legend}"
    )
    print("\n============================================================\n")

    if parameter.states is not None:
        selection = parameter.states
    elif parameter.region in (None, "-1", "all"):
        selection = None
    else:
        selection = ",".join(parameter.region.split())

    # 1. Prepare temporary text file for this variable only.
    cleanup.clean_up_tmp()
    df_dict = inp.csv_to_df_dict(input_dir)
    inp.select_variable(
        df_dict, longitude, latitude, parameter.column, tmp_dir=k.TMP_DIR
    )

    # 2. Import ASCII files to vector maps in the lat/long location.
    with Session(**k.latlong_session):
        cleanup.clean_up_vectors()
        gis.ascii_to_vector()

    # 3. Project, map, and analyze in the projected mapping location.
    with Session(**k.mapping_session):
        cleanup.clean_up_vectors()
        cleanup.clean_up_rasters()
        gis.project_vector_to_current_location(
            source_location=k.latlong_session["location"],
            source_mapset=k.latlong_session["mapset"],
        )

        # (Re)set computational region.
        if k.mapping_data.get("admin_divisions") and k.mapping_data[
            "admin_divisions"
        ].get("map_name"):
            admin_map = k.mapping_data["admin_divisions"]["map_name"]
            admin_column = k.mapping_data["admin_divisions"]["column"]
        else:
            admin_map = admin_column = None
        if selection is not None and admin_map is not None:
            gis.set_mapping_region(
                admin_map, admin_column, selected_subregions=selection
            )
        else:
            gis.set_mapping_region(admin_map, admin_column, selected_subregions=None)

        # Crop area mask (e.g., olive, coffee or cotton growing areas).
        crop_map = resolve_crop_map(parameter.crop)
        if parameter.crop and parameter.crop != "none" and crop_map is not None:
            gis.set_crop_area(
                k.mapping_data["digital_elevation"],
                parameter.altitude,
                crop_area=crop_map,
                crop_fraction_cap=parameter.crop_threshold,
            )

        # Select points to use for interpolation (altitude and value caps).
        surf.select_interpolation_points(
            k.mapping_data["digital_elevation"],
            altitude_cap=parameter.altitude,
            lower_bound=parameter.lower_cut,
        )

        # Interpolate using the selected method.
        if parameter.interpolation == k.BSPLINE:
            abs_max, abs_min = surf.interpolate_points_bspline(
                vector_layer=1,
                method="bicubic",
                smoothing_parameter=parameter.tykhonov_reg,
                avg_west_distance=parameter.spline_step_east,
                avg_north_distance=parameter.spline_step_north,
            )
        else:
            abs_max, abs_min = surf.interpolate_points_idw(
                vector_layer=1,
                number_of_points=parameter.numpoints,
                power=parameter.idw_power,
            )

        # Output image size.
        fig_width, fig_height, number_of_cols, number_of_rows = gis.set_output_image(
            fig_resolution, smart_legend_position=True
        )

        # Build a custom color rule file if one was requested. The rule
        # range spans the absolute min/max of the interpolated rasters.
        color_rule = "panoply.txt"
        if parameter.color_rule_divergent:
            color_rule = clr.write_color_rule(
                parameter.color_rule_divergent,
                divergent=True,
                min_value=abs_min,
                max_value=abs_max,
                outfile_name=f"{parameter.variable}_divergent.txt",
            )
            color_rule = color_rule.name
        elif parameter.color_rule:
            color_rule = parameter.color_rule

        # Render maps.
        gis.make_maps(
            fig_width=fig_width,
            fig_height=fig_height,
            number_of_cols=number_of_cols,
            number_of_rows=number_of_rows,
            background_color="white",
            file_types=[k.PNG, k.PS],
            color_rule=color_rule,
        )

        # Raster statistics and reports.
        if parameter.raster_stats:
            stats.raster_statistics(output_subdir=parameter.output_dir)
        if parameter.plot:
            report.generate_histogram_page(legend_string=parameter.variable)

    print(f"\nDone: '{parameter.variable}' -> {parameter.output_dir}\n")
