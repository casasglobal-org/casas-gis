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
        "coastline": "ne_10m_coastline_andalusia",
        "country_border": "ne_10m_admin_0_countries_lakes_andalusia",
        "admin_divisions": {{
            "map_name": "andalusia_provinces",
            "column": "iso_3166_2"
        }},
        "digital_elevation": "elevation_1KMmd_GMTEDmd_andalusia",
        "shaded_relief": "SR_HR_andalusia_clip_250m",
        "grey_shaded_relief": "GRAY_HR_SR_OB_DR_andalusia_250m",
        "satellite_landuse": "NE1_HR_LC_SR_W_DR.composite_andalusia_250m",
        "crop": {{
            "harvest_area_fraction": "olive_HarvestedAreaFraction_andalusia",
            "area_sigpac_3km": "olive_monoculture_sigpac_2018_3km",
            "area_sigpac_buffered_5km":
                "olive_monoculture_sigpac_2018_grow_5000",
            "area_sigpac_buffered_3km":
                "olive_monoculture_sigpac_2018_grow_3000"
        }}
    }}
}}
"""
andalusia = json.loads(andalusia)

# Next is Colombia and then everything else
