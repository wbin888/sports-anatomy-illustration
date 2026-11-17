# 安装与依赖

本 Skill 面向可读取指令及相关资源的 Agent，按[适配说明](agent-integration.md)映射工具。安装完整 `sports-anatomy-illustration/` 文件夹，保留 SKILL.md、references、data、assets、scripts、VERSION 及许可文件。`agents/` 为可选宿主界面元数据，其他宿主可忽略。图像模型、医学图谱、字体二进制与商业软件许可证按任务准备。

## 安装与加载

- 原生支持 Skill：使用宿主实际可用的安装器或复制完整目录到其配置位置。先检查同名目录，保留已有修改，避免重复加载。
- 有文件/资源访问能力：完整目录放到可访问位置，在请求中指定 `SKILL.md` 的实际路径或资源标识。
- 仅附件或文本：提供入口和本次所需分支，按适配说明交接图像、文件执行与视觉检查。

本版 VERSION 见同目录 `VERSION`。源码中的 Skill 位于仓库 `skills/sports-anatomy-illustration/`，安装时复制整个目录。

安装路径采用宿主配置或实际安装结果。刷新后核对加载路径与 VERSION。对于直接读取方式，重新读取入口及本次使用的资源。只有支持相应语法的宿主才使用 `$sports-anatomy-illustration` 或 `$skill-installer`，自然语言和明确路径是通用入口。

## 更新

独立安装通过重新拉取仓库或下载新版目录覆盖更新；覆盖前备份并保留本地修改。插件管理的副本由宿主更新。

## 依赖按任务选择

- 初始化器与动作规格校验：Python 3.9+，仅标准库。初始化器不是使用 Skill 的必需步骤。
- 图像生成/编辑：实际可调用且满足本次输入需求的工具。可附入合规真实参考直接生成彩色画面；复杂结构按需约束。
- 医学内容：匹配的真实参考、实际查看及用途核验；图像证据与文字论断分别核对。
- 可编辑排字：Illustrator 或保留真实文字对象的矢量工具。指定 `.ai` 时需原生格式实际验收。macOS 运行器、预检与会话库已随包提供，见[调用及平台限制](illustrator-runtime.md)；可选裁切另需 Pillow。
- PPTX：按[原生对象与同版导出](pptx-delivery.md)选择现有编辑器/API 与 Office 导出器，分别验收中文文字、箭头、引线及 PDF/PNG。
- 中文字体和 PDF：使用环境中实际可用、许可与用途匹配的字体及导出器；实际导出并看图。
- `humanize-writing`、`baoyu-comic`、三维工具、影像工具：可选，仅遇到对应任务才使用。缺失时用包内流程，不批量安装。
- 人工审阅与制作状态：按[共用规则](../SKILL.md#共用医学与进度规则)执行。

详细实际测试见[首次环境检查](first-run.md)。包级检查不能证明图像生成、医学准确性或人工签字。

## 初始化器验收

从 Skill 根目录执行（或使用脚本实际路径）：

```bash
python3 ../../tests/test_init_project.py   # 在仓库中运行
python3 scripts/init_project.py /path/to/new-project
python3 scripts/init_project.py /path/to/new-project --type teaching   # 教学与宣教插画
python3 scripts/init_project.py /path/to/new-project --type research --sports   # 运动科研示意图
python3 scripts/check_movement_spec.py                           # 自检随包动作模板
```

按 `--type` 建立不同作品类型的目录：`comic`（默认，科普漫画）与 `teaching`（教学与宣教插画）各建 5 个必要目录、5 份轻量模板（含来源与许可），分别使用页面清单与图版清单；`research`（科研示意图）建立图稿规格、可通过 `check_mechanism_graph.py` 的占位 `mechanism-graph.json` 与图注模板，不含角色或对白。`--sports` 可与任一类型叠加，另建 `02_动作分析/` 及动作分期表与 `movement-spec.json`，不另建固定线稿或多轮审核目录。重复运行保留用户文件，补齐缺失模板；目录/文件冲突和根目录以下的符号链接在写入前拒绝。用户选择的根路径会解析到真实位置；不要在初始化同时改动目录结构，磁盘故障不保证事务回滚。

旧版 13 份模板不会被迁移或删除；沿用已有项目主稿即可，不为升级重建平行目录。
