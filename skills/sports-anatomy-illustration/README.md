# Sports Anatomy Illustration 1.0.0 · 运动解剖与医学绘图

面向人体解剖与运动解剖插画、训练动作肌肉分工图、动作分期/步态图、运动损伤与康复示意、医学科普漫画及涉及医学结构的科研示意图。流程沿用真实参考 → 视觉设计与文字空间 → 彩色无字画面 → 可编辑排字 → 逐页检查与交付，并增加运动解剖专项：动作坐标、肌肉角色与收缩方式、力/力矩箭头和动作规格校验。

从 [SKILL.md](SKILL.md) 开始，按任务读取对应分支：

- [运动解剖绘图规则](references/sports-anatomy.md)
- [动作分析与分期图](references/movement-analysis.md)
- [运动损伤机制与康复图示](references/sports-injury-and-rehab.md)
- [安装与依赖](references/dependencies-installation.md)、[Agent 接入](references/agent-integration.md)
- 数据：`data/muscles.json`（33 块主要运动肌）、`data/joint-actions.json`（关节动作词表）、`data/movements.json`（5 个动作模板）
- 脚本：`scripts/init_project.py [--sports]`、`scripts/check_movement_spec.py`

改编自 wilbert 的 [medical-illustration](https://github.com/wilbert-MD-PhD/medical-illustration)（MIT）。整包采用 MIT，第三方材料遵循各自许可，见 [NOTICE.md](NOTICE.md)。Skill 不表示产出的医学作品已获批准。
