# Touch Leader Arm

<sub>**English** / [简体中文](README.zh.md)</sub>

Hardware resources for Touch Leader Arm and Python teleoperation resources for Star Arm 102 → Lumos.

## Resources

| Task | Entry | Status |
| --- | --- | --- |
| Find hardware specifications and CAD resources | [Hardware](hardware/) | V3.1 assembly STEP available; other resources pending |
| Read assembly, calibration, and operation guides | [Documentation](docs/) | Teleoperation guide available in Chinese; other guides pending |
| Install dependencies and run teleoperation | [Python SDK](python-sdk/) | Existing Star Arm 102 → Lumos script and guide; Touch Leader Arm V3.1 compatibility unverified |

## Repository layout

```text
.
├── README.md
├── README.zh.md
├── hardware/
│   └── touch-leader-arm/
│       ├── step/
│       │   ├── assembly/
│       │   └── parts/
│       ├── printing/
│       │   ├── stl/
│       │   └── 3mf/
│       ├── drawings/
│       └── robot-description/
├── docs/
│   ├── README.md
│   ├── README.zh.md
│   └── StarArm102_Lumos_Python_Teleoperation_Guide.docx
├── python-sdk/
│   ├── stararm102_lumos_teleop.py
│   └── scripts/
└── scripts/
```

## Documentation checks

From the repository root:

```bash
python -m pip install -r scripts/requirements-docs.txt
python scripts/check_docs.py
python scripts/check_readme_sync.py
```

These checks cover local file links and bilingual README structure. Translation meaning, CAD geometry, and operation on hardware require separate validation.
