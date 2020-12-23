from tap_brightview import __version__
import pytest
from tap_brightview.carelogic_service import *

def test_version():
    assert __version__ == '0.1.0'
