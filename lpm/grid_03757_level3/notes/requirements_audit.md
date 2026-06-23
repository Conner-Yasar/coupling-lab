# Requirements Audit

Status meanings:

- Missing: no evidence yet.
- In progress: script or project exists, but no verified output yet.
- Verified: authoritative current-state evidence exists.

| Requirement | Status | Evidence |
|---|---:|---|
| All task files under `E:/aris/grid_03757_level3_lpm_20260612` | Verified | Directory initialized; generated scripts, projects, `.fsm`, data, figures, logs, and notes are under this task folder |
| Periodic `[C,C,C,C,C]` strict Level 3 source solve | Invalid / needs rerun | CST actually calculated 44 broadband samples, not a locked 41-point grid; see `logs/source_results_error_audit_20260613.json` |
| Non-Periodic `[L2,L1,C,R1,R2]` strict Level 3 source solve | Repair implemented; full rerun pending | `scripts/run_locked_single_frequency_sampling.py` rebuilds `np_L2`/`np_R2` with 3D F4B substrates inset from x boundary. Locked-single rows `6.000` through `6.162 GHz` solved without the 2D-sheet material warning; full 1001-point rerun still pending |
| Center-cell FieldSource Monitor extracts only `C` | Verified setup | Setup macros use center subvolume `x=-3..3`, `y=-6..6`, `z=-3..5.5`; CST logs confirm FieldSource monitor files written |
| `.fsm` exported for Periodic and Non-Periodic | Verified | 41 periodic `.fsm` and 41 nonperiodic `.fsm` copied under `fsm/periodic` and `fsm/nonperiodic` |
| Independent FieldSource radiation projects created | Blocked / failing | TD standalone `periodic_xy` and `expanded_open` each exceeded 15 min for one `.fsm`; FD standalone exceeded 20 min and FD `setup-only` exceeded 5 min without producing `Result\Model.log`; no verified probe CSV yet |
| Final channel uses only `SZmax(2),Zmin(1)` | Verified for source-solve CSV | CSV export uses `1D Results\S-Parameters\SZmax(2),Zmin(1)`; independent radiation step still missing |
| 6-24 GHz data saved to CSV | Locked-single partial | `data_locked_single/periodic_locked_single_combined.csv` and `data_locked_single/nonperiodic_locked_single_combined.csv` currently contain 10/1001 exact locked-grid rows for each case (`6.000` through `6.162 GHz`); audit reports ordered prefixes with no extras or duplicates |
| Amplitude plot generated | Invalid / diagnostic only | `figures/level3_fieldsource_periodic_vs_nonperiodic_amplitude.png`; based on invalid source-stage port CSV, not final standalone radiation |
| Per-simulation runtime <= 40 min | Verified for first 10 locked rows only | Periodic locked-single first 10 rows: about 34-37 s each. Nonperiodic locked-single first 10 rows with repaired L2/R2 substrates: about 77-90 s each. Full 1001-point sweep has not been run. |
| CST logs checked after each solve | Verified with caveat | Latest locked-single logs contain no 2D-sheet material warning, no adaptive max-pass failure, no missing Floquet-mode warning, and no solver aborted/stopped message. Nonperiodic logs still contain the mesh edge-length-ratio warning `1:26649`, which remains under monitoring. |
