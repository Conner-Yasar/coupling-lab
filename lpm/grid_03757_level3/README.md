# grid_03757 Level 3 FieldSource LPM Task

Objective: reproduce strict Level 3 FieldSource LPM for `grid_03757`, producing
Periodic and Non-Periodic center-cell radiation data and an amplitude comparison
plot using only `SZmax(2),Zmin(1)` as the final port channel.

All files generated for this task must stay under this directory.

## Source Context

- Original result directory:
  `E:/aris/meta/cst_coupling_model1/reports/formal1001_model1_large_clean_sampling_for_deep_learning_20260608/lpm_output/grid_03757`
- Base model:
  `E:/aris/模型1/模型1.cst`
- Final output directory:
  `E:/aris/grid_03757_level3_lpm_20260612`

## Required Method

Strict Level 3 FieldSource LPM:

1. Build/solve the full Periodic structure: `[C,C,C,C,C]`.
2. Build/solve the full Non-Periodic structure: `[L2,L1,C,R1,R2]`.
3. In each full structure, use a Field Source Monitor enclosing only center cell `C`.
4. Export center-cell equivalent source as `.fsm`.
5. Create a separate radiation project, import the `.fsm` as the only source.
6. Extract final data from `SZmax(2),Zmin(1)`.
7. Save CSV and plot.

Ohmic Sheet LPM may be used only for comparison/debugging, never as the final
Level 3 result.

## Directory Layout

- `scripts/` automation scripts and helper tools.
- `projects/` copied/generated CST projects.
- `fsm/` exported FieldSource `.fsm` files.
- `data/` CSV outputs.
- `figures/` generated plots.
- `logs/` CST logs and run summaries.
- `notes/` investigation notes and issue records.

