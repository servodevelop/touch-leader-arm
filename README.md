# Star Arm 102 → Lumos Python 遥操作

使用 Star Arm 102 主臂实时控制 Lumos 单臂

程序通过 Star Arm UART 和 Lumos CAN 通信，不依赖 LeRobot。客户操作步骤见 [操作指南](docs/StarArm102_Lumos_Python_Teleoperation_Guide.docx)。

## 硬件与环境

- Ubuntu 20.04 / 22.04 / 24.04 主机
- Python 3.10（推荐版本）
- Star Arm 102 主臂及 UART/USB 连接
- Lumos 单臂及已配置为 1 Mbps 的 CAN 接口（默认 `can0`）
- `git` 和 `sudo` 权限，以及可访问 GitHub 和 PyPI 的网络

## 安装

先准备并激活 Python 3.10 环境。若使用 Conda：

```bash
conda create -n stararm102-lumos python=3.10 -y
conda activate stararm102-lumos
```

下载本项目并运行一键安装脚本：

```bash
git clone https://github.com/VincentHSS/stararm102-lumos-teleop.git
cd stararm102-lumos-teleop
bash scripts/install_ubuntu.sh
```

脚本会安装 Lumos SDK 所需的系统构建依赖、StarArm Python 包和 Lumos Python 依赖；然后自动从 Lumos 官方仓库下载 StarTouch SDK 到项目目录 `.dependencies/startouch_sdk` 并完成安装。客户不必手动打开 Lumos 安装文档或进入 SDK 源码目录。脚本使用当前激活的 Python 环境；首次运行需要联网及 `sudo` 权限。

### 手动安装（用于排错）

在项目根目录、已激活的 Python 3.10 环境中依次执行。以下命令和一键脚本执行相同的依赖安装：

```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake pkg-config libeigen3-dev libyaml-cpp-dev liborocos-kdl-dev libtinyxml2-dev pybind11-dev

python -m pip install --upgrade pip setuptools wheel
python -m pip install pyserial fashionstar-uart-sdk

mkdir -p .dependencies
if [ ! -d .dependencies/startouch_sdk ]; then
  git clone --depth 1 https://github.com/lumos-open/startouch_sdk.git .dependencies/startouch_sdk
fi
python -m pip install -r .dependencies/startouch_sdk/requirements.txt
python -m pip install .dependencies/startouch_sdk
```

安装完成后验证接口：

```bash
python -c "import serial, fashionstar_uart_sdk; from startouchclass import SingleArm; print('SDK OK')"
```

> 安装脚本会自动从 [Lumos 官方 StarTouch SDK 仓库](https://github.com/lumos-open/startouch_sdk) 获取并安装 SDK。

## CAN 接口

检查接口：

```bash
ip -details link show can0
```

如果接口尚未启用，再配置为 1 Mbps：

```bash
sudo ip link set can0 up type can bitrate 1000000
```

若提示 `Device or resource busy`，先再次查看接口状态；如果 `can0` 已经是 `UP`，不需要重复设置。串口名称不确定时运行 `ls -l /dev/ttyUSB*`，并在后续命令中替换默认的 `/dev/ttyUSB0`。

## 首次校准

确认急停可用、工作区域畅通，并让两台机械臂处于安全且相互对应的参考姿态。校准会连接 Lumos SDK（SDK 连接会使能电机），采集 StarArm 关节范围并保存参考位置；不会下发运动目标。

```bash
python stararm102_lumos_teleop.py --calibrate --can can0 --leader-port /dev/ttyUSB0 --gripper
```

校准文件默认保存在 `~/.config/stararm102_lumos/calibration.json`。若不使用夹爪，从校准和后续命令中一并删除 `--gripper`。

### SDK 配置文件找不到

Lumos SDK 初始化需要源码目录内的 `src/config/robot_kinematics.yaml`。安装后请保留 `.dependencies/startouch_sdk` 目录；脚本会自动定位这份配置，并在 SDK 目录中完成初始化，再恢复启动目录。不要把 YAML 单独复制到项目根目录或 `site-packages`。

SDK 位于其他位置时，在运行命令中指定源码根目录：

```bash
python stararm102_lumos_teleop.py --calibrate --can can0 --leader-port /dev/ttyUSB0 --gripper --sdk-root /实际路径/startouch_sdk
```

若仍使用旧脚本，可以先从 SDK 目录启动，脚本路径填写为绝对路径：

```bash
PROJECT_DIR="$PWD"
test -f "$PROJECT_DIR/.dependencies/startouch_sdk/src/config/robot_kinematics.yaml"
cd "$PROJECT_DIR/.dependencies/startouch_sdk"
python "$PROJECT_DIR/stararm102_lumos_teleop.py" --calibrate --can can0 --leader-port /dev/ttyUSB0 --gripper
```

## 先预览，再执行

不带 `--execute` 时程序只显示输入，不向 Lumos 下发运动目标；默认开启的 HD 按钮仍会控制 StarArm 主臂悬停/释放：

```bash
python stararm102_lumos_teleop.py --can can0 --leader-port /dev/ttyUSB0 --gripper
```

确认关节映射和方向正确后才运行执行模式：

```bash
python stararm102_lumos_teleop.py --can can0 --leader-port /dev/ttyUSB0 --gripper --execute
```

如果串口不是 `/dev/ttyUSB0`，替换为实际设备名。夹爪方向相反时，在预览和执行命令中都增加 `--invert-gripper`。使用 `Ctrl+C` 正常停止；发生卡滞、碰撞或持续力矩报警时，立即停止并使用硬件急停。

## HD 按钮悬停

HD 实体按钮功能默认开启，按钮板 ID 默认是 `7`。按钮反馈为 `180°` 时锁定主臂六个关节，其他状态释放，夹爪不参与锁定。程序在按钮状态变化时发送锁定/释放指令，并显示 `HD=悬停` 或 `HD=释放`。校准采集和遥操作循环均会读取按钮。

按钮功能在预览模式也生效；`--execute` 仅控制是否向 Lumos 下发跟随目标。按钮板未响应时程序会报错退出。

如果使用无 HD 按钮的主臂，在校准、预览和执行命令中都增加 `--button-disable`：

```bash
python stararm102_lumos_teleop.py --can can0 --leader-port /dev/ttyUSB0 --gripper --button-disable
```

按钮板使用其他 ID 时，增加 `--button-id ID`（允许范围 `7..253`）。也可在脚本顶部修改 `HD_BUTTON_ENABLED` 和 `HD_BUTTON_ID` 默认值；`--button-enable` 可显式开启按钮功能。

## 调整关节映射与速度

脚本顶部的常量控制对应关系和目标变化速度：

- `JOINT_SIGNS`：六个 Lumos 关节方向，`1` 同向、`-1` 反向。
- `FOLLOW_GAIN`：主臂相对参考姿态的角度变化映射比例，范围 `(0, 1]`。
- `MAX_SPEED_DEG_PER_SEC`：按实际采样间隔计算的跟随速度上限，默认 `50°/秒`。
- `MAX_TARGET_STEP_DEG`：单帧最大目标变化，默认 `2°`，防止长时间通信卡顿后出现大步追赶。
- `FILTER_MIN_CUTOFF_HZ` / `FILTER_BETA`：关节角度自适应滤波，慢速时抑制噪声，快速运动时减少滤波延迟。夹爪不参与此滤波。
- `CONTROL_RATE_HZ`：控制循环频率。
- `STATUS_RATE_HZ`：终端状态打印频率，默认 `5 Hz`。

修改后先使用预览模式确认，再谨慎执行。不要通过增大参数或修改 SDK 保护阈值来掩盖力矩报警。

## 延迟与抖动诊断

程序显示实际循环频率 `rate`、本轮主臂读取耗时 `read`、映射目标与已发送目标之间的最大关节差值 `target_gap`，以及读写工作超过设定周期的累计次数 `overruns`。`target_gap` 不代表从臂实际位置误差；`overruns` 不包含终端打印和日志写入耗时，实际采样间隔会包含这些开销。

记录诊断文件时，在原有命令中增加 `--diagnostics-file`，例如：

```bash
python stararm102_lumos_teleop.py --can can0 --leader-port /dev/ttyUSB0 --gripper --execute --diagnostics-file outputs/teleop-diagnostics.csv
```

CSV 包含采样间隔、主臂读取与目标下发耗时、目标差值、六个主臂角度和六个下发目标。每次运行会覆盖指定文件，请为不同测试使用不同文件名。读取耗时偏高时先检查串口、SDK 与设备反馈；频率正常但 `target_gap` 持续增大，表示输入运动超过了跟随限速。默认速度上限保持原有 `50 Hz × 1°` 的水平，不会自动提高。

改动已经过模拟验证，实际机械臂上的延迟与抖动改善需要现场复测。原有校准文件可继续使用。

## 仓库内容

```text
.
├── stararm102_lumos_teleop.py
├── scripts/
│   └── install_ubuntu.sh
├── README.md
└── docs/
    └── StarArm102_Lumos_Python_Teleoperation_Guide.docx
```
