from __future__ import annotations

from unittest.mock import patch

from . import httpx, requests
from .__version__ import __version__
from .mockish import AsyncMock, Mock, patch_fastapi_dependencies

__all__ = [
    "__version__",
    "Mock",
    "AsyncMock",
    "patch",
    "patch_fastapi_dependencies",
    "requests",
    "httpx",
]
