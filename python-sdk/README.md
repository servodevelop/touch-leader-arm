# Star Arm 102 → Lumos Python Teleoperation

[← Home](../README.md)　|　<sub>**English** / [简体中文](README.zh.md)</sub>

Use a Star Arm 102 leader arm to control a Lumos single arm in real time. This directory contains the existing teleoperation script and dependency installer; hardware compatibility with Touch Leader Arm V3.1 remains unverified.

The program communicates through Star Arm UART and Lumos CAN without LeRobot. See the [operation guide (Chinese)](../docs/StarArm102_Lumos_Python_Teleoperation_Guide.docx) for customer instructions.

**Contents:**

- [⚙️ Hardware and environment](#requirements)
- [📦 Installation](#installation)
- [🔌 CAN interface](#can-interface)
- [🎯 Initial calibration](#calibration)
- [▶️ Preview, then execute](#teleoperation)
- [🔘 HD button hold](#hd-button)
- [🔧 Joint mapping and speed](#configuration)
- [📂 Directory contents](#directory-structure)

<a id="requirements"></a>

## Hardware and environment

- Ubuntu 20.04 / 22.04 / 24.04 host
- Python 3.10 (recommended)
- Star Arm 102 leader arm with a UART/USB connection
- Lumos single arm with a CAN interface configured for 1 Mbps (default: `can0`)
- `git`, `sudo` access, and network access to GitHub and PyPI

<a id="installation"></a>

## Installation

Prepare and activate a Python 3.10 environment first. With Conda:

```bash
conda create -n stararm102-lumos python=3.10 -y
conda activate stararm102-lumos
```

Clone this repository and run the installer:

```bash
git clone https://github.com/servodevelop/touch-leader-arm.git
cd touch-leader-arm/python-sdk
bash scripts/install_ubuntu.sh
```

The script installs system build dependencies for the Lumos SDK, StarArm Python packages, and Lumos Python dependencies. It then downloads the StarTouch SDK from the official Lumos repository into `python-sdk/.dependencies/startouch_sdk` and installs it. You do not need to open separate Lumos installation instructions or enter the SDK source directory. The script uses the active Python environment; the first run requires network access and `sudo` privileges.

### Manual installation for troubleshooting

Run these commands from `python-sdk/` with the Python 3.10 environment activated. They install the same dependencies as the installer:

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

Verify the interfaces after installation:

```bash
python -c "import serial, fashionstar_uart_sdk; from startouchclass import SingleArm; print('SDK OK')"
```

> The installer automatically downloads and installs the SDK from the [official Lumos StarTouch SDK repository](https://github.com/lumos-open/startouch_sdk).

<a id="can-interface"></a>

## CAN interface

Check the interface:

```bash
ip -details link show can0
```

If the interface is not yet enabled, configure it for 1 Mbps:

```bash
sudo ip link set can0 up type can bitrate 1000000
```

If `Device or resource busy` appears, check the interface status again; if `can0` is already `UP`, do not repeat the setup. If you are unsure of the serial port name, run `ls -l /dev/ttyUSB*` and replace the default `/dev/ttyUSB0` in subsequent commands.

<a id="calibration"></a>

## Initial calibration

Make sure the emergency stop is available, the workspace is clear, and both arms are in safe, corresponding reference poses. Calibration connects to the Lumos SDK (connecting enables the motors), collects StarArm joint ranges, and saves reference positions. It does not send motion targets.

```bash
python stararm102_lumos_teleop.py --calibrate --can can0 --leader-port /dev/ttyUSB0 --gripper
```

The calibration file defaults to `~/.config/stararm102_lumos/calibration.json`. If you do not use a gripper, remove `--gripper` from both calibration and subsequent commands.

<a id="teleoperation"></a>

## Preview, then execute

Without `--execute`, the program displays inputs without sending motion targets to Lumos. The HD button, enabled by default, still controls hold/release on the StarArm leader:

```bash
python stararm102_lumos_teleop.py --can can0 --leader-port /dev/ttyUSB0 --gripper
```

Only run execution mode after confirming the joint mapping and directions:

```bash
python stararm102_lumos_teleop.py --can can0 --leader-port /dev/ttyUSB0 --gripper --execute
```

Replace `/dev/ttyUSB0` with the actual serial port if different. If the gripper moves in the wrong direction, add `--invert-gripper` to both preview and execution commands. Stop normally with `Ctrl+C`; for a jam, collision, or persistent torque alarm, stop immediately and use the hardware emergency stop.

<a id="hd-button"></a>

## HD button hold

The HD physical button is enabled by default, with button board ID `7`. A button reading of `180°` locks the six leader joints; other states release them. The gripper is excluded. The program sends lock/release commands when the button state changes and displays `HD=悬停` (hold) or `HD=释放` (release). Both calibration sampling and the teleoperation loop read the button.

The button also operates in preview mode; `--execute` only controls whether follow targets are sent to Lumos. The program exits with an error if the button board does not respond.

For a leader without an HD button, add `--button-disable` to calibration, preview, and execution commands:

```bash
python stararm102_lumos_teleop.py --can can0 --leader-port /dev/ttyUSB0 --gripper --button-disable
```

For a different button board ID, add `--button-id ID` (allowed range: `7..253`). You can also change the `HD_BUTTON_ENABLED` and `HD_BUTTON_ID` defaults at the top of the script; `--button-enable` explicitly enables the button.

<a id="configuration"></a>

## Joint mapping and speed

Constants at the top of the script control joint mapping and target changes:

- `JOINT_SIGNS`: directions of the six Lumos joints; `1` follows the same direction and `-1` reverses it.
- `FOLLOW_GAIN`: scale applied to leader angle changes relative to the reference pose, in `(0, 1]`.
- `MAX_STEP_DEG`: maximum target angle change per control cycle.
- `CONTROL_RATE_HZ`: control loop frequency.

After changing these values, verify them in preview mode before cautiously executing. Do not mask torque alarms by increasing parameters or modifying SDK protection thresholds.

<a id="directory-structure"></a>

## Directory contents

```text
python-sdk/
├── stararm102_lumos_teleop.py
├── scripts/
│   └── install_ubuntu.sh
├── README.md
└── README.zh.md
```
