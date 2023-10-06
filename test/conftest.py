import sys
from pathlib import Path
from typing import Any

import pytest


def pytest_ignore_collect(
    collection_path: Path, path: Any, config: pytest.Config
) -> bool:
    # Don't include the pytest-mypy-plugins yaml tests for 3.8 (unless they're
    # explicitly passed when running pytest), because mypy's message formatting
    # in 3.8 is too different to 3.9+ to retain sanity while making the tests's
    # assertion messages match.
    if sys.version_info < (3, 9) and collection_path.match("*.yml"):
        return True
    return False
