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
        "coastline": {
            "map_name": "ne_10m_coastline_andalusia",
            "color": "150:150:150",
            "width": 3
        },
        "countries": {
            "map_name": "ne_10m_admin_0_countries_lakes_andalusia",
            "color": "128:128:128",
            "width": 3
        },
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
    },
    "room_for_bottom_legend": 0.37,
    "region_settings": {
        "full": {
            "north": "n+7000",
            "south": "s-7000",
            "east": "e+7000",
            "west": "w-7000",
            "resolution": 1000
        },
        "subset": {
            "north": "n+7000",
            "south": "s-7000",
            "east": "e+7000",
            "west": "w-7000",
            "resolution": 1000
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
        "coastline": {
            "map_name": "ne_10m_coastline_colombia",
            "color": "150:150:150",
            "width": 4
        },
        "countries": {
            "map_name": "ne_10m_admin_0_countries_lakes_colombia",
            "color": "128:128:128",
            "width": 4
        },
        "target_region": {
            "map_name": "colombia",
            "color": "23:23:23",
            "width": 10
        },
        "admin_divisions": {
            "map_name": "colombia_departments",
            "color": "23:23:23",
            "width": 3,
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
    },
    "room_for_bottom_legend": 0.37,
    "region_settings": {
        "full": {
            "north": "n-70000",
            "south": "s-50000",
            "east": "e+50000",
            "west": "w+233000",
            "resolution": 1000
        },
        "subset": {
            "north": "n+50000",
            "south": "s-50000",
            "east": "e+50000",
            "west": "w-50000",
            "resolution": 1000
        }
    }
}
