from __future__ import absolute_import, division, print_function
# builtins is either provided by Python 3 or by the "future" module for Python 2 (http://python-future.org/)
from builtins import range, map, filter, round, next, input, bytes, hex, oct, chr, int  # TODO: Import all other necessary builtins after testing
from functools import reduce

from distutils.core import setup
import py2exe

setup(
    windows=['knossos_cuber_gui.py'],
    options={"py2exe" : {"includes" : ["sip"]}}
)
