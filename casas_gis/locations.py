#!/usr/bin/env python3
#
# AUTHOR(S):    Luigi Ponti quartese gmail com
# AUTHOR(S):    Luca Delucchi, luca delucchi fmach it, Fondazione Edmund Mach
# AUTHOR(S):    big-pickle AI model
#
# PURPOSE:
#
# NOTE:
#
# Copyright:    (c) 2021-2024 CASAS (Center for the Analysis
#                   of Sustainable Agricultural Systems).
#                   https://www.casasglobal.org/).
#
#               SPDX-License-Identifier: GPL-3.0-or-later

import gis_init as ini

andalusia = {
    "latlong_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "latlong_medgold",
        "mapset": "medgold",
    },
    "mapping_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "laea_andalusia",
        "mapset": "medgold",
    },
    "mapping_data": {
        "coastline": {
            "map_name": "ne_10m_coastline_andalusia",
            "color": "150:150:150",
            "width": 3,
        },
        "countries": {
            "map_name": "ne_10m_admin_0_countries_lakes_andalusia",
            "color": "128:128:128",
            "width": 3,
        },
        "target_region": "andalusia",
        "admin_divisions": {
            "map_name": "andalusia_provinces",
            "column": "iso_3166_2",
            "division_names": (
                "ES-CA",
                "ES-H",
                "ES-AL",
                "ES-GR",
                "ES-MA",
                "ES-SE",
                "ES-CO",
                "ES-J",
            ),
        },
        "digital_elevation": "elevation_1KMmd_GMTEDmd_andalusia",
        "shaded_relief": "SR_HR_andalusia_clip_250m",
        "grey_shaded_relief": "GRAY_HR_SR_OB_DR_andalusia_250m",
        "satellite_landuse": "NE1_HR_LC_SR_W_DR.composite_andalusia_250m",
        "crop": {
            "harvest_area_fraction": "olive_HarvestedAreaFraction_andalusia",
            "area_sigpac_3km": "olive_monoculture_sigpac_2018_3km",
            "area_sigpac_buffered_5km": "olive_monoculture_sigpac_2018_grow_5000",
            "area_sigpac_buffered_3km": "olive_monoculture_sigpac_2018_grow_3000",
        },
    },
    "legend_settings": {
        "room_for_bottom_legend": 0.37,
        "bottom_location": (6, 10, 20, 80),
        "right_location": (20, 80, 86, 90),
    },
    "region_settings": {
        "full": {
            "north": "n+7000",
            "south": "s-7000",
            "east": "e+7000",
            "west": "w-7000",
            "resolution": 1000,
        },
        "subset": {
            "north": "n+7000",
            "south": "s-7000",
            "east": "e+7000",
            "west": "w-7000",
            "resolution": 1000,
        },
    },
}

colombia = {
    "latlong_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "latlong_medgold",
        "mapset": "medgold",
    },
    "mapping_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "laea_colombia",
        "mapset": "medgold",
    },
    "mapping_data": {
        "coastline": {
            "map_name": "ne_10m_coastline_colombia",
            "color": "150:150:150",
            "width": 4,
        },
        "countries": {
            "map_name": "ne_10m_admin_0_countries_lakes_colombia",
            "color": "128:128:128",
            "width": 4,
        },
        "target_region": {"map_name": "colombia", "color": "23:23:23", "width": 10},
        "admin_divisions": {
            "map_name": "colombia_departments",
            "color": "23:23:23",
            "width": 3,
            "column": "iso_3166_2",
            "division_names": (
                "CO-NAR",
                "CO-PUT",
                "CO-CHO",
                "CO-GUA",
                "CO-VAU",
                "CO-AMA",
                "CO-LAG",
                "CO-CES",
                "CO-NSA",
                "CO-ARA",
                "CO-BOY",
                "CO-VID",
                "CO-CAU",
                "CO-VAC",
                "CO-ANT",
                "CO-COR",
                "CO-SUC",
                "CO-BOL",
                "CO-ATL",
                "CO-MAG",
                "CO-SAP",
                "CO-CAQ",
                "CO-HUI",
                "CO-GUV",
                "CO-CAL",
                "CO-CAS",
                "CO-MET",
                "CO-CUN",
                "CO-SAN",
                "CO-TOL",
                "CO-QUI",
                "CO-CUN",
                "CO-RIS",
            ),
        },
        "digital_elevation": "elevation_1KMmd_GMTEDmd_colombia",
        "shaded_relief": "SR_HR_colombia_clip",
        "grey_shaded_relief": "GRAY_HR_SR_OB_DR_colombia",
        "satellite_landuse": "NE1_HR_LC_SR_W_DR.composite_colombia",
        "crop": {"harvest_area_fraction": "coffee_HarvestedAreaFraction_colombia"},
    },
    "legend_settings": {
        "room_for_bottom_legend": 0.37,
        "bottom_location": (6, 10, 20, 80),
        "right_location": (20, 80, 86, 90),
    },
    "region_settings": {
        "full": {
            "north": "n-70000",
            "south": "s-50000",
            "east": "e+50000",
            "west": "w+233000",
            "resolution": 1000,
        },
        "subset": {
            "north": "n+50000",
            "south": "s-50000",
            "east": "e+50000",
            "west": "w-50000",
            "resolution": 1000,
        },
    },
}

# The following regions are migrated from the legacy bash scripts in
# casas_gis_old/casas/grass_scripts/. GRASS location and mapset names
# follow the naming used in the original scripts (e.g., "latlong",
# "AEA_Med" etc.), since those refer to existing GIS data.

# From casas_gis_old/casas/grass_scripts/MedPresentClimate
mediterranean = {
    "latlong_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "latlong",
        "mapset": "luigi",
    },
    "mapping_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "AEA_Med",
        "mapset": "luigi",
    },
    "mapping_data": {
        "countries": {
            "map_name": "admin0_10m_naturalEarth_MED",
            "color": "128:128:128",
            "width": 2,
        },
        "admin_divisions": {
            "map_name": "ecoZonesFaoMedOlive",
            "column": "GEZ_CODE",
            "division_names": ("21", "22", "23", "25", "31", "32", "33", "35"),
        },
        "digital_elevation": "era40dem_resamp",
        "shaded_relief": "era40_67_270_10_grow",
        "satellite_landuse": "natural_earth_color.composite",
        "crop": {"harvest_area_fraction": "olive_groves_new_raster_masked_below900"},
    },
    "legend_settings": {
        "room_for_bottom_legend": 0.37,
        "bottom_location": (6, 11, 20, 80),
        "right_location": (20, 80, 86, 90),
    },
    "region_settings": {
        "full": {
            "north": 900000,
            "south": -930000,
            "east": 2050000,
            "west": -2343000,
            "resolution": 3000,
        },
        "subset": {
            "north": 900000,
            "south": -930000,
            "east": 2050000,
            "west": -2343000,
            "resolution": 3000,
        },
    },
}

# From casas_gis_old/casas/grass_scripts/usa
usa = {
    "latlong_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "latlong",
        "mapset": "luigi",
    },
    "mapping_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "AEA_US_mex_central_america",
        "mapset": "luigi",
    },
    "mapping_data": {
        "coastline": {"map_name": "world_bounds", "color": "150:150:150", "width": 2},
        "countries": {
            "map_name": "us_conterm_hawaii_mex_centr_am",
            "color": "128:128:128",
            "width": 3,
        },
        "lakes": {
            "map_name": "US_conterm_lakes_wwf",
            "color": "150:150:150",
            "fill_color": "215:240:255",
        },
        "admin_divisions": {
            "map_name": "us_states_mex",
            "column": "STATE_CODE",
            "division_names": (
                "AL",
                "AZ",
                "CA",
                "FL",
                "GA",
                "LA",
                "MS",
                "MX",
                "NC",
                "NM",
                "SC",
                "TX",
            ),
        },
        "digital_elevation": "US_dem",
        "shaded_relief": "MSR_50M_land",
        "satellite_landuse": "natural_earth_color.composite",
        "crop": {
            "harvest_area_fraction": "tomato_YieldPerHectare_175_above_0_mask",
            "tomato_temperate": "tomato_y_175crops_t_gaez_temperate",
            "tomato_tropical": "tomato_y_175crops_t_gaez_tropical",
            "tomato_combined": "tomato_y_175crops_t_gaez_combined",
            "alfalfa_harvested": "alfalfa_harvarea_usa_binary",
        },
    },
    "legend_settings": {
        "room_for_bottom_legend": 0.37,
        "bottom_location": (6, 10, 20, 80),
        "right_location": (20, 80, 86, 90),
    },
    "region_settings": {
        "full": {
            "north": "n+3328000",
            "south": "s+179000",
            "east": "e+2720000",
            "west": "w-2620000",
            "resolution": 1000,
        },
        "subset": {
            "north": "n+50000",
            "south": "s-50000",
            "east": "e+50000",
            "west": "w-50000",
            "resolution": 3000,
        },
    },
}

# From casas_gis_old/casas/grass_scripts/africa
africa = {
    "latlong_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "latlong",
        "mapset": "luigi",
    },
    "mapping_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "africa_aea",
        "mapset": "luigi",
    },
    "mapping_data": {
        "coastline": {
            "map_name": "coastline_africa",
            "color": "150:150:150",
            "width": 2,
        },
        "countries": {"map_name": "africa", "color": "128:128:128", "width": 3},
        "target_region": {
            "map_name": "africa_region_box",
            "color": "23:23:23",
            "width": 10,
        },
        "lakes": {
            "map_name": "ne_50m_lakes_africa",
            "color": "150:150:150",
            "fill_color": "215:240:255",
        },
        "land_mask": "africa_region_land",
        "admin_divisions": {
            "map_name": "africa_countries",
            "column": "NAME_EN",
            "division_names": (),
        },
        "digital_elevation": "elevation_1KMmd_GMTEDmd",
        "shaded_relief": "MSR_50M",
        "satellite_landuse": "natural_earth_color.composite",
        "crop": {
            "harvest_area_fraction": "cassava_harvarea_binary",
            "tomato_temperate": "tomato_y_175crops_t_gaez_temperate",
            "tomato_tropical": "tomato_y_175crops_t_gaez_tropical",
            "tomato_combined": "tomato_y_175crops_t_gaez_combined",
        },
    },
    "legend_settings": {
        "room_for_bottom_legend": 0.37,
        "bottom_location": (6, 9, 15, 85),
        "right_location": (20, 80, 86, 90),
    },
    "region_settings": {
        "full": {
            "north": "n+25000",
            "south": "s-25000",
            "east": "e+25000",
            "west": "w-25000",
            "resolution": 3000,
        },
        "subset": {
            "north": "n+25000",
            "south": "s-25000",
            "east": "e+25000",
            "west": "w-25000",
            "resolution": 3000,
        },
    },
}

# From casas_gis_old/casas/grass_scripts/india
india = {
    "latlong_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "latlong",
        "mapset": "luigi",
    },
    "mapping_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "LAEA_India",
        "mapset": "luigi",
    },
    "mapping_data": {
        "coastline": {
            "map_name": "india_region_world_bounds",
            "color": "150:150:150",
            "width": 2,
        },
        "countries": {"map_name": "india_states", "color": "128:128:128", "width": 3},
        "lakes": {
            "map_name": "india_lakes",
            "color": "150:150:150",
            "fill_color": "215:240:255",
        },
        "admin_divisions": {
            "map_name": "india_states",
            "column": "POSTAL",
            "division_names": (),
        },
        "digital_elevation": "india_dem",
        "shaded_relief": "india_shaded_60_315_10",
        "satellite_landuse": "natural_earth_color.composite",
        "crop": {
            "cotton_full": "cotton_harea_175crops2000_india",
            "cotton_irrig": "cotton_area_irrig_fraction_M3",
            "cotton_rainfed": "cotton_area_rainf_fraction_M3",
        },
    },
    "legend_settings": {
        "room_for_bottom_legend": 0.37,
        "bottom_location": (6, 10, 20, 80),
        "right_location": (20, 80, 86, 90),
    },
    "region_settings": {
        "full": {
            "north": "n+50000",
            "south": "s-50000",
            "east": "e+50000",
            "west": "w-50000",
            "resolution": 3000,
        },
        "subset": {
            "north": "n+50000",
            "south": "s-50000",
            "east": "e+50000",
            "west": "w-50000",
            "resolution": 3000,
        },
    },
}

# From casas_gis_old/casas/grass_scripts/LibyaTunisia
libya_tunisia = {
    "latlong_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "latlong",
        "mapset": "libya",
    },
    "mapping_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "AEA_Med",
        "mapset": "libya",
    },
    "mapping_data": {
        "countries": {
            "map_name": "libya_tunisia_boundaries",
            "color": "128:128:128",
            "width": 2,
        },
        "digital_elevation": "libya_tunisia_dem",
        "shaded_relief": "libya_tunisia_shaded_relief",
    },
    "legend_settings": {
        "room_for_bottom_legend": 0.37,
        "bottom_location": (6, 11, 20, 80),
        "right_location": (20, 80, 86, 90),
    },
    "region_settings": {
        "full": {
            "north": -3000,
            "south": -2040000,
            "east": 1116000,
            "west": -726000,
            "resolution": 3000,
        },
        "subset": {
            "north": -3000,
            "south": -2040000,
            "east": 1116000,
            "west": -726000,
            "resolution": 3000,
        },
    },
}

# From casas_gis_old/casas/grass_scripts/EurMedGrape
europe_grape = {
    "latlong_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "latlong",
        "mapset": "luigi",
    },
    "mapping_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "AEA_Med",
        "mapset": "luigi",
    },
    "mapping_data": {
        "countries": {
            "map_name": "admin0_10m_naturalEarth_MED",
            "color": "128:128:128",
            "width": 3,
        },
        "target_region": {
            "map_name": "region_EurMedGrape",
            "color": "23:23:23",
            "width": 10,
        },
        "admin_divisions": {
            "map_name": "admin0_10m_naturalEarth_MED",
            "column": "COUNTRY",
            "division_names": (),
        },
        "digital_elevation": "Med_dem",
        "shaded_relief": "MSR_50M_land",
        "satellite_landuse": "natural_earth_color.composite",
        "crop": {
            "harvest_area_fraction": "grape_growing_area_raster_below1000",
            "tomato_temperate": "tomato_y_175crops_t_gaez_temperate",
            "tomato_tropical": "tomato_y_175crops_t_gaez_tropical",
            "tomato_combined": "tomato_y_175crops_t_gaez_combined",
            "alfalfa_harvested": "alfalfa_harvarea_EurMedGrape_binary",
        },
    },
    "legend_settings": {
        "room_for_bottom_legend": 0.37,
        "bottom_location": (6, 9, 15, 85),
        "right_location": (20, 80, 86, 90),
    },
    "region_settings": {
        "full": {
            "north": "n+50000",
            "south": "s-50000",
            "east": "e+50000",
            "west": "w-50000",
            "resolution": 3000,
        },
        "subset": {
            "north": "n+50000",
            "south": "s-50000",
            "east": "e+50000",
            "west": "w-50000",
            "resolution": 3000,
        },
    },
}

# From casas_gis_old/casas/grass_scripts/italia
italy = {
    "latlong_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "latlong",
        "mapset": "luigi",
    },
    "mapping_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "EurLCC",
        "mapset": "luigi",
    },
    "mapping_data": {
        "coastline": {"map_name": "CoastLines", "color": "150:150:150", "width": 2},
        "countries": {"map_name": "italia", "color": "128:128:128", "width": 3},
        "lakes": {"map_name": "laghi_clean", "color": "0:255:255"},
        "highlight": {"map_name": "trentino_alto_adige", "color": "white", "width": 20},
        "admin_divisions": {
            "map_name": "regioni_istat",
            "column": "COD_REG",
            "division_names": (),
        },
        "digital_elevation": "g10g",
        "shaded_relief": "60_310_4",
        "grey_shaded_relief": "30_310_30",
        "lakes_raster": "laghi",
        "satellite_landuse": None,
        "crop": None,
    },
    "legend_settings": {
        "room_for_bottom_legend": 0.37,
        "bottom_location": (6, 10, 20, 80),
        "right_location": (20, 80, 86, 90),
    },
    "region_settings": {
        "full": {
            "north": "n+20000",
            "south": "s-50000",
            "east": "e+20000",
            "west": "w-20000",
            "resolution": 1000,
        },
        "subset": {
            "north": "n+20000",
            "south": "s-50000",
            "east": "e+20000",
            "west": "w-20000",
            "resolution": 1000,
        },
    },
}

# Entire world, mapped in the Equal Earth projection (EPSG:8857).
# The mapping location must be created first, e.g.:
#     g.proj -c epsg=8857 location=equalearth_world
# Data to import (see the python dataset list), e.g.:
#     v.import -o input=ne_10m_coastline.shp output=ne_10m_coastline_world
#     v.import -o input=gadm36_0.shp output=ne_10m_admin_0_countries_lakes_world
#     v.import -o input=ne_10m_admin_1_states_provinces.shp \
#         output=ne_10m_admin_1_states_provinces_world
#     r.import -o input=gmted2010_me30.tif output=elevation_1KMmd_GMTEDmd_world
#     r.relief input=elevation_1KMmd_GMTEDmd_world output=SR_HR_world_250m
world = {
    "latlong_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "latlong",
        "mapset": "world",
    },
    "mapping_session": {
        "gisdb": f"{ini.gisdb}",
        "location": "equalearth_world",
        "mapset": "world",
    },
    "mapping_data": {
        "coastline": {
            "map_name": "ne_10m_coastline_world",
            "color": "150:150:150",
            "width": 2,
        },
        "countries": {
            "map_name": "ne_10m_admin_0_countries_lakes_world",
            "color": "128:128:128",
            "width": 2,
        },
        "target_region": {
            "map_name": "ne_10m_admin_0_countries_lakes_world",
            "color": "23:23:23",
            "width": 3,
        },
        "admin_divisions": {
            "map_name": "ne_10m_admin_1_states_provinces_world",
            "column": "iso_3166_2",
            "division_names": (),
        },
        "digital_elevation": "elevation_1KMmd_GMTEDmd_world",
        "shaded_relief": "SR_HR_world_250m",
        "grey_shaded_relief": "GRAY_HR_SR_OB_DR_world_250m",
        "satellite_landuse": "NE1_HR_LC_SR_W_DR.composite_world",
        "crop": None,
    },
    "legend_settings": {
        "room_for_bottom_legend": 0.37,
        "bottom_location": (6, 10, 20, 80),
        "right_location": (20, 80, 86, 90),
    },
    "region_settings": {
        "full": {
            "north": "n+10000",
            "south": "s-10000",
            "east": "e+10000",
            "west": "w-10000",
            "resolution": 1000,
        },
        "subset": {
            "north": "n+10000",
            "south": "s-10000",
            "east": "e+10000",
            "west": "w-10000",
            "resolution": 10000,
        },
    },
}

# Keep all available regions together for easy lookup
regions = {
    "andalusia": andalusia,
    "colombia": colombia,
    "mediterranean": mediterranean,
    "usa": usa,
    "africa": africa,
    "india": india,
    "libya_tunisia": libya_tunisia,
    "europe_grape": europe_grape,
    "italy": italy,
    "world": world,
}
