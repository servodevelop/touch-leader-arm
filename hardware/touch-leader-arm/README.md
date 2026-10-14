# Touch Leader Arm Hardware

[← Hardware Resources](../README.md)　|　<sub>**English** / [简体中文](README.zh.md)</sub>

Hardware resource framework for the supplied V3.1 teleoperation leader arm assembly.

**Contents:**

- [📂 Resources](#resources)
- [📐 Assembly model](#assembly-model)
- [📋 Bill of materials](#bill-of-materials)
- [🛠️ Assembly and calibration](#assembly-and-calibration)
- [✅ Validation status](#validation-status)

<a id="resources"></a>

## Resources

| Directory | Contents | Status |
| --- | --- | --- |
| [step/assembly/](step/assembly/) | V3.1 assembly STEP | Available; CAD geometry unverified |
| [step/parts/](step/parts/) | Individual part STEP models | Pending |
| [printing/stl/](printing/stl/) | Printable part meshes | Pending |
| [printing/3mf/](printing/3mf/) | Individual and complete print projects | Pending |
| [drawings/](drawings/) | Dimensioned drawings, PDF / DWG | Pending |
| [robot-description/](robot-description/) | URDF, meshes, and visualization instructions | Framework only; model pending |

<a id="assembly-model"></a>

## Assembly model

[Download V3.1 assembly STEP](step/assembly/touch-leader-arm-v3.1-1013.stp).

The supplied file `遥操臂V3.1_1013.stp` is stored as `touch-leader-arm-v3.1-1013.stp` without changing its contents. Its STEP header identifies Creo Parametric as the exporter and records `2026-10-13T11:21:50` as the export timestamp. The revision label comes from the source filename.

Import the file into a STEP-capable CAD application to inspect the assembly. Individual part exports and printing settings have not yet been prepared.

<a id="bill-of-materials"></a>

## Bill of materials

Pending confirmation against the assembly and physical hardware. No purchase-ready BOM is available yet.

| No. | Part name | Model / specification | Quantity | Notes |
| --- | --- | --- | --- | --- |
| — | Pending | Pending | — | Confirm part identifiers and quantities before filling in this table |

<a id="assembly-and-calibration"></a>

## Assembly and calibration

Assembly sequence, fastener specifications, wiring, joint limits, and zero calibration instructions are pending.

The existing [Python teleoperation guide](../../python-sdk/README.md) targets Star Arm 102 → Lumos. Compatibility with this V3.1 assembly has not been validated.

<a id="validation-status"></a>

## Validation status

| Item | Status |
| --- | --- |
| Assembly file copy | Contents preserved; only the filename changed |
| CAD import, geometry, and interference checks | Not validated |
| Printability and physical assembly | Not validated |
| BOM and hardware specifications | Pending confirmation |
| URDF and simulation | Not available |
| Python teleoperation with V3.1 | Not validated |
