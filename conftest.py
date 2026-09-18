# AUTHOR(S):    Luca Delucchi, luca delucchi fmach it, Fondazione Edmund Mach
# AUTHOR(S):    big-pickle AI model
#
# Make the casas_gis/ directory available on sys.path so that the bare
# imports used inside the package (e.g., "import constants as k") work
# when test modules import the package normally.
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, "casas_gis"))
