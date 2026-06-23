"""CST macro generation for reproducing the paper's UCM/LPM solve flow."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PaperElement:
    element_id: int
    length_nm: float
    target_phase_deg: float
    width_nm: float = 80.0


def q(value: str | float | int) -> str:
    return f'"{value}"'


def fmt(value: float) -> str:
    text = f"{value:.9f}".rstrip("0").rstrip(".")
    return text if text else "0"


def brick(
    name: str,
    component: str,
    material: str,
    xrange_nm: tuple[float, float],
    yrange_nm: tuple[float, float],
    zrange_nm: tuple[float, float],
) -> str:
    return "\n".join(
        [
            "With Brick",
            "    .Reset",
            f"    .Name {q(name)}",
            f"    .Component {q(component)}",
            f"    .Material {q(material)}",
            f"    .Xrange {q(fmt(xrange_nm[0]))}, {q(fmt(xrange_nm[1]))}",
            f"    .Yrange {q(fmt(yrange_nm[0]))}, {q(fmt(yrange_nm[1]))}",
            f"    .Zrange {q(fmt(zrange_nm[0]))}, {q(fmt(zrange_nm[1]))}",
            "    .Create",
            "End With",
        ]
    )


def common_project_setup() -> str:
    boundary_markers = "\n".join(
        [
            "' Boundary.Xmin \"unit cell\"",
            "' Boundary.Xmax \"unit cell\"",
            "' Boundary.Ymin \"unit cell\"",
            "' Boundary.Ymax \"unit cell\"",
        ]
    )
    return "\n".join(
        [
            "' Common optical reflector setup from the LPM paper",
            'Units.Geometry "nm"',
            'Units.Frequency "THz"',
            'Solver.FrequencyRange "350", "400"',
            'ChangeSolverType "HF Frequency Domain"',
            "With Background",
            "    .ResetBackground",
            '    .Type "Normal"',
            "End With",
            boundary_markers,
            "With Boundary",
            '    .Xmin "unit cell"',
            '    .Xmax "unit cell"',
            '    .Ymin "unit cell"',
            '    .Ymax "unit cell"',
            '    .Zmin "electric"',
            '    .Zmax "expanded open"',
            '    .Xsymmetry "none"',
            '    .Ysymmetry "none"',
            '    .Zsymmetry "none"',
            '    .ApplyInAllDirections "False"',
            "End With",
            "With Material",
            "    .Reset",
            '    .Name "TiO2_n2p52"',
            '    .Folder ""',
            '    .FrqType "all"',
            '    .Type "Normal"',
            '    .SetMaterialUnit "THz", "nm"',
            '    .Epsilon "6.3504"',
            '    .Mu "1.0"',
            '    .Create',
            "End With",
            "With Material",
            "    .Reset",
            '    .Name "SiO2_n1p45"',
            '    .Folder ""',
            '    .FrqType "all"',
            '    .Type "Normal"',
            '    .SetMaterialUnit "THz", "nm"',
            '    .Epsilon "2.1025"',
            '    .Mu "1.0"',
            '    .Create',
            "End With",
        ]
    )


def element_geometry(element: PaperElement, x_center_nm: float, component: str) -> str:
    half_period = 400.0
    spacer_height = 120.0
    resonator_height = 160.0
    ground_thickness = 40.0
    half_length = element.length_nm / 2.0
    half_width = element.width_nm / 2.0
    return "\n\n".join(
        [
            f'Component.New "{component}"',
            brick(
                "pec_ground",
                component,
                "PEC",
                (x_center_nm - half_period, x_center_nm + half_period),
                (-half_period, half_period),
                (-ground_thickness, 0.0),
            ),
            brick(
                "sio2_spacer",
                component,
                "SiO2_n1p45",
                (x_center_nm - half_period, x_center_nm + half_period),
                (-half_period, half_period),
                (0.0, spacer_height),
            ),
            brick(
                "tio2_resonator",
                component,
                "TiO2_n2p52",
                (x_center_nm - half_length, x_center_nm + half_length),
                (-half_width, half_width),
                (spacer_height, spacer_height + resonator_height),
            ),
        ]
    )


def plane_wave_y_polarized() -> str:
    return "\n".join(
        [
            "With PlaneWave",
            "    .Reset",
            '    .Normal "0", "0", "-1"',
            '    .EVector "0", "-1", "0"',
            '    .Polarization "Linear"',
            '    .ReferenceFrequency "375"',
            '    .PhaseDifference "0.0"',
            '    .CircularDirection "Left"',
            '    .AxialRatio "0.0"',
            '    .SetUserDecouplingPlane "False"',
            '    .Store',
            "End With",
            "' PlaneWave.ExcitationVector \"0\", \"-1\", \"0\"",
        ]
    )


def sparameter_monitor(name: str) -> str:
    return "\n".join(
        [
            f"' Monitor.Name {q(name)}",
            "With Monitor",
            "    .Reset",
            f"    .Name {q(name)}",
            '    .Domain "Frequency"',
            '    .FieldType "Powerflow"',
            '    .MonitorValue "375"',
            "    .Create",
            "End With",
        ]
    )


def floquet_port_setup() -> str:
    return "\n".join(
        [
            "' Port.StartPortNumber \"1\"",
            "With FloquetPort",
            "    .Reset",
            '    .SetDialogTheta "10"',
            '    .SetDialogPhi "0"',
            '    .SetPolarizationIndependentOfScanAnglePhi "0.0", "False"',
            '    .SetSortCode "+beta/pw"',
            '    .SetCustomizedListFlag "False"',
            '    .Port "Zmax"',
            '    .SetNumberOfModesConsidered "4"',
            '    .SetDistanceToReferencePlane "0.0"',
            '    .SetUseCircularPolarization "False"',
            "End With",
        ]
    )


def field_source_monitor(name: str) -> str:
    return "\n".join(
        [
            f"' FieldSourceMonitor.Name {q(name)}",
            "' TODO: replace this volume field monitor with CST's Fieldsource monitor command once the exact history API is confirmed.",
            "With Monitor",
            "    .Reset",
            f"    .Name {q(name)}",
            '    .Dimension "Volume"',
            '    .Domain "Frequency"',
            '    .FieldType "Efield"',
            '    .Frequency "375"',
            "    .Create",
            "End With",
        ]
    )


def build_ucm_macro(element: PaperElement) -> str:
    return "\n\n".join(
        [
            "' UCM periodic unit-cell phase solve",
            common_project_setup(),
            element_geometry(element, x_center_nm=0.0, component=f"ucm_element_{element.element_id}"),
            plane_wave_y_polarized(),
            floquet_port_setup(),
            sparameter_monitor(f"ucm_sparameter_phase_element_{element.element_id}"),
        ]
    )


def build_lpm_supercell_fieldsource_macro(
    elements: tuple[PaperElement, ...],
    center_element_id: int,
) -> str:
    if not elements:
        raise ValueError("elements must not be empty")
    period_nm = 800.0
    center = next((element for element in elements if element.element_id == center_element_id), None)
    if center is None:
        raise ValueError(f"center_element_id not found: {center_element_id}")

    geometry = []
    offset = -(len(elements) // 2)
    for index, element in enumerate(elements):
        x_center = (offset + index) * period_nm
        geometry.append(element_geometry(element, x_center_nm=x_center, component=f"lpm_element_{element.element_id}"))
    return "\n\n".join(
        [
            "' LPM supercell field solve",
            f"' center element for equivalent-source export: {center.element_id}",
            common_project_setup(),
            *geometry,
            plane_wave_y_polarized(),
            field_source_monitor(f"center_{center.element_id}_equivalent_source"),
        ]
    )


def build_lpm_radiation_probe_macro(center_element_id: int, probe_distance_nm: float) -> str:
    if probe_distance_nm <= 0:
        raise ValueError("probe_distance_nm must be positive")
    return "\n\n".join(
        [
            "' LPM equivalent-source radiation phase probe",
            common_project_setup(),
            'Boundary.Zmin "open"',
            'Boundary.Zmax "open"',
            "' FieldSource.Reset",
            f"' FieldSource.Name {q(f'center_{center_element_id}_equivalent_source')}",
            "With FieldSource",
            "    .Reset",
            f"    .Name {q(f'center_{center_element_id}_equivalent_source')}",
            '    .FileName "<exported-center-field-source.fsm>"',
            "    .Create",
            "End With",
            f"' Probe.Name {q(f'phase_probe_center_{center_element_id}')}",
            f"' Probe.Zrange {q(fmt(probe_distance_nm))}",
            "With Probe",
            "    .Reset",
            f"    .Name {q(f'phase_probe_center_{center_element_id}')}",
            '    .Field "Efield"',
            '    .Orientation "z"',
            f"    .Zrange {q(fmt(probe_distance_nm))}",
            "    .Create",
            "End With",
        ]
    )


def write_macro(path: Path, macro: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(macro, encoding="utf-8")
