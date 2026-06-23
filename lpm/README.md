# LPM (Localized Port Method) 研究

超表面单元的局部端口法（FieldSource LPM）等效源提取与验证。

## 子项目

### `grid_03757_level3/`

严格 Level 3 FieldSource LPM 复现 — 对 `grid_03757` 模型的周期/非周期结构求解，
通过场源监视器提取中心单元等效源，对比辐射数据。

- 本地 CST 工程目录：`E:\aris\grid_03757_level3_lpm_20260612\`

### `paper-reproduction/`

论文复现实验 — 自动生成采样计划、构建 CST 工程、提取 S 参数。

## 技术栈

- CST Studio Suite (Python API + VBA macro)
- 场源监视器 (Field Source Monitor) 等效源方法
- S 参数分析 (`SZmax(2),Zmin(1)`)
