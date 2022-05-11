import pathlib
import locations as loc

# Specify (existing) locations and mapsets
latlong_session = loc.colombia["latlong_session"]
mapping_session = loc.colombia["mapping_session"]
mapping_data = loc.colombia["mapping_data"]

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
INTERPOLATION_PREFIXES = {IDW_PREFIX, BSPLINE_PREFIX}

DRAPE_PREFIX = "drape_"
REGION_RASTER = "mapping_region"
NO_BG_COLOR = "none"

BASE_PAPER_SIDE = 5
