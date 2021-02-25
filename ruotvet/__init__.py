import sys
if sys.version_info < (3, 7):
    raise ImportError(f"Your Python version {'.'.join(map(str, sys.version_info[:3]))} is not supported by RuOtvet, "
                      "please install Python 3.7+")

from .clients import *

__version__ = "1.1.0"
