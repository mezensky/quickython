"""quickython - A quick start Python project template."""

import importlib.metadata as _metadata

from quickython.example import Greeting, greet
from quickython.sample import samplefunction

try:
    __version__ = _metadata.version("quickython")
except _metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

__all__ = ["Greeting", "greet", "samplefunction"]
