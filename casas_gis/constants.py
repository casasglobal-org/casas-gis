import pathlib

# Temporary directory for text files
TMP_DIR = pathlib.Path(__file__).parent / "tmp"
pathlib.Path(TMP_DIR).mkdir(parents=True, exist_ok=True)

# Directory for GIS output files
OUT_DIR = pathlib.Path(__file__).parent / "out"
pathlib.Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

# Directory for PNG output files
PNG_DIR = OUT_DIR / "png"
pathlib.Path(PNG_DIR).mkdir(parents=True, exist_ok=True)

# Directory for PostScript output files
PS_DIR = OUT_DIR / "postscript"
pathlib.Path(PS_DIR).mkdir(parents=True, exist_ok=True)

# Directory for report files
REPORT_DIR = OUT_DIR / "reports"
pathlib.Path(REPORT_DIR).mkdir(parents=True, exist_ok=True)


# Output file extensions
# See 162. Enumerations in Pybites book
PNG = "png"
PS = "ps"
EPS = "eps"
PDF = "pdf"
SVG = "svg"
SUPPORTED_FILE_TYPES = {PNG, PS}

IDW = "idw"
BSPLINE = "bspline"
INTERPOLATION_METHODS = {IDW, BSPLINE}

IMPORTED_PREFIX = "imp_"
SELECTED_PREFIX = "sel_"
IDW_PREFIX = "idw_"
BSPLINE_PREFIX = "bspline_"
REGION_RASTER = "mapping_region"
NO_BG_COLOR = "none"

# DATA
# define GRASS DATABASE
# add your path to grassdata (GRASS GIS database) directory
gisdb = pathlib.Path.home() / "grassdata"
# the following path is the default path on MS Windows
# gisdb = os.path.join(os.path.expanduser("~"), "Documents/grassdata")
print(gisdb)

# Specify (existing) locations and mapsets
latlong_session = {"gisdb": f"{gisdb}",
                   "location": "latlong_medgold",
                   "mapset": "medgold"}
mapping_session = {"gisdb": f"{gisdb}",
                   "location": "laea_andalusia",
                   "mapset": "medgold"}

# Add here another dictionary with GIS mapping data
# for a particular mapping session, e.g.,
mapping_data = {"digital_elevation": "elevation_1KMmd_GMTEDmd_andalusia",
                "shaded relief": "SR_HR_andalusia_clip_250m",
                "coastline": "ne_10m_coastline_andalusia",
                # etc.
                "test_interpolation": "bspline_Olive_30set19_00002_OfPupSum",
                }
