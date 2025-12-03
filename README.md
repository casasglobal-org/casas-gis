# CASAS GIS - Geospatial software based on GRASS GIS

[![DOI](https://zenodo.org/badge/364206056.svg)](https://doi.org/10.5281/zenodo.17551909)

CASAS GIS is software for geospatial mapping and analysis of physiologically based demographic models (PBDMs) developed by [CASAS Global - Center for the Analysis of Sustainable Agricultural Systems](https://www.casasglobal.org/).

## Repository structure

- **casas_gis_old/**: Legacy GRASS GIS scripts used by CASAS Global for [PBDM/GIS analyses](https://www.casasglobal.org/publications/) since 2005
  - Contains Bash shell scripts originally developed for GRASS GIS version 6, currently being transitioned to GRASS GIS version 8
  - Includes Perl scripts for data preprocessing and other utilities
  - Reference implementation of CASAS geospatial analysis workflow
  - Usage documentation: [README_usage_GRASS_GIS6.md](README_usage_GRASS_GIS6.md)

- **casas_gis/**: New Python implementation (under development)
  - Unifies functionality from legacy scripts into a single Python application
  - Built on modern GRASS GIS Python API
  - Aims to provide a more maintainable and user-friendly interface
  - Compatible with current GRASS GIS versions

## Basic CASAS GIS workflow

The core workflow implemented in CASAS GIS scripts follows these steps:

1. Import CSV file containing:
   - Geographic coordinates (latitude/longitude)
   - Variables to be mapped (e.g., model outputs)

2. Create interpolated surfaces:
   - Convert point data to vector format
   - Generate continuous raster surfaces using interpolation

3. Configure map appearance:
   - Set appropriate geographic extent
   - Apply color schemes
   - Overlay with supplementary layers (e.g., shaded relief)

4. Generate outputs:
   - Save maps as PNG files
   - Compute raster statistics
   - Create HTML summary page with:
     - Generated maps
     - Statistical results
     - Processing log

## Development

- Converting legacy Bash/Perl scripts to Python: [GRASS Wiki Guide](https://grasswiki.osgeo.org/wiki/Converting_Bash_scripts_to_Python)
- GRASS Python API documentation: [Script Introduction](https://grass.osgeo.org/grass-stable/manuals/libpython/script_intro.html)
- Python addon development: [Example Repository](https://github.com/wenzeslaus/python-grass-addon)

## Funding

The Center for the Analysis of Sustainable Agricultural Systems (CASAS) has been supported through the Global Collaboration for Resilient Food Systems (CRFS), a program of the McKnight Foundation (grant numbers 22-341 and 24-124; see <https://www.ccrp.org/grants/python-based-platform-to-evaluate-crop-pest-systems/>).

## License

SPDX-License-Identifier: GPL-3.0-or-later

## Authors

- Luigi Ponti (ENEA - Agenzia nazionale per le nuove tecnologie, l'energia e lo sviluppo economico sostenibile / CASAS Global - Center for the Analysis of Sustainable Agricultural Systems)
- Markus Neteler (mundialis GmbH & Co KG / CASAS Global)
