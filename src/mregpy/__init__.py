"""
## MRegPy
#### (M)eta (Reg)estries (Py)thon

`
import mregpy
`
"""

import importlib.metadata

if __package__:
    __version__ = importlib.metadata.version(__package__)
else:
    __version__ = "I think you broke something"