import pytest

from casas_gis import __version__
from casas_gis.grass import set_mapping_region, mapping_session, Session


def test_version():
    assert __version__ == '0.1.0'


@pytest.mark.parametrize(
    "selected_subregions, expected",
    [
        (
            "",
            "{'projection': '99', 'zone': '0', 'n': '8000', 's': '-8000', 'w': '-8000', 'e': '8000', 'nsres': '1000', 'ewres': '1000', 'rows': '16', 'cols': '16', 'cells': '256'}",
        ),
        (
            ("ES-CA,ES-H,ES-AL,ES-GR," "ES-MA,ES-SE,ES-CO,ES-J"),
            "{'projection': '99', 'zone': '0', 'n': '150000', 's': '-167000', 'w': '-252000', 'e': '284000', 'nsres': '1000', 'ewres': '1000', 'rows': '317', 'cols': '536', 'cells': '169912'}",
        ),
        (
            "ES-CA,ES-H,ES-AL",
            "{'projection': '99', 'zone': '0', 'n': '94000', 's': '-167000', 'w': '-252000', 'e': '284000', 'nsres': '1000', 'ewres': '1000', 'rows': '261', 'cols': '536', 'cells': '139896'}",
        ),
        (
            "ES-MA,ES-SE",
            "{'projection': '99', 'zone': '0', 'n': '90000', 's': '-135000', 'w': '-164000', 'e': '96000', 'nsres': '1000', 'ewres': '1000', 'rows': '225', 'cols': '260', 'cells': '58500'}",
        ),
    ],
)
def test_set_mapping_region(selected_subregions, expected, capfd):
    with Session(**mapping_session):
        set_mapping_region(
            map_of_subregions="andalusia_provinces",
            column_name="iso_3166_2",
            selected_subregions=selected_subregions,
        )
    actual = capfd.readouterr().out.strip()
    assert actual == expected
