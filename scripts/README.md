# Repository Maintenance Scripts

[← Home](../README.md)　|　<sub>**English** / [简体中文](README.zh.md)</sub>

## Documentation checks

Run from the repository root with Python 3.10 or newer:

```bash
python -m pip install -r scripts/requirements-docs.txt
python scripts/check_docs.py
python scripts/check_readme_sync.py
```

The checks cover local file/image links and bilingual README structure. Translation meaning needs manual review.

## Reproduce the CAD BOM and illustrations

The [hardware BOM](../hardware/touch-leader-arm/README.md#bill-of-materials) is derived from the checksum-pinned V3.1 assembly. `extract_step_bom.py` requires a Python environment with FreeCAD, Part, and Import. `render_bom.py` runs inside Blender. The generated assets were checked with FreeCAD 1.1.4 and Blender 5.2.2.

On macOS, with FreeCAD and Blender installed in `/Applications`, run from the repository root:

```bash
PYTHONPATH=/Applications/FreeCAD.app/Contents/Resources/lib \
  /Applications/FreeCAD.app/Contents/Resources/bin/python \
  scripts/extract_step_bom.py --mesh-dir /tmp/touch-r1-bom-meshes

/Applications/Blender.app/Contents/MacOS/Blender \
  --background --factory-startup --python scripts/render_bom.py -- \
  --mesh-dir /tmp/touch-r1-bom-meshes
```

The first command regenerates the 16 `step/parts/` exports and `bom.json`; the second regenerates 17 images (16 BOM items and the assembly). Temporary triangle meshes stay outside the repository. The assembly file is never rewritten. Repeated source PRODUCT references are counted as instances; servo internals stay inside their subassembly. Equal-looking components with different source PRODUCT identifiers are not automatically merged.

Exports are reimported to verify shape validity and solid counts, with bounding-box differences below 0.001 mm and volume differences within the larger of 0.001 mm³ or 0.01%. The source CAD tolerances and measured errors are retained in `bom.json`. These numerical checks are not manufacturing tolerances. Source component placements are removed for individual exports; internal subassembly placements remain intact.

If the assembly changes, review the source identifiers and BOM scope before updating the pinned SHA-256 and item mapping. The STEP reference parser is specific to this Creo export. The scripts do not rewrite the README tables: synchronize the English and Chinese tables with the regenerated data, then inspect every image and run the documentation checks.
