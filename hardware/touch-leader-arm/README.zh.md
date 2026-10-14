# Touch Leader Arm 硬件

[← 硬件资源](../README.zh.md)　|　<sub>[English](README.md) / **简体中文**</sub>

所提供的 V3.1 遥操作主臂装配体对应的硬件资源框架。

**目录：**

- [📂 资源目录](#resources)
- [📐 装配模型](#assembly-model)
- [📋 物料清单](#bill-of-materials)
- [🛠️ 装配与校准](#assembly-and-calibration)
- [✅ 验证状态](#validation-status)

<a id="resources"></a>

## 资源目录

| 目录 | 内容 | 状态 |
| --- | --- | --- |
| [step/assembly/](step/assembly/) | V3.1 装配体 STEP | 已提供；CAD 几何尚未验证 |
| [step/parts/](step/parts/) | 独立零件 STEP 模型 | 待补充 |
| [printing/stl/](printing/stl/) | 可打印的零件网格 | 待补充 |
| [printing/3mf/](printing/3mf/) | 独立零件与整套打印项目 | 待补充 |
| [drawings/](drawings/) | 带尺寸工程图纸，PDF／DWG | 待补充 |
| [robot-description/](robot-description/) | URDF、网格和可视化说明 | 仅有框架；模型待补充 |

<a id="assembly-model"></a>

## 装配模型

[下载 V3.1 装配体 STEP](step/assembly/touch-leader-arm-v3.1-1013.stp)。

所提供的文件 `遥操臂V3.1_1013.stp` 以 `touch-leader-arm-v3.1-1013.stp` 保存，内容未作修改。STEP 文件头记录的导出软件为 Creo Parametric，导出时间为 `2026-10-13T11:21:50`。版本标注来自源文件名。

可将文件导入支持 STEP 的 CAD 软件查看装配体。独立零件导出及打印参数尚未准备。

<a id="bill-of-materials"></a>

## 物料清单

待根据装配体和实物核对，目前尚无可用于采购的完整 BOM。

| 序号 | 品名 | 型号／规格 | 数量 | 备注 |
| --- | --- | --- | --- | --- |
| — | 待补充 | 待补充 | — | 填写前确认零件编号与数量 |

<a id="assembly-and-calibration"></a>

## 装配与校准

装配顺序、紧固件规格、接线、关节限位及零位校准说明待补充。

现有 [Python 遥操作指南](../../python-sdk/README.zh.md) 面向 Star Arm 102 → Lumos；与此 V3.1 装配体的兼容性尚未验证。

<a id="validation-status"></a>

## 验证状态

| 项目 | 状态 |
| --- | --- |
| 装配体文件复制 | 内容保持不变，仅修改文件名 |
| CAD 导入、几何及干涉检查 | 尚未验证 |
| 可打印性与实物装配 | 尚未验证 |
| 物料清单与硬件规格 | 待确认 |
| URDF 与仿真 | 尚未提供 |
| V3.1 的 Python 遥操作 | 尚未验证 |
