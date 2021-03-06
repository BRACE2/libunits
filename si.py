import sys
# try using a faster library
try: import orjson as json
except ImportError: import json

from . import units

this_module = sys.modules[__name__]

defs = units.load("si")

for name, value in defs.items():
    setattr(this_module, name, units.Dimension(value))


