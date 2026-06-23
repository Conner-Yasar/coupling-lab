"""Export one CST 1D S-parameter result item to CSV."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

from cst_runtime import ensure_cst_python_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--treepath", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    ensure_cst_python_path()
    from cst.results import ProjectFile  # type: ignore

    project = ProjectFile(str(args.project.resolve()), allow_interactive=True)
    item = project.get_3d().get_result_item(args.treepath)
    rows = []
    for frequency, value in zip(item.get_xdata(), item.get_ydata()):
        rows.append(
            {
                "frequency_thz": frequency,
                "real": value.real,
                "imag": value.imag,
                "magnitude": abs(value),
                "phase_deg": math.degrees(math.atan2(value.imag, value.real)),
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"exported {len(rows)} rows: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
