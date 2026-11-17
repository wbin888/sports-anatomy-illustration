# Sports Anatomy Illustration 1.1.0 · 运动解剖与医学绘图

制作三类医学作品，并可在任一类中加入运动解剖内容：

| 作品类型 | 说明 |
|---|---|
| 面向患者和公众的科普漫画 | 从生活情境出发，用人物对白和连续画面讲清一个医学问题 |
| 教学与宣教用的医学插画 | 依据真实参考表现解剖层次、损伤位置与修复过程，配上清楚的标签；宣教图另核对行动建议与就医提示 |
| 涉及医学结构的科研示意图 | 根据研究论断与证据组织结构和机制，区分已证实关系与假说 |
| 运动解剖（可叠加） | 动作坐标、肌肉角色与收缩方式、力/力矩箭头、运动损伤与康复，以及动作规格校验 |

从 [SKILL.md](SKILL.md) 开始，按任务读取对应分支：

- [作品类型：科普漫画、教学与宣教插画、科研示意图](references/output-types.md)
- [漫画与医学插画流程](references/workflow.md)、[科研绘图流程](references/research-workflow.md)
- [运动解剖绘图规则](references/sports-anatomy.md)、[动作分析与分期图](references/movement-analysis.md)、[运动损伤机制与康复图示](references/sports-injury-and-rehab.md)
- [安装与依赖](references/dependencies-installation.md)、[Agent 接入](references/agent-integration.md)
- 数据：`data/muscles.json`（33 块主要运动肌）、`data/joint-actions.json`（关节动作词表）、`data/movements.json`（5 个动作模板）
- 脚本：`scripts/init_project.py [--type comic|teaching|research] [--sports]`、`scripts/check_movement_spec.py`、`scripts/check_mechanism_graph.py`

改编自 wilbert 的 [medical-illustration](https://github.com/wilbert-MD-PhD/medical-illustration)（MIT）。整包采用 MIT，第三方材料遵循各自许可，见 [NOTICE.md](NOTICE.md)。Skill 不表示产出的医学作品已获批准。
