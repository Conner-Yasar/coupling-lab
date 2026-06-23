# Source Inventory

## Selected Source Project Pair

Root:

`E:/aris/meta/cst_coupling_model1/cst_projects/formal1001_model1_large_clean_sampling_for_deep_learning_20260608/grid_03757_np_r02_model1_dl_large`

Periodic source project:

`E:/aris/meta/cst_coupling_model1/cst_projects/formal1001_model1_large_clean_sampling_for_deep_learning_20260608/grid_03757_np_r02_model1_dl_large/same_center_whole_plane/model1.cst`

Non-Periodic source project:

`E:/aris/meta/cst_coupling_model1/cst_projects/formal1001_model1_large_clean_sampling_for_deep_learning_20260608/grid_03757_np_r02_model1_dl_large/nonperiodic_five_cell/model1.cst`

## grid_03757 Parameters

Center cell:

- `C`: `Atheta=-15.5`, `Pphi=55.0`, `gap=125.0`

Periodic case:

- `L2/L1/C/R1/R2`: all use center cell parameters.

Non-Periodic case:

- `L2`: `Atheta=-1.0`, `Pphi=84.0`, `gap=96.0`
- `L1`: `Atheta=-22.5`, `Pphi=94.0`, `gap=86.0`
- `C`: `Atheta=-15.5`, `Pphi=55.0`, `gap=125.0`
- `R1`: `Atheta=-6.0`, `Pphi=82.0`, `gap=98.0`
- `R2`: `Atheta=-34.5`, `Pphi=64.0`, `gap=116.0`

## Existing Related Attempts

Existing directories in the source root include:

- `lpm_fieldsource`
- `lpm_fs_test`
- `lpm_fs_v2`
- `lpm_fs_minimal`
- `_lpm_fieldsource`

These are evidence that FieldSource monitor generation and `.fsm` export were
attempted previously. They must not be reused as final outputs unless verified
inside this task directory.

