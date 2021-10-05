import pytest
from casas_gis import __version__
from casas_gis.grass import set_mapping_region


def test_version():
    assert __version__ == '0.1.0'


