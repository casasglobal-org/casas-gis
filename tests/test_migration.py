#!/usr/bin/env python3
#
# AUTHOR(S):    Luigi Ponti quartese gmail com
# AUTHOR(S):    Luca Delucchi, luca delucchi fmach it, Fondazione Edmund Mach
# AUTHOR(S):    big-pickle AI model
#
# PURPOSE:      Tests for the modules migrated from casas_gis_old.
#
# Copyright:    (c) 2021-2024 CASAS (Center for the Analysis
#                   of Sustainable Agricultural Systems).
#                   https://www.casasglobal.org/).
#
#               SPDX-License-Identifier: GPL-3.0-or-later

"""Unit tests for the pure-Python (non-GRASS) parts migrated from
the legacy bash/Perl scripts. GRASS-dependent tests go in
test_casas_gis.py."""

import os
from pathlib import Path

import pytest

import locations as loc
import report

# batch.py and stats.py require a GRASS installation for some of their
# imports; keep pure helpers testable here when GRASS is not available.
try:
    from batch import (
        BatchParameter,
        OLIVE_PLANT_PARAMETERS,
        OLIVE_FLY_PARAMETERS,
        resolve_crop_map,
    )
except ImportError:
    BatchParameter = None
    OLIVE_PLANT_PARAMETERS = None
    OLIVE_FLY_PARAMETERS = None
    resolve_crop_map = None

try:
    from stats import compute_delta, compute_model_output_delta
except ImportError:  # pragma: no cover
    compute_delta = None
    compute_model_output_delta = None


def test_all_regions_available():
    """Check that all ten expected region names are configured.

    Returns:
        None."""
    expected = {
        "andalusia",
        "colombia",
        "mediterranean",
        "usa",
        "africa",
        "india",
        "libya_tunisia",
        "europe_grape",
        "italy",
        "world",
    }
    assert set(loc.regions) == expected


@pytest.mark.parametrize("region", loc.regions)
def test_region_config_required_keys(region):
    """Check that a region configuration dict has the required keys.

    Args:
        region (str): Name of the configured region.

    Returns:
        None."""
    cfg = loc.regions[region]
    assert "latlong_session" in cfg
    assert "mapping_session" in cfg
    assert "mapping_data" in cfg
    assert "legend_settings" in cfg
    assert "region_settings" in cfg
    for session in ("latlong_session", "mapping_session"):
        assert "gisdb" in cfg[session]
        assert "location" in cfg[session]
        assert "mapset" in cfg[session]
    assert "digital_elevation" in cfg["mapping_data"]
    assert "resolution" in cfg["region_settings"]["full"]


def test_constants_region_selection(monkeypatch):
    """Check that the CASAS_REGION variable selects matching constants.

    Args:
        monkeypatch (pytest.MonkeyPatch): Fixture to set environment.

    Returns:
        None."""
    import constants as k
    import importlib

    monkeypatch.setenv("CASAS_REGION", "italy")
    importlib.reload(k)
    assert k.mapping_session["location"] == "EurLCC"
    assert k.latlong_session["location"] == "latlong"
    monkeypatch.delenv("CASAS_REGION")
    importlib.reload(k)
    assert k.mapping_session["location"] == "laea_colombia"


@pytest.mark.skipif(BatchParameter is None, reason="GRASS not available")
def test_batch_parameter_defaults():
    """Check the default values of a BatchParameter.

    Returns:
        None."""
    p = BatchParameter(
        column=28, variable="OfPupSum", output_dir="out", legend="olive fly pupae"
    )
    assert p.lower_cut == 0
    assert p.upper_cut == 0
    assert p.altitude == 2000
    assert p.interpolation == "idw"
    assert p.numpoints == 3
    assert p.clip is False
    assert p.plot is False
    assert p.mask is False
    assert p.idw_power == 2.0


@pytest.mark.skipif(OLIVE_FLY_PARAMETERS is None, reason="GRASS not available")
def test_batch_olive_parameter_lists():
    """Check that the olive parameter lists contain expected variables.

    Returns:
        None."""
    variables = {p.variable for p in OLIVE_PLANT_PARAMETERS}
    assert "dd" in variables
    assert "FruWgt" in variables
    assert "Bloomday" in variables
    fly = {p.variable for p in OLIVE_FLY_PARAMETERS}
    assert "OfPupSum" in fly
    assert "PrcntAtkd" in fly


@pytest.mark.skipif(resolve_crop_map is None, reason="GRASS not available")
def test_batch_resolve_crop_map():
    """Check crop map resolution for a region without a configured crop.

    Returns:
        None."""
    # No crop configured for libya_tunisia
    assert resolve_crop_map("coffee") is None
    assert resolve_crop_map(None) is None
    assert resolve_crop_map("none") is None


def test_report_summary_page(tmp_path):
    """Check that a summary HTML page is written with expected content.

    Args:
        tmp_path (pathlib.Path): Temporary directory fixture.

    Returns:
        None."""
    (tmp_path / "idw_test.png").write_bytes(b"x")
    (tmp_path / "idw_test.txt").write_text("min: 0\nmax: 10\n")
    outfile = report.generate_summary_page(
        str(tmp_path),
        "TestMap",
        map_par="dd",
        lower_cut=0,
        upper_cut=0,
        alt_clip=900,
        eto_clip="-1",
        plots=True,
    )
    content = Path(outfile).read_text()
    assert "TestMap" in content
    assert "idw_test.png" in content
    assert "idw_test.txt" in content
    assert "900" in content


def test_report_histogram_page(tmp_path):
    """Check that a histogram HTML page is written with expected content.

    Args:
        tmp_path (pathlib.Path): Temporary directory fixture.

    Returns:
        None."""
    stats_file = tmp_path / "idw_test_stats.txt"
    stats_file.write_text("min: 0\nmax: 10\n")
    outfile = report.generate_histogram_page(
        save_dir=str(tmp_path), legend_string="dd", stats_files=[stats_file]
    )
    content = Path(outfile).read_text()
    assert "idw_test_stats.txt" in content


def test_report_log_file(tmp_path):
    """Check that the log file reports the input file list.

    Args:
        tmp_path (pathlib.Path): Temporary directory fixture.

    Returns:
        None."""
    log_file = report.build_log_file(
        "dd", ["input1.txt", "input2.txt"], log_dir=str(tmp_path)
    )
    content = Path(log_file).read_text()
    assert "input1.txt" in content
    assert "input2.txt" in content


@pytest.mark.skipif(compute_delta is None, reason="GRASS not available")
def test_delta_computation():
    """Check the delta computation between two model output data frames.

    Returns:
        None."""
    import pandas as pd

    warm = pd.DataFrame(
        {
            "file": ["a", "b"],
            "lon": [1, 2],
            "lat": [3, 4],
            "year": [2000, 2001],
            "dd": [10, 20],
            "rain": [100, 200],
            "name": ["x", "y"],
        }
    )
    obs = pd.DataFrame(
        {
            "file": ["a", "b"],
            "lon": [1, 2],
            "lat": [3, 4],
            "year": [2000, 2001],
            "dd": [5, 8],
            "rain": [80, 150],
            "name": ["x", "y"],
        }
    )
    diff = compute_delta(warm, obs, ncols_first=4)
    assert diff["dd"].tolist() == [5.0, 12.0]
    assert diff["rain"].tolist() == [20.0, 50.0]
    assert diff["name"].tolist() == ["x", "y"]
    assert diff["year"].tolist() == [2000, 2001]


@pytest.mark.skipif(compute_model_output_delta is None, reason="GRASS not available")
def test_delta_to_file(tmp_path):
    """Check that the model output delta is computed and written to file.

    Args:
        tmp_path (pathlib.Path): Temporary directory fixture.

    Returns:
        None."""
    import pandas as pd

    warm = pd.DataFrame(
        {"file": ["a"], "lon": [1], "lat": [3], "year": [2000], "dd": [10]}
    )
    obs = pd.DataFrame(
        {"file": ["a"], "lon": [1], "lat": [3], "year": [2000], "dd": [5]}
    )
    warm.to_csv(tmp_path / "warm.txt", sep="\t", index=False)
    obs.to_csv(tmp_path / "obs.txt", sep="\t", index=False)
    compute_model_output_delta(
        str(tmp_path), "warm.txt", "obs.txt", "diff.txt", ncols_first=4
    )
    diff = pd.read_csv(tmp_path / "diff.txt", sep="\t")
    assert diff["dd"].tolist() == [5.0]


def test_write_color_rule(tmp_path):
    """Check that a divergent color rule file contains the zero value.

    Args:
        tmp_path (pathlib.Path): Temporary directory fixture.

    Returns:
        None."""
    from color import write_color_rule

    panoply = (
        "4:14:216-32:80:255-65:150:255-109:193:255"
        "-134:217:255-156:238:255-175:245:255-206:255:255"
        "-255:254:71-255:235:0-255:196:0-255:144:0"
        "-255:72:0-255:0:0-213:0:0-158:0:0"
    )
    outfile = write_color_rule(
        panoply,
        min_value=-100,
        max_value=100,
        divergent=True,
        outfile_name="test_rule.txt",
    )
    content = Path(outfile).read_text()
    outfile.unlink()
    assert "end" in content
    # Center (0) must be present in a divergent rule.
    numbers = [
        float(line.split()[0])
        for line in content.strip().splitlines()
        if not line.startswith("#") and line != "end"
    ]
    assert 0 in numbers


def test_geotiff_constants_present():
    """Check that the output format constants are as expected.

    Returns:
        None."""
    import constants as k

    assert k.PNG == "png"
    assert k.PS == "ps"
    assert k.IDW == "idw"
    assert k.BSPLINE == "bspline"


def test_color_rule_files_portable():
    """Check that the migrated color rule files are shipped.

    Returns:
        None."""
    color_dir = Path(os.path.dirname(os.path.abspath(report.__file__)))
    color_rules = color_dir / "color_rules"
    assert color_rules.exists()
    files = set(p.name for p in color_rules.iterdir())
    # At least the palette files migrated from casas_gis_old.
    assert "defaultColorRule_Panoply" in files
    assert "panoply.txt" in files
    assert "defaultColorRule_turbo" in files
