"""Reproduce the UCM/LPM sampling structure from the local phase method paper.

This module does not run an EM solver. It builds the deterministic sample
descriptors needed by the paper workflow:

- UCM: one meta-atom analyzed with identical periodic neighbors.
- LPM: one center meta-atom analyzed inside a local non-identical-neighbor
  supercell, then exported as an equivalent-source task.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MetaAtom:
    element_id: int
    target_phase_deg: float


@dataclass(frozen=True)
class SamplingPair:
    center: MetaAtom
    ucm_periodic_window: tuple[MetaAtom, ...]
    lpm_local_window: tuple[MetaAtom, ...]

    @property
    def has_non_identical_neighbors(self) -> bool:
        return any(cell.element_id != self.center.element_id for cell in self.lpm_local_window)


def build_paper_deflector_supercell(phase_step_deg: float = 40.0) -> tuple[MetaAtom, ...]:
    """Build the paper's 9-element phase ramp.

    The paper uses a constant adjacent phase difference of 40 degrees, which
    gives 360 / 40 = 9 elements in the deflector supercell.
    """

    if phase_step_deg <= 0:
        raise ValueError("phase_step_deg must be positive")
    count = round(360.0 / phase_step_deg)
    if abs(count * phase_step_deg - 360.0) > 1e-9:
        raise ValueError("phase_step_deg must divide 360 degrees")
    return tuple(MetaAtom(element_id=index, target_phase_deg=index * phase_step_deg) for index in range(count))


def build_ucm_and_lpm_samples(
    supercell: tuple[MetaAtom, ...],
    neighbor_radius: int = 2,
) -> tuple[SamplingPair, ...]:
    """Build paired UCM and LPM windows for every center in a supercell."""

    if not supercell:
        raise ValueError("supercell must contain at least one meta-atom")
    if neighbor_radius < 0:
        raise ValueError("neighbor_radius must be non-negative")

    width = 2 * neighbor_radius + 1
    samples = []
    for center_index, center in enumerate(supercell):
        ucm = tuple(center for _ in range(width))
        lpm = tuple(
            supercell[(center_index + offset) % len(supercell)]
            for offset in range(-neighbor_radius, neighbor_radius + 1)
        )
        samples.append(SamplingPair(center=center, ucm_periodic_window=ucm, lpm_local_window=lpm))
    return tuple(samples)


def build_lpm_equivalent_source_tasks(
    samples: tuple[SamplingPair, ...],
    probe_distance_um: float,
) -> list[dict[str, object]]:
    """Describe the LPM equivalent-source phase-measurement tasks."""

    if probe_distance_um <= 0:
        raise ValueError("probe_distance_um must be positive")

    tasks: list[dict[str, object]] = []
    for sample in samples:
        tasks.append(
            {
                "method": "LPM",
                "center_element_id": sample.center.element_id,
                "target_phase_deg": sample.center.target_phase_deg,
                "ucm_periodic_element_ids": [cell.element_id for cell in sample.ucm_periodic_window],
                "local_window_element_ids": [cell.element_id for cell in sample.lpm_local_window],
                "equivalent_sources": ["Js = n x H", "Ms = -n x E"],
                "probe_distance_um": probe_distance_um,
                "phase_measurement": "export center closed-surface field source, then record probe phase",
            }
        )
    return tasks


def sampling_rows(samples: tuple[SamplingPair, ...]) -> list[dict[str, object]]:
    """Flatten paired UCM/LPM samples into table rows."""

    rows: list[dict[str, object]] = []
    for sample in samples:
        rows.append(
            {
                "center_element_id": sample.center.element_id,
                "target_phase_deg": sample.center.target_phase_deg,
                "ucm_periodic_element_ids": "|".join(str(cell.element_id) for cell in sample.ucm_periodic_window),
                "ucm_periodic_target_phases_deg": "|".join(
                    f"{cell.target_phase_deg:g}" for cell in sample.ucm_periodic_window
                ),
                "lpm_local_window_element_ids": "|".join(str(cell.element_id) for cell in sample.lpm_local_window),
                "lpm_local_window_target_phases_deg": "|".join(
                    f"{cell.target_phase_deg:g}" for cell in sample.lpm_local_window
                ),
                "has_non_identical_neighbors": "yes" if sample.has_non_identical_neighbors else "no",
            }
        )
    return rows
