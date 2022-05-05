import json
import gis_init as ini

# Also need to figure out all required GIS layers

andalusia = f"""
{{
    "latlong_session" : {{
        "gisdb": "{ini.gisdb}",
        "location": "latlong_medgold",
        "mapset": "medgold"
    }},
    "mapping_session" : {{
        "gisdb": "{ini.gisdb}",
        "location": "laea_andalusia",
        "mapset": "medgold"
    }},
    "mapping_data" : {{
        "digital_elevation": "elevation_1KMmd_GMTEDmd_andalusia",
        "shaded_relief": "SR_HR_andalusia_clip_250m",
        "coastline": "ne_10m_coastline_andalusia",
        "test_interpolation": "bspline_Olive_30set19_00002_OfPupSum"
    }}
}}
"""
andalusia = json.loads(andalusia)
