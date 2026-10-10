# Star Arm 102 HD 主臂与 FL 从臂 LeRobot 集成

本包包含 `stararm102_hd` 主臂遥操作接口和 `stararm102_fl` 从臂接口。

## 安装

在已安装 LeRobot 的 Python 3.10 或更高版本环境中，进入本目录执行：

```bash
pip install -e .
```

本目录与相邻的 `lerobot-teleoperator-stararm102` 使用相同的 Python 包名，请按所选教程使用对应插件，避免在同一环境混装两个版本。

## 校准

先校准主臂：

```bash
lerobot-calibrate \
  --teleop.type=stararm102_hd \
  --teleop.id=stararm102_hd \
  --teleop.port=/dev/ttyUSB0 \
  --teleop.baudrate=1000000
```

再校准从臂：

```bash
lerobot-calibrate \
  --robot.type=stararm102_fl \
  --robot.id=stararm102_fl \
  --robot.port=/dev/ttyUSB1 \
  --robot.baudrate=1000000
```

按终端提示摆放零位、移动关节并保存校准文件。后续运行使用相同的设备 ID；重新校准时再次执行对应命令。

## 遥操作与 HD 按钮

```bash
lerobot-teleoperate \
  --teleop.type=stararm102_hd \
  --teleop.id=stararm102_hd \
  --teleop.port=/dev/ttyUSB0 \
  --teleop.baudrate=1000000 \
  --teleop.button.enabled=true \
  --robot.type=stararm102_fl \
  --robot.id=stararm102_fl \
  --robot.port=/dev/ttyUSB1 \
  --robot.baudrate=1000000
```

按实际设备修改串口。无 HD 按钮或使用 LD 主臂时，把 `--teleop.button.enabled` 改为 `false`。

开启按钮功能时，默认读取 ID 为 `7` 的按钮板：角度接近 `0°` 表示释放，接近 `180°` 表示锁定。锁定时，如果 `freeze_action_on_lock=true`，锁定关节的输出保持为上一次释放状态的动作；释放后恢复跟随。具体触发阈值和不锁定的关节由配置决定。

## 调试示例

只读取按钮状态：

```bash
python examples/read_button_state.py --port=/dev/ttyUSB0 --button-id=7
```

读取主臂关节和锁定状态，并写入 `examples/leader.log`：

```bash
python examples/read_leader_state.py --port=/dev/ttyUSB0 --button-enabled
```

将主臂日志中的动作回放到从臂：

```bash
python examples/replay_leader_actions_to_follower.py \
  --port=/dev/ttyUSB1 \
  --input-log=examples/leader.log \
  --skip-locked \
  --interval=0.2
```

回放会驱动从臂，可用于检查通信、关节方向、范围与跟随情况。另有 `examples/check_follower_observation.py` 和 `examples/teleoperate_hd_to_fl_with_cameras.py`，参数可用 `--help` 查看。

## 配置项

主臂支持 `port`、`baudrate`、`joint_ids`、`joint_directions`、`joint_ranges`，以及 `button.enabled`、`button.id`、`button.trigger_threshold`、`button.freeze_action_on_lock`、`button.lock_on_connect` 和 `excluded_lock_joints`。

从臂支持 `port`、`baudrate`、`joint_ids`、`joint_directions` 和 `joint_ranges`，不包含按钮配置。

默认关节名称是 `shoulder_pan`、`shoulder_lift`、`elbow_flex`、`wrist_flex`、`wrist_yaw`、`wrist_roll` 和 `gripper`。配置中的关节范围仍用于结构限位；校准文件保存每台机械臂的零位和范围。没有有效校准文件时，设备可能提示校准；从臂实现也保留了使用配置范围的回退逻辑。

## 相机、采集与训练

先查看相机设备：

```bash
lerobot-find-cameras opencv
```

在遥操作命令中加入从臂相机配置，例如：

```text
--robot.cameras="{first_person: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}, third_person: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}}"
```

采集、训练和策略运行步骤见 [中文教程](../stararm102.md)。ACT 模型及运行参数见 [夹方块示例](../examples/act_pick/README.md)，权重下载和演示见 [预训练模型仓库](https://github.com/VincentHSS/star-arm-102-act-model)；该示例使用相邻插件的类型名称，执行时按对应指南配置环境。

## 其他从臂

reBot Arm 102 的遥操作配置：

```bash
lerobot-teleoperate \
  --robot.type=seeed_b601_dm_follower \
  --robot.port=/dev/ttyACM0 \
  --robot.id=follower1 \
  --robot.can_adapter=damiao \
  --robot.joint_directions='{"shoulder_pan":1,"shoulder_lift":1,"elbow_flex":1,"wrist_flex":1,"wrist_yaw":1,"wrist_roll":1,"gripper":10}' \
  --teleop.type=stararm102_hd \
  --teleop.port=/dev/ttyUSB0 \
  --teleop.id=stararm102_hd \
  --teleop.button.enabled=true
```

此命令需要相应从臂插件。LD 主臂使用 `--teleop.button.enabled=false`。
