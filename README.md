# Touch R1 Leader Arm

<sub>**简体中文**</sub>

Touch R1 Leader Arm 硬件资源，以及 Star Arm 102 → Lumos 的 Python 遥操作资源。

文档以中文为主，英文按需补充。各目录的 `README.md` 为正文入口。

## 资源入口

| 任务 | 入口 | 状态 |
| --- | --- | --- |
| 查看硬件规格与 CAD 资料 | [硬件资源](hardware/) | 已提供 V3.1 装配体、16 份 STEP 导出件及图文 CAD BOM；采购规格待确认 |
| 查阅装配、校准与使用指南 | [文档中心](docs/) | 已有中文遥操作指南；其他指南待补 |
| 安装依赖并运行遥操作 | [Python SDK](python-sdk/) | 已有 Star Arm 102 → Lumos 脚本与指南；Touch R1 Leader Arm V3.1 兼容性尚未验证 |

## 仓库结构

```text
.
├── README.md
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
│   └── StarArm102_Lumos_Python_Teleoperation_Guide.docx
├── python-sdk/
│   ├── stararm102_lumos_teleop.py
│   └── scripts/
└── scripts/
```

## 文档检查

在仓库根目录执行：

```bash
python -m pip install -r scripts/requirements-docs.txt
python scripts/check_docs.py
python scripts/check_readme_sync.py
```

这些检查覆盖本地文件链接、中文 README 入口与旧链接兼容页。CAD 几何和硬件实际运行需要另外验证。

## 本版本与上一版本的区别

本节对比当前已合入 `main` 的新版与合并前已支持 HD 按钮的 Lumos Python 遥操作脚本。新版运行入口为 [`python-sdk/stararm102_lumos_teleop.py`](python-sdk/stararm102_lumos_teleop.py)，完整参数和运行步骤见 [Python SDK 使用说明](python-sdk/README.md)。

| 项目 | 上一版本 | 当前版本 | 对使用的影响 |
| --- | --- | --- | --- |
| 关节输入平滑 | 主臂角度直接用于目标计算，没有滤波。 | 加入自适应角度滤波，慢速时抑制噪声，快速时提高响应速度。 | 减少输入噪声传到从臂；滤波仍会引入一定滞后，实际改善需要实机复测。夹爪不参与此滤波。 |
| 跟随限速 | 用 `MAX_STEP_DEG=1.0` 限制每周期步长；循环变慢时，目标变化速度也随之下降。 | 用 `MAX_SPEED_DEG_PER_SEC=50.0` 按实际采样间隔限速，同时以 `MAX_TARGET_STEP_DEG=2.0` 限制单帧变化。 | 在正常频率波动时减少额外追赶延迟，长时间卡顿后不下发大步跳变。默认 50 Hz 时的速度上限保持不变；持续低频时仍受单帧上限限制。 |
| 终端输出 | 每个控制循环打印一次状态。 | 默认每秒最多打印 5 次，并显示实际频率、读取耗时、目标差值和超时次数。 | 降低打印开销，也更容易判断延迟来自通信耗时还是目标限速。 |
| 诊断日志 | 没有循环诊断 CSV。 | 新增 `--diagnostics-file`，逐帧记录耗时、主臂输入和输出目标。 | 可将现场数据用于排查延迟与抖动；不填写该参数时不保存日志。 |
| SDK 配置定位 | 直接从启动目录初始化 Lumos，部分 SDK 版本会找不到 `robot_kinematics.yaml`。 | 自动查找 SDK 源码目录，在该目录内完成初始化；新增 `--sdk-root` 指定位置。安装脚本也检查配置文件是否存在。 | 减少配置路径错误；仍须保留 SDK 源码目录及其 `src/config`，无需复制 YAML 到 Python 安装目录。 |
| 参数说明 | 主要提供基本运行步骤。 | 补充命令行参数、调速与滤波参数、诊断字段的中文说明。 | 可按用途选择参数，并了解调大、调小的影响。 |

原有校准文件、关节映射、关节方向和夹爪开合映射可继续使用；HD 按钮逻辑与默认开启设置保持不变。仍需 `--execute` 才会向 Lumos 下发跟随目标。

升级后进入 `python-sdk/` 目录运行 `stararm102_lumos_teleop.py`，原有命令可继续使用。SDK 无法自动定位时增加 `--sdk-root`；需要记录现场数据时增加 `--diagnostics-file`。旧版中的 `MAX_STEP_DEG` 已替换为速度上限与单帧步长上限，之前自行调整过该常量的用户需要在新版顶部重新核对设置。

本版本已通过模拟测试，尚不能据此保证实机延迟或抖动完全消失，也不会自动提高默认跟随速度。
