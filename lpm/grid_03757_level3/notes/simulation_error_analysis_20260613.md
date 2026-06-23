# Simulation Error Analysis

Date: 2026-06-13

Scope: audit the already-produced `periodic` and `nonperiodic` source-stage CST results before trying any new Level 3 rerun.

## Verdict

The existing source-stage results must be treated as invalid/preliminary. The reported nonperiodic runtime of `1973.656 s` is not evidence of a correct 41-point Level 3 sample. CST actually ran an interpolative broadband sweep, produced extra frequencies, warned that the sampling setup may be inaccurate, and the nonperiodic geometry contains F4B substrate objects that CST treated as non-PEC 2D sheets.

## Blocking Errors

1. Nonperiodic F4B substrate material is ignored on edge cells.

   Evidence from:

   `projects/nonperiodic/source_solve/model1/Result/Model.log`

   CST warning:

   `Normal materials assigned to 2D sheets will be ignored. This is the case for np_L2:substrate1, np_L2:substrate2, np_R2:substrate1, np_R2:substrate2.`

   Interpretation: the true-neighbor nonperiodic model is not preserving all F4B dielectric substrates as valid 3D dielectric material. L2/R2 substrate layers are partially or fully treated as sheet entities, so the electromagnetic environment is not the intended real five-cell structure.

2. Mesh adaptation did not converge for nonperiodic.

   Evidence from:

   `projects/nonperiodic/source_solve/model1/Result/Model.log`

   CST warning:

   `Mesh adaptation terminated because the maximum number of passes is reached.`

   Final adaptive S-parameter error at pass 8 was still `0.0238737`, above the requested `0.01` criterion.

3. The 41-point sweep was not a locked 41-point sweep.

   Evidence from:

   `projects/nonperiodic/source_solve/model1/Result/Model.log`

   CST warning:

   `The number interpolated samples (41) is lower than twice the number of calculated samples. With these settings, the broadband sweep's results may be inaccurate.`

   CST summary:

   `All broadband sweep convergence criteria have been satisfied after calculating 44 frequency samples`

   The exported CSV has 44 rows, not 41. Extra adaptive/intermediate frequencies include `8.025`, `8.475`, and `15.675` GHz.

4. Periodic has the same sampling-method error.

   Evidence from:

   `projects/periodic/source_solve/model1/Result/Model.log`

   CST also warns that 41 interpolated samples is too low and reports `calculating 44 frequency samples`. The periodic CSV also has 44 rows, including an extra `6.675` GHz point.

5. The current plot is therefore not a valid strict Level 3 result.

   The figure:

   `figures/level3_fieldsource_periodic_vs_nonperiodic_amplitude.png`

   is based on the source-stage `SZmax(2),Zmin(1)` CSVs, not the standalone imported-FieldSource radiation result, and those CSVs come from an interpolative sweep with the errors listed above.

## Root-Cause Hypotheses

1. `FDSolver.SetResultDataSamplingMode "Automatic"` leaves CST in interpolative broadband sweep mode. Even with multiple `.AddSampleInterval(..., "Single", ...)` lines, CST still inserts extra adaptive samples and exports a non-locked grid.

2. The nonperiodic source project likely contains degenerate or sheet-like substrate geometry for the outer cells L2/R2 after clone/translate/boolean operations. CST identifies those F4B objects as non-PEC sheets and ignores their normal material assignment.

3. The large edge-length ratio (`1:26649`) is probably tied to tiny sliver/degenerate geometry in the same outer-cell substrate/metal construction and contributes to the non-converged adaptive mesh.

## Required Fix Before Rerun

1. Repair the nonperiodic geometry before solving:

   - `np_L2:substrate1`
   - `np_L2:substrate2`
   - `np_R2:substrate1`
   - `np_R2:substrate2`

   These must be valid 3D F4B solids with finite thickness, not 2D sheet remnants.

2. Replace broadband/interpolative sweep with exact locked-frequency sampling:

   - run one frequency at a time, or
   - create a CST setup that provably exports exactly the requested frequency list and fails if extra/missing frequencies appear.

3. Add hard validation gates:

   - fail if any log contains `Normal materials assigned to 2D sheets will be ignored`;
   - fail if adaptive mesh reaches maximum passes before the requested criterion;
   - fail if exported S-parameter frequency grid differs from the requested grid;
   - fail if CST inserts extra broadband samples;
   - fail if `.fsm` frequency files are not one-to-one with requested monitor frequencies.

4. Only after the above pass should the independent imported-FieldSource radiation stage be retried.

