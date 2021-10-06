import pytest
from casas_gis import __version__
from casas_gis.grass import set_mapping_region


def test_version():
    assert __version__ == '0.1.0'


dict_region_none = {}

dict_region_all = {
   'projection': '99', 'zone': '0',
   'n': '150000', 's': '-167000', 'w': '-252000', 'e': '284000',
   'nsres': '1000', 'ewres': '1000',
   'rows': '317', 'cols': '536', 'cells': '169912'
   }

dict_region_three = {}

dict_region_two = {}


@pytest.mark.parametrize("selected_subregions, expected", [
    ("", dict_region_none),
    (("ES-CA,ES-H,ES-AL,ES-GR,"
      "ES-MA,ES-SE,ES-CO,ES-J"), dict_region_all),
    ("ES-CA,ES-H,ES-AL", dict_region_three),
    ("ES-MA,ES-SE", dict_region_two),
])
def test_set_mapping_region(selected_subregions, expected):
  set_mapping_region(map_of_subregions="andalusia_provinces",
                     column_name='iso_3166_2',
                     selected_subregions=selected_subregions)
  actual = expected
