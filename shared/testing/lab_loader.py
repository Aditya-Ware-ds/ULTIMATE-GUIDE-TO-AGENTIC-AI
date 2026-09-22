"""Shared helper every lab's test suite uses to load either the learner's
`starter/` code or the reference `solution/`, selected by the `LAB_TARGET`
env var (default "solution").

This is what makes `make test` verify every solution automatically while the
same test file also works against a learner's in-progress starter code:

    uv run pytest path/to/labs/NN-lab-name/tests                # tests solution/
    LAB_TARGET=starter uv run pytest path/to/labs/NN-lab-name/tests  # tests your code
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from types import ModuleType

VALID_TARGETS = frozenset({"starter", "solution"})


def load_lab_module(lab_dir: Path, module_name: str, *, filename: str | None = None) -> ModuleType:
    target = os.environ.get("LAB_TARGET", "solution")
    if target not in VALID_TARGETS:
        raise ValueError(f"LAB_TARGET must be one of {sorted(VALID_TARGETS)}, got {target!r}")
    module_path = lab_dir / target / (filename or f"{module_name}.py")
    if not module_path.exists():
        raise FileNotFoundError(
            f"{module_path} does not exist. Did you create {module_path.name} in {target}/?"
        )
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load a module spec for {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
