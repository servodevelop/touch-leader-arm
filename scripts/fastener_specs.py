"""从 R1 简化 CAD 的圆柱面核查紧固件尺寸，不据此确认采购螺纹。"""

FASTENER_PRODUCTS = {35916, 36620, 99391, 101106}
REFERENCE = 'https://github.com/servodevelop/Star-Arm-102/blob/main/hardware/102-hd/README.zh.md#bill-of-materials'


def describe_fastener(product, shape):
    if product not in FASTENER_PRODUCTS:
        return None
    # 前三种沿 Z 轴，台阶件沿 Y 轴；测量头下长度而不是总包围长度。
    axis = 'Y' if product == 101106 else 'Z'
    import Part
    groups = {}
    for face in shape.Faces:
        surface = face.Surface
        if not isinstance(surface, Part.Cylinder):
            continue
        assert abs(abs(getattr(surface.Axis, axis.lower())) - 1) < 1e-6
        radius = round(surface.Radius, 6)
        lo = getattr(face.BoundBox, axis + 'Min')
        hi = getattr(face.BoundBox, axis + 'Max')
        previous = groups.get(radius, (lo, hi))
        groups[radius] = (min(previous[0], lo), max(previous[1], hi))
    expected = {1.0, 1.25, 2.5} if product == 101106 else {1.5, 2.75}
    assert set(groups) == expected, '圆柱尺寸变化，请重新审核规格'
    head_radius = max(groups)
    head_lo, head_hi = groups[head_radius]
    dimensions = {
        'head_diameter_mm': round(2 * head_radius, 4),
        'head_height_mm': round(head_hi - head_lo, 4),
    }
    if product == 101106:
        shoulder_lo, shoulder_hi = groups[1.25]
        tip_lo, tip_hi = groups[1.0]
        assert abs(shoulder_lo - head_hi) < 1e-4 and abs(tip_lo - shoulder_hi) < 1e-4
        dimensions.update({
            'shoulder_diameter_mm': 2.5,
            'shoulder_length_mm': round(shoulder_hi - head_hi, 4),
            'tip_diameter_mm': 2.0,
            'tip_length_mm': round(tip_hi - tip_lo, 4),
            'under_head_length_mm': round(tip_hi - head_hi, 4),
        })
        assert dimensions == dict(head_diameter_mm=5.0, head_height_mm=2.5,
                                  shoulder_diameter_mm=2.5, shoulder_length_mm=3.0,
                                  tip_diameter_mm=2.0, tip_length_mm=4.0,
                                  under_head_length_mm=7.0)
        name = '内六角台阶螺钉'
        specification = '台阶段 Ø2.5 × 3 mm；末段 Ø2 × 4 mm（螺纹待确认）'
        note = '源名称含 M3，但台阶段直径为 2.5 mm、末段为 2 mm；不能据名称确定 M3，也不能将末段直径直接认定为 M2 螺纹。'
    else:
        shank_lo, _ = groups[1.5]
        dimensions.update({'shank_diameter_mm': 3.0,
                           'under_head_length_mm': round(head_lo - shank_lo, 4)})
        assert dimensions == dict(head_diameter_mm=5.5, head_height_mm=2.0,
                                  shank_diameter_mm=3.0, under_head_length_mm=4.0)
        name = '内六角圆柱头螺钉'
        specification = 'M3 × 4（CAD 推定，螺纹待确认）'
        note = '按杆径 3 mm、头下长度 4 mm 推定；CAD 头高仅 2 mm，不据源名称确认 GB/T 70.1 标准符合性。'
    return {
        'name_zh': name,
        'specification_zh': specification,
        'dimensions_mm': dimensions,
        'measurement_basis_zh': '按圆柱面半径及轴向边界测量；含头总长不作为螺钉标称长度。',
        'assessment_zh': note,
        'confirmation_status_zh': 'CAD 尺寸已核查；螺纹、螺距、标准、材质、强度等级及表面处理待工程确认。',
        'format_reference': REFERENCE,
        'reference_scope_zh': '仅参考 102 的品名与规格表达方式，不继承其尺寸、数量和采购属性。',
    }
