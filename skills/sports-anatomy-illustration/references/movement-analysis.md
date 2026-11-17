# 动作分析与分期图

适用于动作分解图、训练动作肌肉分工图、步态或跳跃周期图、漫画中的动作教学页。总规则见[运动解剖绘图规则](sports-anatomy.md)。

## 流程

1. **确定问题：**读者要看懂什么，例如“深蹲起立时哪些肌肉发力”“跑步哪一刻腘绳肌负荷最大”。一幅图回答一个主问题。
2. **选择模板：**随包 [`data/movements.json`](../data/movements.json) 提供深蹲、硬拉、俯卧撑、跑步步态、反向纵跳的定性分期。它只是起点，须按项目来源核对，不能直接作为证据。其他动作按下方字段新建。
3. **分期：**用可观察事件划分分期，常见为准备、离心/负荷、转换、向心/推进、恢复。分期数量服务表达，示意图一般 2–4 期。
4. **写 movement spec：**新项目可运行 `python3 scripts/init_project.py <项目目录> --sports`，在 `02_动作分析/` 得到分期表和 `movement-spec.json` 模板。
5. **取证：**结构证据按[真实参考与证据](anatomy-reference-search.md)；动作、激活和数值证据按[证据选择](sports-anatomy.md#5-证据选择)。动作参考优先使用有授权的真人照片/视频截帧、运动捕捉数据或研究原图，记录帧号或时间点。
6. **校验规格：**`python3 scripts/check_movement_spec.py 02_动作分析/movement-spec.json`。错误必须修正；警告逐条核对来源，结论写入审计记录。
7. **构图与生成：**按[生成与资产](generation-and-assets.md)制作。多分期图保持同一人物、同一机位、同一比例和同一配色；肌肉高亮层建议与人体底图分层，方便逐期修改。
8. **标注与检查：**按[文字空间](text-space-and-visible-copy.md)和[质量检查](qa-and-prepress.md)完成，额外检查下方动作专项。

## movement spec 字段

```json
{
  "title": "杠铃后蹲起立期肌肉分工",
  "view": {"plane": "sagittal", "side": "right"},
  "sources": [{"id": "S1", "citation": "作者. 题名. 出处, 年份, 页码/图号", "checked_scope": "实际支持范围"}],
  "phases": [{
    "id": "ascent", "name": "起立（向心）", "events": "最低点 → 站立位",
    "joint_actions": [{"joint": "knee", "action": "extension", "angle_deg": null, "source_ids": []}],
    "muscles": [{"muscle": "vastus_lateralis", "role": "agonist", "contraction": "concentric",
                 "controls": "knee:extension", "source_ids": ["S1"]}],
    "arrows": [{"type": "force", "target": "ground_reaction", "source_ids": ["S1"]}]
  }]
}
```

| 字段 | 说明 |
|---|---|
| `view.plane` | `sagittal` / `frontal` / `transverse`，可为数组；用于检查动作在当前视角是否可见 |
| `joint_actions` | 关节和动作取自 `data/joint-actions.json` |
| `muscles[].muscle` | 取自 `data/muscles.json` 的 `id`；图谱外的肌肉先补入项目副本并登记来源 |
| `role` / `contraction` | 见[角色与收缩](sports-anatomy.md#2-肌肉角色与收缩方式) |
| `controls` | 该肌肉产生或控制的本分期关节动作，格式 `关节:动作` |
| `angle_deg`、`range_deg`、`timing_pct`、`emg_pct`、`velocity`、`force_n` | 任何数值都必须带 `source_ids` |
| `arrows[].type` | `motion` / `force` / `torque` / `sequence`；力和力矩箭头必须有来源 |

## 动作专项检查

| 检查 | 要点 |
|---|---|
| 分期连续 | 相邻分期的关节角度、负荷位置、支撑足和人物朝向连续 |
| 平衡与支撑 | 重心投影落在支撑面内（动态动作按参考），负荷位置符合动作规范 |
| 关节对线 | 侧视图中膝、髋、踝和杠铃/负荷的相对位置与参考一致；冠状面检查膝与足尖方向 |
| 肌肉高亮 | 高亮范围与真实起止点一致；同一肌肉在各分期的颜色编码与收缩方式一致 |
| 文字强度 | “主要”“参与”“稳定”与证据强度相符；不写“唯一”“完全孤立”等绝对表述 |
| 安全示范 | 示范姿势不包含已知高风险错误；错误示范必须明确标注并与正确示范区分 |
