# Touch R1 Leader Arm Hardware

[← Hardware Resources](../README.md)　|　<sub>**English** / [简体中文](README.zh.md)</sub>

CAD resources and an assembly-derived bill of materials for the supplied V3.1 model.

**Contents:**

- [📂 Resources](#resources)
- [📐 Assembly model](#assembly-model)
- [📋 Bill of materials](#bill-of-materials)
- [🔎 Items requiring confirmation](#confirmation)
- [🛠️ Assembly and calibration](#assembly-and-calibration)
- [✅ Validation status](#validation-status)

<a id="resources"></a>

## Resources

| Directory / file | Contents | Status |
| --- | --- | --- |
| [step/assembly/](step/assembly/) | Original V3.1 assembly STEP | Source bytes preserved; CAD import checked |
| [step/parts/](step/parts/) | 16 individual part or subassembly STEP exports | Export and reimport checks passed |
| [bom.json](bom.json) | BOM quantities, source identifiers, instance placements, and geometry checks | Extracted from the source assembly tree |
| [printing/stl/](printing/stl/) | Printable part meshes | Pending |
| [printing/3mf/](printing/3mf/) | Individual and complete print projects | Pending |
| [drawings/](drawings/) | Dimensioned drawings, PDF / DWG | Pending |
| [robot-description/](robot-description/) | URDF, meshes, and visualization instructions | Framework only; model pending |

<a id="assembly-model"></a>

## Assembly model

[Download V3.1 assembly STEP](step/assembly/touch-leader-arm-v3.1-1013.stp).

<a href="images/touch-r1-assembly.png"><img src="images/touch-r1-assembly.png" alt="Touch R1 V3.1 CAD assembly" width="320"></a>

The supplied file `遥操臂V3.1_1013.stp` is stored as `touch-leader-arm-v3.1-1013.stp` without changing its contents. Its STEP header identifies Creo Parametric as the exporter and records `2026-10-13T11:21:50` as the export timestamp. The revision label comes from the source filename.

The individual STEP files preserve each component's local CAD coordinates; servo exports retain their internal geometry as a complete subassembly. They are reference CAD exports, with no manufacturing or printing process assigned.

<a id="bill-of-materials"></a>

## Bill of materials

The table lists **16 distinct source items and 21 top-level occurrences** in one supplied assembly. Quantities come from STEP assembly references, grouped by source PRODUCT identity. The two servo subassembly types each occur three times; their internal parts are included within those subassemblies and are not counted again as purchase items. Expanding all subassemblies yields **99 leaf occurrences / solids**, not 99 purchased units.

Resource identifiers in Model / specification link to the corresponding STEP; the identifiers match the STEP and image filenames without extensions. All images, including fasteners, are rendered from the source STEP geometry as **1024 × 1024 white-background illustrations**. Click an image to enlarge it. The uniform gray display material does not specify physical material, color, or finish; each image is independently scaled.

CAD envelopes below are **local-axis X × Y × Z bounding-box dimensions**, rounded to 0.01 mm. They describe the model extent and are not engineering dimensions, tolerances, thread sizes, or purchase specifications. This CAD-derived BOM requires engineering confirmation before procurement; components missing from the source model are not inferred.

| No. | Part name | Model / specification | Image | Description | Quantity |
| :---: | --- | --- | :---: | --- | :---: |
| 1 | Servo subassembly | [touch-r1-servo-rp8-u45h-m-c028](step/parts/touch-r1-servo-rp8-u45h-m-c028.step) | <a href="images/touch-r1-servo-rp8-u45h-m-c028.png"><img src="images/touch-r1-servo-rp8-u45h-m-c028.png" alt="touch-r1-servo-rp8-u45h-m-c028" width="90"></a> | Source: `RP8-U45H-M-C028_STEP_ASM`<br>CAD envelope: 40.10 × 45.80 × 20.21 mm.<br>Source labels this subassembly RP8-U45H-M-C028; horn and internal CAD parts included. Confirm the delivered configuration. | 3 |
| 2 | Servo subassembly (model unconfirmed) | [touch-r1-servo-25-50kg-0001](step/parts/touch-r1-servo-25-50kg-0001.step) | <a href="images/touch-r1-servo-25-50kg-0001.png"><img src="images/touch-r1-servo-25-50kg-0001.png" alt="touch-r1-servo-25-50kg-0001" width="90"></a> | Source: `_25-50KG-0001_ASM_ASM`<br>CAD envelope: 40.10 × 52.60 × 20.21 mm.<br>Source label is a generic assembly identifier, not a confirmed purchasing model; horn and internals included. | 3 |
| 3 | Joint 1 structure | [touch-r1-joint-1](step/parts/touch-r1-joint-1.step) | <a href="images/touch-r1-joint-1.png"><img src="images/touch-r1-joint-1.png" alt="touch-r1-joint-1" width="90"></a> | Source: `关节1_NEW`<br>CAD envelope: 120.03 × 56.00 × 120.02 mm.<br>Material and manufacturing process unconfirmed. | 1 |
| 4 | Joint 2 structure | [touch-r1-joint-2](step/parts/touch-r1-joint-2.step) | <a href="images/touch-r1-joint-2.png"><img src="images/touch-r1-joint-2.png" alt="touch-r1-joint-2" width="90"></a> | Source: `关节2_新`<br>CAD envelope: 69.27 × 27.42 × 46.15 mm.<br>Material and manufacturing process unconfirmed. | 1 |
| 5 | Joint 3 structure | [touch-r1-joint-3](step/parts/touch-r1-joint-3.step) | <a href="images/touch-r1-joint-3.png"><img src="images/touch-r1-joint-3.png" alt="touch-r1-joint-3" width="90"></a> | Source: `关节3`<br>CAD envelope: 170.96 × 30.31 × 61.65 mm.<br>Material and manufacturing process unconfirmed. | 1 |
| 6 | Joint 4 structure | [touch-r1-joint-4](step/parts/touch-r1-joint-4.step) | <a href="images/touch-r1-joint-4.png"><img src="images/touch-r1-joint-4.png" alt="touch-r1-joint-4" width="90"></a> | Source: `关节4`<br>CAD envelope: 167.35 × 70.38 × 63.65 mm.<br>Material and manufacturing process unconfirmed. | 1 |
| 7 | Joint 5 structure | [touch-r1-joint-5](step/parts/touch-r1-joint-5.step) | <a href="images/touch-r1-joint-5.png"><img src="images/touch-r1-joint-5.png" alt="touch-r1-joint-5" width="90"></a> | Source: `关节5_NEW`<br>CAD envelope: 69.52 × 53.85 × 83.00 mm.<br>Material and manufacturing process unconfirmed. | 1 |
| 8 | Joint 6 structure | [touch-r1-joint-6](step/parts/touch-r1-joint-6.step) | <a href="images/touch-r1-joint-6.png"><img src="images/touch-r1-joint-6.png" alt="touch-r1-joint-6" width="90"></a> | Source: `关节6_NEW`<br>CAD envelope: 46.20 × 25.75 × 51.70 mm.<br>Material and manufacturing process unconfirmed. | 1 |
| 9 | Joint 7 handle structure | [touch-r1-joint-7](step/parts/touch-r1-joint-7.step) | <a href="images/touch-r1-joint-7.png"><img src="images/touch-r1-joint-7.png" alt="touch-r1-joint-7" width="90"></a> | Source: `关节7`<br>CAD envelope: 65.25 × 135.66 × 51.22 mm.<br>Handle shape is present in the CAD; material and manufacturing process unconfirmed. | 1 |
| 10 | Spacer | [touch-r1-spacer](step/parts/touch-r1-spacer.step) | <a href="images/touch-r1-spacer.png"><img src="images/touch-r1-spacer.png" alt="touch-r1-spacer" width="90"></a> | Source: `垫片`<br>CAD envelope: 20.00 × 2.30 × 20.00 mm.<br>Perforated spacer; material and fit tolerances unconfirmed. | 1 |
| 11 | Bracket A000 (function unconfirmed) | [touch-r1-part-a000](step/parts/touch-r1-part-a000.step) | <a href="images/touch-r1-part-a000.png"><img src="images/touch-r1-part-a000.png" alt="touch-r1-part-a000" width="90"></a> | Source: `A000`<br>CAD envelope: 41.12 × 41.76 × 8.00 mm.<br>Retain the source identifier; function, material, and process unconfirmed. | 1 |
| 12 | Bracket B000 (function unconfirmed) | [touch-r1-part-b000](step/parts/touch-r1-part-b000.step) | <a href="images/touch-r1-part-b000.png"><img src="images/touch-r1-part-b000.png" alt="touch-r1-part-b000" width="90"></a> | Source: `B000`<br>CAD envelope: 10.00 × 22.11 × 13.51 mm.<br>Retain the source identifier; function, material, and process unconfirmed. | 1 |
| 13 | Socket-head fastener PRT0001 | [touch-r1-fastener-prt0001](step/parts/touch-r1-fastener-prt0001.step) | <a href="images/touch-r1-fastener-prt0001.png"><img src="images/touch-r1-fastener-prt0001.png" alt="touch-r1-fastener-prt0001" width="90"></a> | Source: `PRT0001`<br>CAD envelope: 5.50 × 5.50 × 6.00 mm.<br>Simplified fastener geometry; thread, length designation, grade, and finish unconfirmed. See the grouping note below. | 1 |
| 14 | Socket-head fastener PRT0002 | [touch-r1-fastener-prt0002](step/parts/touch-r1-fastener-prt0002.step) | <a href="images/touch-r1-fastener-prt0002.png"><img src="images/touch-r1-fastener-prt0002.png" alt="touch-r1-fastener-prt0002" width="90"></a> | Source: `PRT0002`<br>CAD envelope: 5.50 × 5.50 × 6.00 mm.<br>Simplified fastener geometry; thread, length designation, grade, and finish unconfirmed. See the grouping note below. | 1 |
| 15 | Socket-head fastener GB_T70_1-M3X400 | [touch-r1-fastener-gb-t70-1-m3x400](step/parts/touch-r1-fastener-gb-t70-1-m3x400.step) | <a href="images/touch-r1-fastener-gb-t70-1-m3x400.png"><img src="images/touch-r1-fastener-gb-t70-1-m3x400.png" alt="touch-r1-fastener-gb-t70-1-m3x400" width="90"></a> | Source: `GB_T70_1-M3X400`<br>CAD envelope: 5.50 × 5.50 × 6.00 mm.<br>Keep the source name literally; do not interpret its suffix as a confirmed screw length. See the grouping note below. | 1 |
| 16 | Stepped socket-head fastener | [touch-r1-fastener-m3x3x60001](step/parts/touch-r1-fastener-m3x3x60001.step) | <a href="images/touch-r1-fastener-m3x3x60001.png"><img src="images/touch-r1-fastener-m3x3x60001.png" alt="touch-r1-fastener-m3x3x60001" width="90"></a> | Source: `M3X3X60001`<br>CAD envelope: 5.00 × 9.50 × 5.00 mm.<br>Two occurrences share one source PRODUCT. Thread, stepped lengths, grade, and finish unconfirmed. | 2 |

<a id="confirmation"></a>

## Items requiring confirmation

- Confirm the exact purchasing model and delivery contents of `_25-50KG-0001_ASM_ASM`. The name alone does not establish torque, voltage, encoder, or shaft specifications. Verify the configuration of the RP8-U45H-M-C028-labeled assemblies as well.
- `PRT0001`, `PRT0002`, and `GB_T70_1-M3X400` are separate PRODUCT definitions with matching 5.50 × 5.50 × 6.00 mm CAD envelopes and near-equal volumes. They remain three BOM rows until thread, material, grade, and length specifications establish whether they are interchangeable.
- Confirm the functions of A000 and B000, and the materials, manufacturing processes, and tolerances of all structural parts. No PLA, print settings, or fabrication method is assumed.
- Confirm the complete physical fastener, wiring, control-board, power, and accessory requirements. This source tree contains five top-level fastener occurrences; that is not evidence that five fasteners are sufficient to build the arm. Source joint names 1–7 do not establish the arm's actuated degrees of freedom.

<a id="assembly-and-calibration"></a>

## Assembly and calibration

Assembly sequence, confirmed fastener specifications, wiring, joint limits, and zero calibration instructions are pending.

The existing [Python teleoperation guide](../../python-sdk/README.md) targets Star Arm 102 → Lumos. Compatibility with this V3.1 assembly has not been validated.

<a id="validation-status"></a>

## Validation status

| Item | Status |
| --- | --- |
| Source assembly | SHA-256 matches the supplied file; one root, 21 top-level occurrences |
| CAD import | 99 solids; FreeCAD shape validity check passed |
| 16 STEP exports | Reimported successfully; solid counts unchanged, maximum relative volume difference below 0.0011%, envelope differences below 0.001 mm |
| BOM quantities | Cross-checked between STEP references and imported objects; source mapping retained in bom.json |
| Part illustrations | Rendered from CAD meshes; neutral display material; independent image scales |
| Interference, fit, and physical assembly | Not validated |
| Purchase BOM completeness and hardware specifications | Pending engineering confirmation |
| Printability, URDF, and simulation | Not validated; print files and URDF not supplied |
| Python teleoperation with V3.1 | Not validated |

The geometry checks verify CAD import/export consistency, not manufacturing approval. See [generation instructions](../../scripts/README.md) to reproduce the exports and illustrations.
