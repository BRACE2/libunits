import sys
# try using a faster library
try: import orjson as json
except ImportError: import json

from . import units


definitions = {'a': 1, 'b': 2, 'c': 123.4}

this_module = sys.modules[__name__]

defs = units.load("english")

for name, value in defs.items():
    setattr(this_module, name, units.Dimension(value))


