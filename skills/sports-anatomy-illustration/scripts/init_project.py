#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create a non-destructive medical / sports-anatomy illustration project scaffold."""

# Code and embedded runtime templates: MIT License; see ../LICENSE-CODE.

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SKILL_VERSION = Path(__file__).resolve().parent.parent.joinpath("VERSION").read_text(encoding="utf-8").strip()

TEMPLATE_NOTICE = (
    "\n---\n模板来源：sports-anatomy-illustration（改编自 wilbert 的 medical-illustration）；"
    "作者：wilbert、wbin888；许可：MIT；完整版权与许可见本项目 00_项目规范/LICENSE-CODE。\n"
    "模板原文由初始化脚本复制；后续修改请记录。此声明适用于复制的模板内容，"
    "不自动覆盖使用者新增内容或独立创作作品。\n"
)

DIRECTORIES = ['00_项目规范', '01_证据', '07_审计记录']

FILES = {
    '00_项目规范/项目说明.md': """# 项目说明

- 项目名称：
- 作品类型：{kind_label}（规则见 Skill 的 references/output-types.md）
- 图型：{figure_types}
- 读者与项目目标：
- 当前主稿与视觉/角色基准：
- 工作规格与出版规格状态：
- 制作进度与人工审签状态（分别记录）：

{kind_note}

唯一画面、调用记录及制作工具保存在正式目录；临时目录只存可重建文件。默认交付普通文件夹和文件链接，不自动压缩。
""",
    '01_证据/医学事实与来源.md': """# 医学事实与来源

按事实 ID 记录论断、来源、定位、支持范围和使用页面、图版或图上对象。

## 解剖图像来源与许可

每个实际图版/模型版本一条，含人工核对及上游来源。记录原作者/作品/版本/URL/图号/双页码、本地文件与哈希、医学支持范围、具体许可及凭据、各用途核验、实际调用链接和输入输出映射、修改与拟刊署名。共享凭据链接引用，同源多页合并。
""",
    '07_审计记录/问题与变更.md': """# 问题与变更

| 页面/图稿与版本 | 问题与检查类别 | 修改目标和影响范围 | 新版及复核结论 | 人工意见凭据（如有） |
|---|---|---|---|---|

制作、美术/编辑、医学图文对照、人工审签和印前状态分别记录。
""",
}

FILES["00_项目规范/模板来源与许可说明.md"] = """# 模板来源与许可说明

- 来源：sports-anatomy-illustration，版本：""" + SKILL_VERSION + """；改编自 wilbert 的 medical-illustration（MIT）。
- 作者：wilbert、wbin888；Copyright © 2026 wilbert；Copyright © 2026 wbin888。
- 复制的文字模板与初始化器代码均采用 MIT，允许商业使用。
- 分发模板副本或实质部分时，保留版权与完整许可声明，见同目录 LICENSE-CODE。
- 使用流程创作的新插画、漫画或文档不自动继承模板许可；实际复制的模板内容和纳入的第三方素材仍按各自许可处理。
- 脚本不覆盖已有文件，也不自动为已有模板补写署名。迁移旧项目时，请在分发复制的模板内容前核对来源声明。
- 修改记录：初始化为原模板副本；后续修改由使用者记录。
"""


KINDS = {
    "comic": {
        "label": "面向患者和公众的科普漫画",
        "figure_types": "科普漫画（单页/多页）/ 漫画中的运动讲解页 / 其他",
        "note": "按 Skill 的 references/workflow.md 制作；对白、气泡和标注在排字阶段独立可编辑。",
        "directories": ['04_脚本与分配表', '06_彩稿与排版'],
        "files": {
    '04_脚本与分配表/页面清单.md': """# 页面清单

| 页面 ID | 读者问题与视觉重点 | 当前脚本 | 来源/角色版本 | 生成记录 | 当前画面与检查状态 |
|---|---|---|---|---|---|

记录实际可见文字、标题与对白位置及预计行数，空间规划按 Skill 的 references/text-space-and-visible-copy.md。按本次格式建立可编辑文字与标注，PPTX 交付见 references/pptx-delivery.md。
""",
        },
    },
    "teaching": {
        "label": "教学与宣教用的医学插画",
        "figure_types": "解剖教学插画 / 患者宣教图 / 运动解剖与动作分析图 / 运动损伤与康复图示 / 其他",
        "note": "按 Skill 的 references/workflow.md 制作，单幅或系列图版不需要角色与对白；宣教图另按 references/output-types.md 核对行动建议与就医提示。",
        "directories": ['04_脚本与分配表', '06_彩稿与排版'],
        "files": {
            '04_脚本与分配表/图版清单.md': """# 图版清单

| 图版 ID | 读者与教学/宣教目标 | 结构、层次、视角与侧别 | 标签清单（标准名/公众表达） | 来源 ID | 生成记录 | 当前画面与检查状态 |
|---|---|---|---|---|---|---|

## 宣教图附加项（面向患者或公众时填写）

- 读者能做的具体行动及其依据（来源 ID）：
- 需要就医或停止活动的警示信号及其依据：
- 适用人群与不适用情形；不替代个体诊疗的提示位置：
- 可读性检查：术语替换、字号、对比度、无恐吓或责备表达：

标签先按实际文字试排，再生成或修改底图，规则见 references/text-space-and-visible-copy.md。
""",
        },
    },
    "research": {
        "label": "涉及医学结构的科研示意图",
        "figure_types": "医学结构示意图 / 结构与机制结合图 / 图形摘要 / 运动生物力学或训练机制示意 / 其他",
        "note": "按 Skill 的 references/research-workflow.md 制作，不使用角色或对白；结构证据与机制证据分别登记。",
        "directories": ['03_图稿规格', '05_图注与交付'],
        "files": {
            '03_图稿规格/图稿规格.md': """# 图稿规格

完整字段见 Skill 的 references/research-figure-spec.md；纯结构图可省略机制关系。

## 图稿目标

- 图稿 ID/版本、当前主稿和输出位置：
- 图型、读者、用途；目标期刊/图型政策及核查日期：
- 一句话主旨（受证据约束）：
- 物种/组织/细胞/实验模型与时程条件：
- 用户实测结果、文献背景和假说的范围：

## 结构与视觉参考

| 对象 ID | 结构/状态及区室 | 视角/切面与连接/层次约束 | 允许简化与关键避错点 | 参考 ID、实际查看位置 | 对应图上对象/区域 |
|---|---|---|---|---|---|

## 机制关系（有此内容时填写）

可直接维护同目录 mechanism-graph.json，并用 scripts/check_mechanism_graph.py 检查记录一致性；不重复维护两份。

| 关系 ID | 起点与终点/区室 | 关系与直接性 | 证据类型、支持范围与条件 | 来源/核验位置 | 线型、端点及图上对象 ID |
|---|---|---|---|---|---|

## 构图与绘制输入

- 主视觉、阅读顺序、放大选区：
- 视觉表现（平面/2.5D/三维）与细节层级：
- 标签容量、引线通道与须避让结构：
- 实现方式与可编辑范围；实际附入的参考与草图：
""",
            '03_图稿规格/mechanism-graph.json': None,
            '05_图注与交付/图注.md': """# 图注

- 图题：
- 核心结论（区分本研究结果、文献背景与假说）：
- 模型/物种与条件：
- 符号、线型、端点与缩写：
- 被省略的关键中间步骤：
- 必要来源：

| 检查层 | 检查对象/版本与依据 | 实际结论/未检查项 | 修订及复核位置 |
|---|---|---|---|
| 医学结构对照 | | | |
| 机制关系（如有） | | | |
| 视觉表现与实际尺寸可读性 | | | |
| 源文件可编辑性与导出 | | | |
""",
        },
    },
}

MECHANISM_GRAPH_TEMPLATE = {
    "nodes": [
        {"id": "N1", "label": "待填写：起点", "compartment": "待填写"},
        {"id": "N2", "label": "待填写：终点", "compartment": "待填写"},
    ],
    "edges": [
        {
            "id": "E1", "source": "N1", "target": "N2", "relation": "activation",
            "evidence_status": "hypothesis", "directness": "unspecified", "source_ids": ["S1"],
            "line_style": "dashed", "arrowhead": "arrow",
            "note": "占位示例：按实际证据改写；未核验前保持 hypothesis。",
        }
    ],
    "sources": [{"id": "S1", "citation": "待填写", "checked_scope": "未核验"}],
}


SPORTS_DIRECTORIES = ['02_动作分析']

SPORTS_FILES = {
    '02_动作分析/动作分期表.md': """# 动作分期表

按 Skill 的 references/movement-analysis.md 填写。每个分期一行；角度、时序与肌肉激活写来源 ID，未核实的数值留空。

| 分期 ID | 动作/分期名称 | 起止事件 | 观察平面与视角 | 主要关节动作（关节:动作） | 主动肌与收缩方式 | 稳定/拮抗肌 | 角度或时序（来源 ID） | 成图位置 |
|---|---|---|---|---|---|---|---|---|

## 风险与表达限定

- 受试者/人群（如训练水平、性别、年龄、负荷）：
- 不得画成普遍规律的个体差异或研究局限：
- 涉及训练、康复或损伤预防建议时的证据等级与适用条件：
""",
    '02_动作分析/movement-spec.json': None,
}


FILES["00_项目规范/LICENSE-CODE"] = Path(__file__).resolve().parent.parent.joinpath("LICENSE-CODE").read_text(encoding="utf-8")

def validate_path(root: Path, target: Path, *, directory: bool) -> None:
    """Reject conflicting types and symlinks below the selected project root."""
    if root.exists() and not root.is_dir():
        raise ValueError(f"项目根路径不是目录: {root}")
    relative = target.relative_to(root)
    current = root
    for index, part in enumerate(relative.parts):
        current = current / part
        if current.is_symlink():
            raise ValueError(f"项目内路径不能是符号链接: {current}")
        wants_dir = directory or index < len(relative.parts) - 1
        if current.exists() and not (current.is_dir() if wants_dir else current.is_file()):
            expected = "目录" if wants_dir else "普通文件"
            raise ValueError(f"路径类型冲突，应为{expected}: {current}")


def sports_spec_template() -> str:
    example = Path(__file__).resolve().parent.parent / "assets" / "movement-spec.example.json"
    return example.read_text(encoding="utf-8")


def planned(sports: bool = False, kind: str = "comic") -> tuple[list[str], dict[str, str]]:
    if kind not in KINDS:
        raise ValueError(f"未知作品类型: {kind}")
    spec = KINDS[kind]
    directories = list(DIRECTORIES) + spec["directories"]
    files = dict(FILES)
    files["00_项目规范/项目说明.md"] = files["00_项目规范/项目说明.md"].format(
        kind_label=spec["label"], figure_types=spec["figure_types"], kind_note=spec["note"]
    )
    for relative, content in spec["files"].items():
        files[relative] = (
            json.dumps(MECHANISM_GRAPH_TEMPLATE, ensure_ascii=False, indent=2) + "\n"
            if content is None else content
        )
    if sports:
        directories += SPORTS_DIRECTORIES
        for relative, content in SPORTS_FILES.items():
            files[relative] = sports_spec_template() if content is None else content
    return directories, files


def initialize(root: Path, sports: bool = False, kind: str = "comic") -> tuple[int, int, int]:
    DIRECTORIES, FILES = planned(sports, kind)
    # Inspect every planned path before creating anything. Explicit root aliases
    # are resolved by main(); nested symlinks are rejected, even when dangling.
    for relative in DIRECTORIES:
        validate_path(root, root / relative, directory=True)
    for relative in FILES:
        validate_path(root, root / relative, directory=False)

    root.mkdir(parents=True, exist_ok=True)
    created_dirs = created_files = skipped_files = 0
    for relative in DIRECTORIES:
        target = root / relative
        validate_path(root, target, directory=True)
        if not target.exists():
            created_dirs += 1
        target.mkdir(parents=True, exist_ok=True)

    for relative, content in FILES.items():
        target = root / relative
        validate_path(root, target, directory=False)
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            # Exclusive creation also preserves a file created since preflight.
            with target.open("x", encoding="utf-8") as output:
                output.write(content if not relative.endswith(".md") else content + TEMPLATE_NOTICE)
        except FileExistsError:
            validate_path(root, target, directory=False)
            skipped_files += 1
        else:
            created_files += 1
    return created_dirs, created_files, skipped_files


def main() -> int:
    # Preserve the caller's encoding; escape characters it cannot represent.
    # Configure before argparse so help and error messages are covered too.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(
        description="按作品类型创建科普漫画、教学与宣教插画或科研示意图项目目录，可叠加运动解剖模板。保留已有文件，拒绝类型冲突与项目内符号链接。"
    )
    parser.add_argument("project_dir", type=Path, help="目标项目目录")
    parser.add_argument(
        "--type", dest="kind", choices=sorted(KINDS), default="comic",
        help="作品类型：comic=科普漫画（默认），teaching=教学与宣教插画，research=科研示意图",
    )
    parser.add_argument("--sports", action="store_true", help="同时创建运动解剖动作分期表与 movement-spec.json 模板")
    args = parser.parse_args()
    try:
        root = args.project_dir.expanduser().resolve()
        created_dirs, created_files, skipped_files = initialize(root, sports=args.sports, kind=args.kind)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"初始化失败: {error}", file=sys.stderr)
        return 1

    print(f"项目目录: {root}")
    print(f"新建目录: {created_dirs}")
    print(f"新建模板: {created_files}")
    print(f"跳过已有模板: {skipped_files}")
    if skipped_files:
        print("已有文件未修改；分发旧模板前请核对模板来源与许可说明。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
