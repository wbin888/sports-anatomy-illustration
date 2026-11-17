# README 示例图参考对照表

README 中每幅示例图的解剖结构、肌肉角色与机制关系，都对应到下表的具体来源。图中标注的来源 ID（如 `G350`）与本表一致。

> **核验范围**：已通过公开目录检索核对图号、图题与文献信息，**尚未下载原图逐项对照形态**。所有示例图的状态为“制作完成，医学待审”。标注“待核”的条目，图号或图题仍需对照原书确认。
>
> 示例图为本仓库原创的简化示意图，**没有复制**任何来源中的图像。Gray 1918 与 NCI SEER 为公有领域；OpenStax 为 CC BY 4.0，本仓库仅将其作为结构对照参考，不复制其图片或文字。

## 来源表

| ID | 来源 | 许可 | 核对范围 | 状态 |
|---|---|---|---|---|
| G345 | Gray H. *Anatomy of the Human Body*, 20th ed., 1918, Fig. 345：右膝关节，前面观 | 公有领域 | 髌骨、髌腱、股四头肌腱的相对位置 | 图题已核 |
| G350 | Gray 1918, Fig. 350：右膝关节矢状切面 | 公有领域 | 髌腱连接髌骨下端与胫骨粗隆 | 图题已核 |
| G389 | Gray 1918：背部深层肌（竖脊肌） | 公有领域 | 竖脊肌沿脊柱两侧纵行 | 图号已核 |
| G430 | Gray 1918：大腿前区肌（股四头肌） | 公有领域 | 股四头肌位于大腿前侧、止于髌骨 | 图题待核 |
| GGM | Gray 1918 臀大肌图版（Wikimedia Commons: `File:Gluteus_maximus_muscle.PNG`） | 公有领域 | 臀大肌起于髂骨后部、骶骨，止于臀肌粗隆与髂胫束 | 图号待核 |
| G439 | Gray 1918：小腿后群浅层肌（腓肠肌、比目鱼肌） | 公有领域 | 小腿三头肌经跟腱止于跟骨 | 图题待核 |
| SEER | NCI SEER Training Modules, *Structure of Skeletal Muscle* | 公有领域（美国政府作品） | 肌肉→肌束→肌纤维层次及肌外膜/肌束膜/肌内膜 | 已核 |
| OSX | Betts JG et al. *Anatomy and Physiology* 2e, OpenStax, 2022：图 4.18、10.3、10.4、10.5 | CC BY 4.0（仅对照，未复制） | 骨骼肌层次、肌纤维多核且核位于边缘、肌节 Z 线/A 带/I 带/M 线 | 图号已核 |
| SCH10 | Schoenfeld BJ. Squatting kinematics and kinetics and their application to exercise performance. *J Strength Cond Res* 2010;24(12):3497–3506. PMID 20182386 | 引用 | 深蹲主要参与肌群：臀大肌、股四头肌、竖脊肌稳定 | 已核；小腿三头肌的收缩方式为据关节动作推断 |
| DRU09 | Drummond MJ et al. Rapamycin administration in humans blocks the contraction-induced increase in skeletal muscle protein synthesis. *J Physiol* 2009;587:1535–1546. doi:10.1113/jphysiol.2008.163816 | 引用 | 人体中雷帕霉素抑制 mTORC1 并阻断收缩诱导的肌蛋白合成增加 | 已核 |
| HOR11 | Hornberger TA. Mechanotransduction and the regulation of mTORC1 signaling in skeletal muscle. *Int J Biochem Cell Biol* 2011;43(9):1267–1276. PMC3146557 | 引用 | 机械负荷激活 mTORC1 的感受机制尚未明确 | 已核；图中按假说处理（虚线） |
| JOA20 | Joanisse S et al. Recent advances in understanding resistance exercise training-induced skeletal muscle hypertrophy in humans. *F1000Research* 2020;9:F1000 Faculty Rev-141. PMID 32148775 | 引用 | 肌蛋白合成累积与肌纤维横截面积增加 | 已核 |
| NHS | NHS. *Knee pain*. https://www.nhs.uk/symptoms/knee-pain/ | 引用 | 就医提示：疼痛数周未好转或明显肿胀时就医 | 已核 |

## 逐图映射

### 杠铃后蹲两分期（`docs/images/squat-phases.png`）

| 图中元素 | 来源 |
|---|---|
| 臀大肌位置 | GGM |
| 股四头肌位置 | G430 |
| 小腿三头肌位置 | G439 |
| 竖脊肌位置 | G389 |
| 下蹲离心、起立向心；竖脊肌等长稳定 | SCH10 |
| 小腿三头肌下蹲离心、起立向心 | 依据踝背屈/跖屈方向推断（`data/joint-actions.json`），待医学审核 |

### 科普漫画：跑步后膝前痛（`docs/images/comic-example.png`）

| 图中元素 | 来源 |
|---|---|
| 股四头肌腱、髌骨、髌腱、胫骨的位置关系 | G345、G350 |
| “髌腱连接髌骨下端和胫骨” | G350 |
| 就医提示 | NHS |

### 教学插画：骨骼肌结构层次（`docs/images/teaching-example.png`）

| 图中元素 | 来源 |
|---|---|
| ① 肌肉、② 肌束及肌外膜、肌束膜 | SEER；OSX 图 10.3 |
| ③ 肌纤维、肌内膜、细胞核位于边缘 | OSX 图 4.18、10.4 |
| ④ 肌原纤维横纹、⑤ 肌节（Z 线、M 线、A 带、I 带，粗/细肌丝） | OSX 图 10.5 |

### 科研示意图：抗阻训练与肌肥大（`docs/images/research-example.png`）

关系登记见 [`research-example.mechanism-graph.json`](research-example.mechanism-graph.json)，可用以下命令检查记录是否自洽：

```bash
python3 skills/sports-anatomy-illustration/scripts/check_mechanism_graph.py docs/examples/research-example.mechanism-graph.json
```

| 图中关系 | 证据状态 | 线型 | 来源 |
|---|---|---|---|
| 抗阻训练 → 机械感受 | 过程 | 实线箭头 | HOR11 |
| 机械感受 → mTORC1 激活 | 假说（感受器未明） | 虚线箭头 | HOR11 |
| mTORC1 激活 → 肌蛋白合成 ↑ | 已证实 | 实线箭头 | DRU09 |
| 雷帕霉素 ⊣ mTORC1 | 已证实 | 平头抑制线 | DRU09 |
| 肌蛋白合成 ↑ → 肌纤维横截面积 ↑ | 已观察 | 实线箭头 | JOA20 |

### 横幅与流程图

`banner.png` 与 `workflow.png` 不含解剖结构，无需解剖参考。
