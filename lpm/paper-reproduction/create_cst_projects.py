"""Create CST projects for the standalone paper UCM/LPM reproduction."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from cst_runtime import import_cst_interface


def remove_existing_project(project_path: Path) -> None:
    project_path = project_path.resolve()
    allowed_root = (Path(__file__).resolve().parent / "outputs" / "cst_projects").resolve()
    if allowed_root not in project_path.parents:
        raise ValueError(f"Refusing to overwrite outside {allowed_root}: {project_path}")
    if project_path.exists():
        project_path.unlink()
    companion_dir = project_path.with_suffix("")
    if companion_dir.exists():
        shutil.rmtree(companion_dir)


def add_macro_to_new_project(project_path: Path, history_name: str, macro: str, overwrite: bool = False) -> None:
    interface = import_cst_interface()
    project_path.parent.mkdir(parents=True, exist_ok=True)
    if overwrite:
        remove_existing_project(project_path)
    design_environment = interface.DesignEnvironment.new()
    project = design_environment.new_mws()
    project.model3d.add_to_history(history_name, macro)
    project.save(str(project_path.resolve()))
    project.close()
    design_environment.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--macro", type=Path, required=True)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--history-name", default="paper reproduction macro")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    macro = args.macro.read_text(encoding="utf-8")
    add_macro_to_new_project(args.project, args.history_name, macro, args.overwrite)
    print(f"created: {args.project.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
