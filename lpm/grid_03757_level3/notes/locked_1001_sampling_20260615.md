# Locked 1001-Point Sampling

Date: 2026-06-15

## Frequency Grid

The locked grid is:

- start: `6 GHz`
- stop: `24 GHz`
- points: `1001`
- step: `(24 - 6) / (1001 - 1) = 0.018 GHz`

Generated grid CSVs:

- `data/periodic_locked_1001_frequency_grid.csv`
- `data/nonperiodic_locked_1001_frequency_grid.csv`

## Macro Policy

The preferred final route is now the per-frequency runner:

`scripts/run_locked_single_frequency_sampling.py`

It creates one fresh CST project per frequency and writes only the exact target frequency row to the final CSV. CST may internally calculate nearby interpolation samples, but those samples are rejected from the final output.

The older one-project broadband macro is retained only as a preflight asset. CST 2025 rejects `SetResultDataSamplingMode "Equidistant"` for this solver property, so the final locked data must come from the per-frequency runner plus post-export exact-grid validation.

## Validation Policy

After solve/export, the locked-single workflow fails if:

- CST log contains `Normal materials assigned to 2D sheets will be ignored`;
- CST log contains `Mesh adaptation terminated because the maximum number of passes is reached`;
- CST log contains `At least one propagating Floquet mode is not considered`;
- the exact target frequency is absent from the result item;
- the combined CSV frequency column is not an ordered prefix of the 1001-point locked grid.

Additional standalone audit:

`python scripts/audit_locked_single_results.py --points 1001`

The current locked-single CSVs contain only the tested 6 GHz row for each case. They pass the prefix check but are not complete until all 1001 rows are present.

Current progress after the latest locked-single batch:

- periodic: 10/1001 rows, covering `6.000` through `6.162 GHz`;
- nonperiodic: 10/1001 rows, covering `6.000` through `6.162 GHz`;
- both combined CSVs have no duplicate rows, no extra frequencies, and remain exact ordered prefixes of the 1001-point grid;
- missing rows begin at `6.180 GHz`.

## Important Geometry Blocker

The nonperiodic geometry repair is implemented inside the locked-single runner:

- `np_L2:substrate1`
- `np_L2:substrate2`
- `np_R2:substrate1`
- `np_R2:substrate2`

CST previously treated these F4B substrates as non-PEC 2D sheets, so the runner deletes and rebuilds `np_L2` and `np_R2` before solving. The repaired substrates are finite 3D F4B bricks inset by `0.001 mm` from the x unit-cell boundary.

Validated pilot:

- nonperiodic 6 GHz solved in `77.985 s`; no 2D-sheet material warning; final CSV contains only `6.0 GHz`;
- periodic 6 GHz solved in `34.531 s`; final CSV contains only `6.0 GHz`.

Validated continuation:

- periodic `6.018/6.036/6.054 GHz`: `35.875/35.515/34.234 s`;
- nonperiodic `6.018/6.036/6.054 GHz`: `80.140/89.797/82.609 s`;
- periodic `6.072/6.090/6.108 GHz`: `35.859/34.907/34.672 s`;
- nonperiodic `6.072/6.090/6.108 GHz`: `77.172/80.047/78.797 s`;
- periodic `6.126/6.144/6.162 GHz`: `36.359/35.344/35.000 s`;
- nonperiodic `6.126/6.144/6.162 GHz`: `79.188/77.235/81.219 s`;
- the repaired nonperiodic logs still have the CST mesh warning `The length ratio between the shortest and the longest model edges is 1:26649.`;
- the repaired logs do not contain the previous `Normal materials assigned to 2D sheets will be ignored` warning.
