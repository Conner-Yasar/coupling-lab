"""Runtime helpers for launching CST from this standalone reproduction."""

from __future__ import annotations

import sys
from pathlib import Path


CST_PYTHON_LIB = Path(r"D:\software\CST\AMD64\python_cst_libraries")


def ensure_cst_python_path() -> None:
    if str(CST_PYTHON_LIB) not in sys.path:
        sys.path.insert(0, str(CST_PYTHON_LIB))


def import_cst_interface():
    ensure_cst_python_path()
    import cst.interface as interface  # type: ignore

    return interface
