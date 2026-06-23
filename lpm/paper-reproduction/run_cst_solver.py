"""Run the CST solver for one generated reproduction project."""

from __future__ import annotations

import argparse
from pathlib import Path

from cst_runtime import import_cst_interface


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    args = parser.parse_args()

    interface = import_cst_interface()
    design_environment = interface.DesignEnvironment.new()
    project = design_environment.open_project(str(args.project.resolve()))
    print(f"active_solver: {project.model3d.get_active_solver_name()}")
    project.model3d.run_solver()
    print(f"solver_info: {project.model3d.get_solver_run_info()}")
    project.save()
    project.close()
    design_environment.close()
    print(f"solved: {args.project.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
