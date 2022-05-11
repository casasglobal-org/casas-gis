import gis_init as ini

andalusia = {
    "latlong_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "latlong_medgold",
        "mapset": "medgold"
    },
    "mapping_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "laea_andalusia",
        "mapset": "medgold"
    },
    "mapping_data": {
        "coastline": "ne_10m_coastline_andalusia",
        "countries": "ne_10m_admin_0_countries_lakes_andalusia",
        "target_region": "andalusia",
        "admin_divisions": {
            "map_name": "andalusia_provinces",
            "column": "iso_3166_2",
            "division_names": [
                "ES-CA", "ES-H", "ES-AL", "ES-GR",
                "ES-MA", "ES-SE", "ES-CO", "ES-J"
                ]
        },
        "digital_elevation": "elevation_1KMmd_GMTEDmd_andalusia",
        "shaded_relief": "SR_HR_andalusia_clip_250m",
        "grey_shaded_relief": "GRAY_HR_SR_OB_DR_andalusia_250m",
        "satellite_landuse": "NE1_HR_LC_SR_W_DR.composite_andalusia_250m",
        "crop": {
            "harvest_area_fraction": "olive_HarvestedAreaFraction_andalusia",
            "area_sigpac_3km": "olive_monoculture_sigpac_2018_3km",
            "area_sigpac_buffered_5km":
                "olive_monoculture_sigpac_2018_grow_5000",
            "area_sigpac_buffered_3km":
                "olive_monoculture_sigpac_2018_grow_3000"
        }
    }
}

colombia = {
    "latlong_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "latlong_medgold",
        "mapset": "medgold"
    },
    "mapping_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "laea_colombia",
        "mapset": "medgold"
    },
    "mapping_data": {
        "coastline": "ne_10m_coastline_colombia",
        "countries": "ne_10m_admin_0_countries_lakes_colombia",
        "target_region": "colombia",
        "admin_divisions": {
            "map_name": "colombia_departments",
            "column": "iso_3166_2",
            "division_names": [
                "CO-NAR", "CO-PUT", "CO-CHO", "CO-GUA", "CO-VAU",
                "CO-AMA", "CO-LAG", "CO-CES", "CO-NSA", "CO-ARA",
                "CO-BOY", "CO-VID", "CO-CAU", "CO-VAC", "CO-ANT",
                "CO-COR", "CO-SUC", "CO-BOL", "CO-ATL", "CO-MAG",
                "CO-SAP", "CO-CAQ", "CO-HUI", "CO-GUV", "CO-CAL",
                "CO-CAS", "CO-MET", "CO-CUN", "CO-SAN", "CO-TOL",
                "CO-QUI", "CO-CUN", "CO-RIS"
                ]
        },
        "digital_elevation": "elevation_1KMmd_GMTEDmd_colombia",
        "shaded_relief": "SR_HR_colombia_clip",
        "grey_shaded_relief": "GRAY_HR_SR_OB_DR_colombia",
        "satellite_landuse": "NE1_HR_LC_SR_W_DR.composite_colombia",
        "crop": {
            "harvest_area_fraction": "coffee_HarvestedAreaFraction_colombia"
        }
    }
}
