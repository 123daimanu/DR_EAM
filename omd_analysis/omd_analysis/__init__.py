"""
omd_analysis
This package contains modules that can be used to analyze result of openmd simulations.
"""

# Add imports here
from .main import *
from .extractor import * 
# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
