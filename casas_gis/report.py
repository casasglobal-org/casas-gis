#!/usr/bin/env python3
#
# AUTHOR(S):    Luigi Ponti quartese gmail com
# AUTHOR(S):    Luca Delucchi, luca delucchi fmach it, Fondazione Edmund Mach
# AUTHOR(S):    big-pickle AI model
#
# PURPOSE:      Get an HTML report where results of the mapping and
#               analysis are reported.
#
# NOTE:         Migrated from casas_gis_old/PerlScripts/htmlSum.pl and
#               casas_gis_old/PerlScripts/HtmlPlotA.pl / HtmlPlotB.pl /
#               HtmlPlotC.pl
#
# Copyright:    (c) 2021-2024 CASAS (Center for the Analysis
#                   of Sustainable Agricultural Systems).
#                   https://www.casasglobal.org/).
#
#               SPDX-License-Identifier: GPL-3.0-or-later

"""Get an HTML report where results of the mapping and analysis are
reported (see e.g., https://jackbakerds.com/posts/
python-equivalent-rmarkdown/)."""

import html as html_module
import pathlib

import constants as k

HTML_HEADER = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" \
"http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<title>{title}</title>
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1" >
</head>
<body>
"""


def _html_page(title, save_dir, body_fragment):
    """Write a minimal HTML page and return the output file path.

    Args:
        title (str): Page title (also used as the output file name).
        save_dir (str): Directory where the HTML file is written.
        body_fragment (str): HTML body content.

    Returns:
        pathlib.Path: Path of the written HTML file."""
    outfile = pathlib.Path(save_dir) / f"{title}.html"
    with open(outfile, "w") as f:
        f.write(HTML_HEADER.format(title=html_module.escape(title)))
        f.write(body_fragment)
        f.write("</body>\n</html>\n")
    print(f"\nReport written to {outfile}\n")
    return outfile


def generate_summary_page(
    save_dir: str,
    legend_string: str,
    map_par: str,
    lower_cut: float = 0,
    upper_cut: float = 0,
    alt_clip: float = None,
    surf_cut: str = None,
    eto_clip: str = None,
    plots: bool = False,
    log_file: str = None,
):
    """Generate an HTML visual summary for CASAS maps, as done by
    htmlSum.pl. All PNG maps found in save_dir are shown next to
    their "_stats.txt" reports, followed by mapping parameters and
    the input file log.

    Args:
        save_dir (str): Directory containing the PNG maps and where
            the report is written.
        legend_string (str): Legend/summary string used as report
            title and file name.
        map_par (str): Name of the mapped parameter.
        lower_cut (float): Lower cutting point of the interpolation.
        upper_cut (float): Upper cutting point of the interpolation.
        alt_clip (float, optional): Altitude clip in meters.
        surf_cut (str, optional): Whether stations above the altitude
            clip were used to interpolate.
        eto_clip (str, optional): Name of the region clip dataset.
        plots (bool): Whether to link the PLOT (barchart/histogram)
            pages. Defaults to False.
        log_file (str, optional): Path of the input file log to embed
            in the report.

    Returns:
        pathlib.Path: Path of the written HTML summary page."""
    save_path = pathlib.Path(save_dir)
    body = []
    body.append(f"\n<h1>Report for " f'"{html_module.escape(legend_string)}"</h1>')
    body.append("\n<h2>Output maps</h2>")
    for filepath in sorted(save_path.glob("*.png")):
        if "PLOT" in filepath.name or "HIST" in filepath.name:
            continue
        stem = filepath.stem
        stats_file = save_path / f"{stem}.txt"
        if stats_file.exists():
            body.append(
                f'<a href="{stem}.txt">' f'<img src="{stem}.png" width="32%"></a>'
            )
        else:
            body.append(f'<img src="{stem}.png" width="32%">')
    body.append("\n<p><i>Please, click on images to see stat report.</i></p>")

    if plots:
        body.append(
            "\n<p><i>You may also see raster statistics as barcharts "
            '(<a href="'
            f"{html_module.escape(legend_string)}-PLOTa.html"
            '" target="_blank">zoned</a> and <a href="'
            f"{html_module.escape(legend_string)}-PLOTb.html"
            '" target="_blank">overall</a>) and as cell frequency '
            f'<a href="{html_module.escape(legend_string)}-PLOTc.html" '
            'target="_blank">histogram</a>.</i></p>'
        )

    body.append("\n<h2>Mapping parameters</h2>")
    body.append("\n<ul>")
    body.append(f"\n<li>Parameter mapped: {html_module.escape(map_par)}")
    body.append(f"\n<li>Lower cutting point: {lower_cut}")
    body.append(f"\n<li>Upper cutting point: {upper_cut}")
    body.append(f"\n<li>Region clip: {html_module.escape(str(eto_clip))}")
    if alt_clip is not None:
        body.append(f"\n<li>Altitude clip: {alt_clip} m")
    if surf_cut is not None:
        body.append(
            f"\n<li>Stations above altitude clip were used to "
            f"interpolate: {html_module.escape(surf_cut)}"
        )
    body.append("\n</ul>")

    if log_file:
        body.append("\n<h2>Input file log</h2>")
        log_path = pathlib.Path(log_file)
        if log_path.exists():
            with open(log_path) as f:
                for line in f:
                    line = line.rstrip("\n")
                    if line.strip() == "":
                        continue
                    if " " in line:
                        body.append(f"\n{html_module.escape(line)}<br>")
                    else:
                        body.append("\n<ul>")
                        body.append(f"\n<li>{html_module.escape(line)}</li>")
                        body.append("\n</ul>")

    return _html_page(legend_string, save_dir, "".join(body))


def generate_histogram_page(
    save_dir: str = None, legend_string: str = "histogram", stats_files: list = None
):
    """Generate a simple HTML page summarizing raster statistics for the
    interpolated maps (histogram/barchart placeholder, replacing the
    gnuplot-based HtmlPlot*.pl pages). In current implementation maps
    are listed next to their statistics; charts can later be attached
    by adding plotting support (e.g., matplotlib).

    Args:
        save_dir (str, optional): Directory where the page is written;
            defaults to constants.REPORT_DIR.
        legend_string (str): Legend string used in the page title.
            Defaults to "histogram".
        stats_files (list, optional): Paths of the statistics text
            files to include in the page.

    Returns:
        pathlib.Path: Path of the written HTML page."""
    save_path = pathlib.Path(save_dir) if save_dir else k.REPORT_DIR
    stats_files = stats_files or []
    body = [f'\n<h1>Raster statistics for "{legend_string}"</h1>\n']
    for stats_file in stats_files:
        stats_path = pathlib.Path(stats_file)
        if stats_path.exists():
            body.append(
                f'<h2><a href="{stats_path.name}">{stats_path.name}</a></h2>' "\n<pre>"
            )
            with open(stats_path) as f:
                body.append(html_module.escape(f.read()[:4000]))
            body.append("</pre>\n<hr>\n")
    return _html_page(f"{legend_string}-PLOTc", save_path, "".join(body))


def build_log_file(
    variable: str, input_files: list, log_dir: str = None, extra_lines: list = None
):
    """Write the input file log used by generate_summary_page, as done
    by the legacy grass_scripts (e.g., "$LegendString.log").

    Args:
        variable (str): Variable name used as the log file name.
        input_files (list): Paths of the input files logged.
        log_dir (str, optional): Directory where the log is written;
            defaults to constants.REPORT_DIR.
        extra_lines (list, optional): Additional lines prepended to
            the log.

    Returns:
        pathlib.Path: Path of the written log file."""
    log_dir = pathlib.Path(log_dir) if log_dir else k.REPORT_DIR
    log_file = log_dir / f"{variable}.log"
    with open(log_file, "w") as f:
        for line in extra_lines or []:
            f.write(f"{line}\n")
        for input_file in input_files:
            f.write(f"{pathlib.Path(input_file).name}\n")
    print(f"\nLog written to {log_file}\n")
    return log_file
