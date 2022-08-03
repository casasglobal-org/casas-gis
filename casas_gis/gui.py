# %Module
# %  description: Map and analyze the output of CASAS Global physiologically based demographic models (CASAS-PBDMs) for Colombia departments using GRASS GIS
# %  keywords: MED-GOLD project, GRASS GIS, physiologically based demographic, models (PBDM), coffee, agroecosystem analysis
# %End 

# %option
# % guisection: Main
# % key: savedir
# % type: string
# % description: Name for directory where to store output maps
# % required: yes
# %end

# %option
# % guisection: Main
# % key: longitude
# % type: integer
# % answer: 4
# % description: Longitude (X) column number
# % required: yes
# %end

# %option
# % guisection: Main
# % key: latitude
# % type: integer
# % answer: 5
# % description: Latitude (Y) column number
# % required: yes
# %end

# %option
# % guisection: Main
# % key: year
# % type: integer
# % answer: 11
# % description: Year column number
# % required: yes
# %end

# %option
# % guisection: Main
# % key: parameter
# % type: integer
# % description: Parameter to map
# % required : yes
# %end

# %option
# % guisection: Main
# % key: interpolation
# % type: string
# % options: idw,bspline
# % answer: bspline
# % description: Interpolation method
# % required : yes
# %end

# %option
# % guisection: Main
# % key: numpoints
# % type: integer
# % answer: 3
# % description: Number of interpolation points (only used with interpolation method IDW)
# % required : yes
# %end

# %option
# % guisection: Main
# % key: legend1
# % type: string
# % description: Text for legend - first line (file name of HTML summary)
# % required: yes
# %end

# %option
# % guisection: Color rules
# % key: colorruledivergent
# % type: string
# % answer: 32:96:255-32:159:255-32:191:255-0:207:255-42:255:255-85:255:255-127:255:255-170:255:255-255:255:84-255:240:0-255:191:0-255:168:0-255:138:0-255:112:0-255:77:0-255:0:0
# % description: Select or input a DIVERGENT color pattern (hyphen-separated) using standard GRASS colors (see r.colors manual page for color names) or R:G:B triplets
# %end

# %option
# % guisection: Color rules
# % key: colorruleregular
# % type: string
# % answer: 255:255:255-204:204:204-150:150:150-150:150:150-99:99:99-99:99:99-37:37:37-37:37:37
# % description: Select or input a REGULAR color pattern (hyphen-separated) using standard GRASS colors (see r.colors manual page for color names) or R:G:B triplets
# %end

# %option
# % guisection: Color rules
# % key: lowbarcol
# % type: double
# % description: Lower limit for legend color bar when -w option is enabled
# %end

# %option
# % guisection: Color rules
# % key: upbarcol
# % type: double
# % description: Upper limit for legend color bar when -w option is enabled
# %end

# %flag
# % guisection: Color rules
# % key: w
# % description: Modify extent of legend color bar (using low and high input values)
# %end

# %flag
# % guisection: Color rules
# % key: g
# % description: Black and white output instead of color
# %end

# %flag
# % guisection: Color rules
# % key: e
# % description: Use histogram-equalized color rule
# %end

# %flag
# % guisection: Color rules
# % key: l
# % description: Logarithmic scaling
# %end

# %flag
# % guisection: Color rules
# % key: x
# % description: Use an overall (compound) range for all maps (absolute max and min)
# %end

# %flag
# % guisection: Color rules
# % key: a
# % description: Use also same legend bar for all maps (i.e. bar will extend to overall max and min)
# %end

# %flag
# % guisection: Color rules
# % key: d
# % description: Use divergent, zero-centered color pattern (requires positive max and negative min)
# %end

# %option
# % key: lowercut
# % type: double
# % answer: 0
# % description: Cutting point to mask low values
# % required: yes
# %end

# %option
# % key: uppercut
# % type: double
# % answer: 0
# % description: Cutting point to mask high values (please, also check option -u Use cutting point to mask high values)
# % required: yes
# %end

# %option
# % key: departments
# % type: string
# % options: all,CO-NAR,CO-PUT,CO-CHO,CO-GUA,CO-VAU,CO-AMA,CO-LAG,CO-CES,CO-NSA,CO-ARA,CO-BOY,CO-VID,CO-CAU,CO-VAC,CO-ANT,CO-COR,CO-SUC,CO-BOL,CO-ATL,CO-MAG,CO-SAP,CO-CAQ,CO-HUI,CO-GUV,CO-CAL,CO-CAS,CO-MET,CO-CUN,CO-SAN,CO-TOL,CO-QUI,CO-CUN,CO-RIS
# % answer: all
# % description: Specify multiple departments to map (comma separated). Use the word all to map them all. For departments, use codes defined as follows: CO-NAR = Nariño, CO-PUT = Putumayo, CO-CHO = Chocó, CO-GUA = Guainía, CO-VAU = Vaupés, CO-AMA = Amazonas, CO-LAG = La Guajira, CO-CES = Cesar, CO-NSA = Norte de Santander, CO-ARA = Arauca, CO-BOY = Boyacá, CO-VID = Vichada, CO-CAU = Cauca, CO-VAC = Valle del Cauca, CO-ANT = Antioquia, CO-COR = Córdoba, CO-SUC = Sucre, CO-BOL = Bolívar, CO-ATL = Atlántico, CO-MAG = Magdalena, CO-SAP = San Andrés y Providencia, CO-CAQ = Caquetá, CO-HUI = Huila, CO-GUV = Guaviare, CO-CAL = Caldas, CO-CAS = Casanare, CO-MET = Meta, CO-CUN = Bogota, CO-SAN = Santander, CO-TOL = Tolima, CO-QUI = Quindío, CO-CUN = Cundinamarca, CO-RIS = Risaralda
# % multiple: yes
# % required: yes
# %end

# %option
# % key: crop
# % type: string
# % options: coffee,none
# % answer: coffee
# % description: Constrain output map to crop growing area. If coffee is used, it is possible to select a threshold for crop harvested area fraction above which mapping will occur.
# % required : yes
# %end

# %option
# % key: cropthreshold
# % type: double
# % answer: 0.01
# % description: Threshold for crop harvested area fraction above which mapping will occur (output will not be mapped below the threshold)
# % required: yes
# %end

# %option
# % key: alt
# % type: double
# % answer: 10000
# % description: Altitude (meters) above which to clip
# % required: yes
# %end

# %option
# % key: resolution
# % type: string
# % options: 1,2,4
# % answer: 1
# % description: Resolution of output figure (single = 1, double = 2, quad = 4)
# % required: yes
# %end

# %flag
# % key: u
# % description: Use cutting point to mask high values
# %end

# %flag
# % key: c
# % description: Do not interpolate stations above clipping altitude
# %end

# %flag
# % key: r
# % description: Write a report with raster statistics
# %end

# %flag
# % key: p
# % description: Produce bar chart plots summarizing raster statistics
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
