# casas-gis

- The functionality is already in a Bash (GRASS, <https://grass.osgeo.org/>) GIS script.
- This is how to start turning it into a Python app <https://grass.osgeo.org/grass79/manuals/libpython/script_intro.html>
- Converting Bash scripts to Python <https://grasswiki.osgeo.org/wiki/Converting_Bash_scripts_to_Python>
- The script also calls some Perl scripts that do text manipulation (I think those should be relatively straightforward to turn into Python modules).
- Should the Bash and Perl scripts included in the repo somehow as a reference
- How to write a Python tool for GRASS <https://github.com/wenzeslaus/python-grass-addon>

## Basic workflow of `gis_script.sh` is as follows

1. import CSV file with latitude and longitude fields plus other variables one would like to map
2. use the imported vector file (they are points, e.g. geographic coordinates plus the value of a certain variable at each point) to get a raster surface using interpolation
3. give the raster surface the right extent, color, etc. and put it on top of other information layers such as a shaded relief map that gives you an idea of what the terrain looks like
4. save maps to PNG output files
5. compute statistics with the interpolated raster (etc.)
6. display a visual summary as a web page (saved PNGs, links to statistics, log of commands and settings used for the mapping task).
