#!/usr/bin/env python3
"""Generate the README illustrations (schematic, not to scale). MIT; see ../../LICENSE.

Usage: python3 docs/images/generate.py
"""
from __future__ import annotations

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent
FONT = "'PingFang SC','Microsoft YaHei','Noto Sans CJK SC','Noto Sans SC',sans-serif"
INK = "#1F2937"
MUTED = "#6B7280"
BONE = "#E5E7EB"
SKIN = "#F3E8DC"
CONC = "#DC2626"   # concentric
ECC = "#EA580C"    # eccentric
ISO = "#2563EB"    # isometric / stabilizer
ACCENT = "#C2410C"


def defs() -> str:
    return f"""<defs>
  <pattern id="ecc" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <rect width="8" height="8" fill="#FFEDD5"/><rect width="4" height="8" fill="{ECC}"/>
  </pattern>
  <pattern id="iso" width="7" height="7" patternUnits="userSpaceOnUse">
    <rect width="7" height="7" fill="#DBEAFE"/><circle cx="3.5" cy="3.5" r="1.8" fill="{ISO}"/>
  </pattern>
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{INK}"/>
  </marker>
  <marker id="arrowA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/>
  </marker>
</defs>"""


def text(x, y, s, size=16, fill=INK, weight="normal", anchor="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>')


def unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    return dx / n, dy / n


def anterior(a, b):
    """Normal toward the anterior side of a proximal->distal segment for a right-facing figure."""
    dx, dy = unit(a, b)
    return dy, -dx


def lerp(a, b, t):
    return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t


def band(a, b, side, fill, t0, t1, offset, width):
    """Muscle belly along segment a->b on one side (+1 anterior, -1 posterior)."""
    nx, ny = anterior(a, b)
    nx, ny = nx * side, ny * side
    p, q = lerp(a, b, t0), lerp(a, b, t1)
    mid = lerp(p, q, 0.5)
    o0 = (p[0] + nx * offset, p[1] + ny * offset)
    o1 = (mid[0] + nx * (offset + 2 * width), mid[1] + ny * (offset + 2 * width))
    o2 = (q[0] + nx * offset, q[1] + ny * offset)
    i0 = (q[0] + nx * 2, q[1] + ny * 2)
    i1 = (p[0] + nx * 2, p[1] + ny * 2)
    d = (f"M{i1[0]:.1f},{i1[1]:.1f} L{o0[0]:.1f},{o0[1]:.1f} Q{o1[0]:.1f},{o1[1]:.1f} {o2[0]:.1f},{o2[1]:.1f} "
         f"L{i0[0]:.1f},{i0[1]:.1f} Z")
    return f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>'


def pose(ankle, ankle_deg, thigh_deg, trunk_deg):
    """Joint positions. ankle_deg: shank forward lean from vertical; thigh_deg: knee->hip angle
    above horizontal (pointing backwards); trunk_deg: trunk forward lean from vertical."""
    shank, thigh, trunk = 112, 112, 132
    a = math.radians(ankle_deg)
    knee = (ankle[0] + shank * math.sin(a), ankle[1] - shank * math.cos(a))
    t = math.radians(thigh_deg)
    hip = (knee[0] - thigh * math.cos(t), knee[1] - thigh * math.sin(t))
    r = math.radians(trunk_deg)
    shoulder = (hip[0] + trunk * math.sin(r), hip[1] - trunk * math.cos(r))
    head = (shoulder[0] + 30 * math.sin(r) + 4, shoulder[1] - 30 * math.cos(r) - 6)
    return dict(ankle=ankle, knee=knee, hip=hip, shoulder=shoulder, head=head)


def figure(j, colors, ghost=False):
    out = []
    ankle, knee, hip, sh, head = j["ankle"], j["knee"], j["hip"], j["shoulder"], j["head"]
    heel, toe = (ankle[0] - 14, ankle[1] + 14), (ankle[0] + 46, ankle[1] + 14)
    stroke = "#D1D5DB" if ghost else INK
    body = "#F9FAFB" if ghost else SKIN
    for a, b, w in ((sh, hip, 40), (hip, knee, 30), (knee, ankle, 24)):
        out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
                   f'stroke="{stroke}" stroke-width="{w + 3}" stroke-linecap="round"/>')
    for a, b, w in ((sh, hip, 40), (hip, knee, 30), (knee, ankle, 24)):
        out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
                   f'stroke="{body}" stroke-width="{w}" stroke-linecap="round"/>')
    out.append(f'<path d="M{heel[0]:.1f},{heel[1]:.1f} L{ankle[0] - 6:.1f},{ankle[1] - 8:.1f} '
               f'L{ankle[0] + 10:.1f},{ankle[1] - 6:.1f} L{toe[0]:.1f},{toe[1]:.1f} Z" '
               f'fill="{body}" stroke="{stroke}" stroke-width="2" stroke-linejoin="round"/>')
    out.append(f'<circle cx="{head[0]:.1f}" cy="{head[1]:.1f}" r="21" fill="{body}" stroke="{stroke}" stroke-width="2"/>')
    if ghost:
        return "\n".join(out)
    for a, b in ((hip, knee), (knee, ankle), (hip, sh)):
        out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
                   f'stroke="{BONE}" stroke-width="5" stroke-linecap="round"/>')
    if "quads" in colors:
        out.append(band(hip, knee, +1, colors["quads"], 0.14, 0.9, 4, 6))
    if "calf" in colors:
        out.append(band(knee, ankle, -1, colors["calf"], 0.08, 0.72, 4, 8))
    if "erector" in colors:
        out.append(band(sh, hip, -1, colors["erector"], 0.1, 0.88, 12, 3))
    if "glute" in colors:
        nx, ny = anterior(hip, knee)
        ux, uy = unit(hip, knee)
        cx, cy = hip[0] - nx * 15 + ux * 6, hip[1] - ny * 15 + uy * 6
        ang = math.degrees(math.atan2(uy, ux))
        out.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="24" ry="14" transform="rotate({ang:.1f} {cx:.1f} {cy:.1f})" '
                   f'fill="{colors["glute"]}" stroke="{INK}" stroke-width="1.2"/>')
    for p in (hip, knee, ankle):
        out.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="6" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    nx, ny = anterior(sh, hip)
    bx, by = sh[0] - nx * 22, sh[1] - ny * 22 + 6
    out.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="15" fill="#374151"/><circle cx="{bx:.1f}" cy="{by:.1f}" r="5" fill="#9CA3AF"/>')
    return "\n".join(out)


def label(x, y, x0, side, ty, s):
    """Leader line from point (x, y) to a label on the left or right margin of a panel at x0."""
    w = 14 * len(s)
    if side == "left":
        tx, end = x0 + 20, x0 + 20 + w + 6
        anchor = "start"
    else:
        tx, end = x0 + 400, x0 + 400 - w - 6
        anchor = "end"
    return (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{end:.1f}" y2="{ty:.1f}" stroke="{MUTED}" stroke-width="1.2"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{INK}"/>'
            + text(tx, ty + 5, s, 14, INK, anchor=anchor))


def squat_svg() -> str:
    W, H = 1000, 600
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', defs(),
             f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>',
             text(40, 50, "杠铃后蹲 · 两分期肌肉分工（右侧矢状面）", 24, INK, "bold"),
             text(40, 78, "示意图，非按比例；肌肉角色来自 data/movements.json 的 back_squat 模板", 14, MUTED)]
    ground = 486
    panels = [
        (60, "① 下蹲 · 离心", "肌肉在张力下被拉长，控制屈髋、屈膝、踝背屈",
         dict(glute="url(#ecc)", quads="url(#ecc)", calf="url(#ecc)", erector="url(#iso)"), (230, 34, 6, 44), "down"),
        (520, "② 起立 · 向心", "肌肉缩短发力，产生伸髋、伸膝、踝跖屈",
         dict(glute=CONC, quads=CONC, calf=CONC, erector="url(#iso)"), (680, 24, 30, 36), "up"),
    ]
    for x0, title, sub, colors, (ax, ankle_deg, thigh_deg, trunk_deg), direction in panels:
        parts.append(f'<rect x="{x0}" y="100" width="420" height="420" rx="14" fill="#F9FAFB" stroke="#E5E7EB"/>')
        parts.append(text(x0 + 20, 132, title, 20, INK, "bold"))
        parts.append(text(x0 + 20, 156, sub, 13, MUTED))
        parts.append(f'<line x1="{x0 + 20}" y1="{ground + 15}" x2="{x0 + 400}" y2="{ground + 15}" stroke="#9CA3AF" stroke-width="2"/>')
        j = pose((ax, ground), ankle_deg, thigh_deg, trunk_deg)
        parts.append(figure(j, colors))
        ex = x0 + 392
        y1, y2 = (180, 255) if direction == "down" else (255, 180)
        parts.append(f'<line x1="{ex}" y1="{y1}" x2="{ex}" y2="{y2}" stroke="{ACCENT}" stroke-width="5" marker-end="url(#arrowA)"/>')
        hip, knee, sh, ankle = j["hip"], j["knee"], j["shoulder"], j["ankle"]
        nx, ny = anterior(hip, knee)
        parts.append(label(hip[0] - nx * 18, hip[1] - ny * 18, x0, "left", hip[1] + 60, "臀大肌"))
        q = lerp(hip, knee, 0.55)
        parts.append(label(q[0] + nx * 12, q[1] + ny * 12, x0, "right", q[1] - 70, "股四头肌"))
        c = lerp(knee, ankle, 0.4)
        cn = anterior(knee, ankle)
        parts.append(label(c[0] - cn[0] * 14, c[1] - cn[1] * 14, x0, "left", ground - 6, "小腿三头肌"))
        e = lerp(sh, hip, 0.5)
        en = anterior(sh, hip)
        parts.append(label(e[0] - en[0] * 24, e[1] - en[1] * 24, x0, "left", 200, "竖脊肌（稳定）"))
    ly = 556
    items = [(CONC, "向心收缩（缩短发力）"), ("url(#ecc)", "离心收缩（拉长控制）"), ("url(#iso)", "等长收缩 / 稳定肌")]
    x = 60
    for fill, s in items:
        stroke = "#D1D5DB" if fill == "#F9FAFB" else INK
        parts.append(f'<rect x="{x}" y="{ly - 14}" width="34" height="18" rx="4" fill="{fill}" stroke="{stroke}"/>')
        parts.append(text(x + 44, ly, s, 14))
        x += 280
    parts.append("</svg>")
    return "\n".join(parts)


def workflow_svg() -> str:
    W, H = 1000, 230
    steps = [("动作问题", "读者要看懂什么"), ("真实取证", "教材 / EMG / 动捕"), ("动作规格", "movement-spec.json"),
             ("自洽校验", "规格校验脚本"), ("生成与排字", "无字底图 + 可编辑字"), ("质检交付", "医学待审 / 审签")]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', defs(),
             f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>',
             text(40, 46, "制作流程", 22, INK, "bold"),
             text(140, 46, "运动解剖模块在原医学绘图流程上增加动作规格与校验（橙色）", 14, MUTED)]
    bw, gap, y = 138, 26, 76
    for i, (title, sub) in enumerate(steps):
        x = 40 + i * (bw + gap)
        new = i in (2, 3)
        parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="96" rx="14" fill="{"#FFF7ED" if new else "#F9FAFB"}" '
                     f'stroke="{ACCENT if new else "#D1D5DB"}" stroke-width="{2.5 if new else 1.5}"/>')
        parts.append(f'<circle cx="{x + 24}" cy="{y + 28}" r="13" fill="{ACCENT if new else INK}"/>')
        parts.append(text(x + 24, y + 33, str(i + 1), 14, "#FFFFFF", "bold", "middle"))
        parts.append(text(x + 44, y + 34, title, 17, INK, "bold"))
        parts.append(text(x + bw / 2, y + 72, sub, 12, MUTED, anchor="middle"))
        if i < len(steps) - 1:
            parts.append(f'<line x1="{x + bw + 3}" y1="{y + 48}" x2="{x + bw + gap - 3}" y2="{y + 48}" '
                         f'stroke="{INK}" stroke-width="2" marker-end="url(#arrow)"/>')
    parts.append(text(40, 208, "校验通过只说明规格自洽，不代表医学正确；医学审签与制作状态分开记录。", 13, MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


def banner_svg() -> str:
    W, H = 1000, 260
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', defs(),
             '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7C2D12"/>'
             '<stop offset="1" stop-color="#C2410C"/></linearGradient>',
             f'<rect width="{W}" height="{H}" rx="20" fill="url(#bg)"/>',
             text(48, 96, "运动解剖与医学绘图", 44, "#FFFFFF", "bold"),
             text(50, 134, "Sports Anatomy Illustration · Agent Skill", 22, "#FED7AA"),
             text(50, 178, "动作分期 · 肌肉分工 · 损伤与康复示意 · 真实取证 · 可编辑交付", 18, "#FFFFFF")]
    x = 50
    for c in ["33 块运动肌图谱", "5 个动作模板", "动作规格校验器"]:
        w = 30 + len(c) * 14
        parts.append(f'<rect x="{x}" y="200" width="{w}" height="32" rx="16" fill="#FFFFFF" fill-opacity="0.16" stroke="#FED7AA"/>')
        parts.append(text(x + w / 2, 221, c, 14, "#FFFFFF", anchor="middle"))
        x += w + 12
    j = pose((0, 0), 34, 6, 44)
    fig = figure(j, dict(glute=CONC, quads=CONC, calf=CONC, erector="url(#iso)"))
    parts.append(f'<circle cx="845" cy="130" r="112" fill="#FFFFFF" fill-opacity="0.95"/>')
    parts.append(f'<g transform="translate(815 205) scale(0.62)">{fig}</g>')
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    (OUT / "banner.svg").write_text(banner_svg(), encoding="utf-8")
    (OUT / "squat-phases.svg").write_text(squat_svg(), encoding="utf-8")
    (OUT / "workflow.svg").write_text(workflow_svg(), encoding="utf-8")
    print("written:", ", ".join(p.name for p in sorted(OUT.glob("*.svg"))))


if __name__ == "__main__":
    main()
