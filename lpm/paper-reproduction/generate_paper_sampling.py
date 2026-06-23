"""Generate a standalone reproduction of the paper's UCM/LPM sampling plan."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from lpm_sampling import (
    build_lpm_equivalent_source_tasks,
    build_paper_deflector_supercell,
    build_ucm_and_lpm_samples,
    sampling_rows,
)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-step-deg", type=float, default=40.0)
    parser.add_argument("--neighbor-radius", type=int, default=2)
    parser.add_argument("--probe-distance-um", type=float, default=2.0)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    supercell = build_paper_deflector_supercell(args.phase_step_deg)
    samples = build_ucm_and_lpm_samples(supercell, args.neighbor_radius)
    tasks = build_lpm_equivalent_source_tasks(samples, args.probe_distance_um)

    rows = sampling_rows(samples)
    write_csv(args.output_dir / "paper_ucm_lpm_sampling_plan.csv", rows)
    (args.output_dir / "paper_lpm_equivalent_source_tasks.json").write_text(
        json.dumps(tasks, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    summary = {
        "source": "Hsu et al. 2017 Local phase method",
        "phase_step_deg": args.phase_step_deg,
        "supercell_elements": len(supercell),
        "neighbor_radius": args.neighbor_radius,
        "local_window_width": 2 * args.neighbor_radius + 1,
        "ucm_definition": "periodic window repeats the center element",
        "lpm_definition": "local window keeps non-identical neighbors from the supercell",
        "outputs": [
            "paper_ucm_lpm_sampling_plan.csv",
            "paper_lpm_equivalent_source_tasks.json",
        ],
    }
    (args.output_dir / "paper_sampling_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
