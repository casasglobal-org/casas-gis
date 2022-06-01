""" Color related stuff.
    Select color scheme, adjust to data, etc."""

# https://matplotlib.org/stable/tutorials/colors/colormaps.html
# https://colorcet.holoviz.org/
# https://jiffyclub.github.io/palettable/
# https://seaborn.pydata.org/

import constants as k

import grass.script as grass  # noqa E402


def set_color_rule(raster_map: str,
                   color_rule: str):
    grass.run_command("r.colors",
                      # flags="st",
                      map=raster_map,
                      rules=k.COLOR_DIR / color_rule)
