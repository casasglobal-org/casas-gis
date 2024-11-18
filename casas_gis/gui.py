#!/usr/bin/env python3
#
# AUTHOR(S):    Luigi Ponti quartese gmail com
#
# PURPOSE:      
#
# NOTE:         
#
# COPYRIGHT:    (c) 2021-2024 CASAS (Center for the Analysis
#                   of Sustainable Agricultural Systems).
#                   https://www.casasglobal.org/).
#
#               SPDX-License-Identifier: GPL-3.0-or-later


# %Module
# %  description: CASAS GIS
# %End

# %option
# % guisection: Main
# % key: savedir
# % type: string
# % description: Name for directory where to store output maps
# % required: yes
# %end


import os
import pathlib
import constants as k

from dotenv import load_dotenv

load_dotenv()  # needed for grass_session

from grass_session import Session  # noqa E402
import grass.script as grass  # noqa E402

# grassbin = os.getenv("GRASSBIN")

current_dir = pathlib.Path(__file__).parent
print(current_dir)
os.environ["GRASS_ADDON_PATH"] = str(current_dir)


def main():
    print(options["savedir"])
    return 0


if __name__ == "__main__":
    with Session(**k.latlong_session):
        options, flags = grass.parser()
        main()
