#!/usr/bin/env python3
"""Generate the README illustrations (schematic, not to scale). MIT; see ../../LICENSE.

PNG: rsvg-convert -z 2 X.svg -o X.png

Usage: python3 docs/images/generate.py
"""
from __future__ import annotations

import math
from xml.sax.saxutils import escape
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
  <marker id="tee" viewBox="0 0 10 14" refX="5" refY="7" markerWidth="5" markerHeight="7" orient="auto">
    <path d="M5,0 L5,14" stroke="{INK}" stroke-width="3"/>
  </marker>
  <marker id="arrowA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/>
  </marker>
</defs>"""


def text(x, y, s, size=16, fill=INK, weight="normal", anchor="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')


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
             text(40, 78, "示意图，非按比例；肌肉角色依据 Schoenfeld 2010，肌肉位置依据 Gray 1918 图版（见 docs/examples/references.md）", 14, MUTED)]
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
             text(50, 178, "科普漫画 · 教学与宣教插画 · 科研示意图 · 运动解剖", 18, "#FFFFFF")]
    x = 50
    for c in ["每幅解剖图可追溯参考", "33 块运动肌图谱", "动作规格校验器"]:
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


def bubble(x, y, w, h, lines, tail, size=15):
    tx, ty = tail
    bx = min(max(tx, x + 24), x + w - 24)
    by = y + h if ty > y + h else y
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>',
           f'<path d="M{bx - 10},{by} L{tx},{ty} L{bx + 10},{by}" fill="#FFFFFF" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>',
           f'<line x1="{bx - 8}" y1="{by}" x2="{bx + 8}" y2="{by}" stroke="#FFFFFF" stroke-width="4"/>']
    for i, line in enumerate(lines):
        out.append(text(x + w / 2, y + 26 + i * (size + 7), line, size, INK, anchor="middle"))
    return "".join(out)


def person(x, ground, shirt, hair, coat=False, arm=None, mood="smile"):
    """Simple cartoon character standing at x; arm=(hand_x, hand_y) for the raised right arm."""
    hip, neck = ground - 78, ground - 150
    leg = "#374151"
    out = [f'<path d="M{x - 9},{hip} L{x - 13},{ground} M{x + 9},{hip} L{x + 13},{ground}" stroke="{leg}" stroke-width="13" stroke-linecap="round"/>']
    body_fill = "#FFFFFF" if coat else shirt
    out.append(f'<rect x="{x - 24}" y="{neck}" width="48" height="{hip - neck + 8}" rx="18" fill="{body_fill}" stroke="{INK}" stroke-width="2"/>')
    if coat:
        out.append(f'<path d="M{x},{neck + 4} L{x},{hip + 4}" stroke="#9CA3AF" stroke-width="2"/>'
                   f'<path d="M{x - 10},{neck} L{x},{neck + 18} L{x + 10},{neck}" fill="{shirt}"/>')
    out.append(f'<path d="M{x - 22},{neck + 12} L{x - 34},{neck + 62}" stroke="{SKIN}" stroke-width="11" stroke-linecap="round"/>')
    hx, hy = arm if arm else (x + 34, neck + 62)
    out.append(f'<path d="M{x + 22},{neck + 12} L{hx},{hy}" stroke="{SKIN}" stroke-width="11" stroke-linecap="round"/>')
    out.append(f'<circle cx="{x}" cy="{neck - 26}" r="27" fill="{SKIN}" stroke="{INK}" stroke-width="2"/>')
    out.append(f'<path d="M{x - 27},{neck - 28} Q{x},{neck - 70} {x + 27},{neck - 28} Q{x + 6},{neck - 44} {x - 27},{neck - 28} z" fill="{hair}"/>')
    out.append(f'<circle cx="{x - 9}" cy="{neck - 24}" r="2.6" fill="{INK}"/><circle cx="{x + 9}" cy="{neck - 24}" r="2.6" fill="{INK}"/>')
    mouth = (f'M{x - 8},{neck - 12} Q{x},{neck - 6} {x + 8},{neck - 12}' if mood == "smile"
             else f'M{x - 7},{neck - 9} Q{x},{neck - 15} {x + 7},{neck - 9}')
    out.append(f'<path d="{mouth}" stroke="{INK}" stroke-width="2" fill="none" stroke-linecap="round"/>')
    return "".join(out)


def knee_lateral(ox, oy, s=1.0):
    """Lateral view of a right knee, anterior to the right (schematic)."""
    def P(x, y):
        return f"{ox + x * s:.1f},{oy + y * s:.1f}"
    out = [
        f'<path d="M{P(-22,-110)} L{P(-22,-28)} Q{P(-30,8)} {P(0,12)} Q{P(32,12)} {P(26,-24)} L{P(18,-110)} z" fill="{BONE}" stroke="{INK}" stroke-width="2"/>',
        f'<path d="M{P(-30,22)} L{P(30,22)} Q{P(36,30)} {P(30,46)} L{P(30,52)} Q{P(38,58)} {P(30,66)} L{P(20,72)} L{P(18,130)} L{P(-16,130)} L{P(-18,60)} Q{P(-34,40)} {P(-30,22)} z" fill="{BONE}" stroke="{INK}" stroke-width="2"/>',
        f'<path d="M{P(30,-96)} Q{P(40,-50)} {P(40,-22)}" stroke="#B91C1C" stroke-width="{9 * s:.1f}" fill="none" stroke-linecap="round"/>',
        f'<ellipse cx="{ox + 44 * s:.1f}" cy="{oy - 4 * s:.1f}" rx="{11 * s:.1f}" ry="{19 * s:.1f}" fill="#FDE68A" stroke="{INK}" stroke-width="2"/>',
        f'<path d="M{P(42,14)} Q{P(40,40)} {P(34,58)}" stroke="#F59E0B" stroke-width="{8 * s:.1f}" fill="none" stroke-linecap="round"/>',
    ]
    return "".join(out)


def comic_svg() -> str:
    W, H = 1000, 400
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', defs(),
             f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>',
             text(30, 40, "科普漫画", 22, INK, "bold"),
             text(130, 40, "示例：跑完步，膝盖前面为什么疼？（三格，示意）", 15, MUTED)]
    pw, ph, y0 = 300, 320, 60
    xs = [30, 350, 670]
    for i, x in enumerate(xs):
        parts.append(f'<rect x="{x}" y="{y0}" width="{pw}" height="{ph}" rx="10" fill="{["#F0F9FF", "#FFF7ED", "#F0FDF4"][i]}" stroke="{INK}" stroke-width="2.5"/>')
        parts.append(f'<line x1="{x}" y1="{y0 + ph - 30}" x2="{x + pw}" y2="{y0 + ph - 30}" stroke="#D1D5DB" stroke-width="2"/>')
    g = y0 + ph - 32
    x = xs[0]
    parts.append(person(x + 150, g, "#38BDF8", "#1F2937", arm=(x + 166, g - 60), mood="worry"))
    parts.append(f'<path d="M{x + 178},{g - 64} l10,-8 M{x + 182},{g - 52} l13,-2 M{x + 178},{g - 42} l10,7" stroke="{CONC}" stroke-width="3" stroke-linecap="round"/>')
    parts.append(bubble(x + 20, y0 + 16, 260, 60, ["跑完步，", "膝盖前面有点疼……"], (x + 140, y0 + 118)))
    x = xs[1]
    parts.append(f'<rect x="{x + 130}" y="{y0 + 88}" width="156" height="190" rx="8" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
    parts.append(knee_lateral(x + 186, y0 + 192, 0.62))
    for ty, t, lx in ((y0 + 126, "股四头肌腱", y0 + 132), (y0 + 186, "髌骨", y0 + 190), (y0 + 222, "髌腱", y0 + 218), (y0 + 262, "胫骨", y0 + 250)):
        parts.append(text(x + 236, ty, t, 12, INK))
    parts.append(f'<line x1="{x + 234}" y1="{y0 + 222 - 4}" x2="{x + 211}" y2="{y0 + 213}" stroke="{INK}" stroke-width="1"/>')
    parts.append(f'<line x1="{x + 234}" y1="{y0 + 186 - 4}" x2="{x + 220}" y2="{y0 + 189}" stroke="{INK}" stroke-width="1"/>')
    parts.append(f'<line x1="{x + 234}" y1="{y0 + 126 - 4}" x2="{x + 211}" y2="{y0 + 140}" stroke="{INK}" stroke-width="1"/>')
    parts.append(f'<line x1="{x + 234}" y1="{y0 + 262 - 4}" x2="{x + 200}" y2="{y0 + 260}" stroke="{INK}" stroke-width="1"/>')
    parts.append(person(x + 70, g, "#0EA5E9", "#6B7280", coat=True, arm=(x + 134, g - 112)))
    parts.append(bubble(x + 14, y0 + 14, 272, 64, ["这是髌腱，", "连接髌骨下端和胫骨。"], (x + 70, y0 + 102)))
    x = xs[2]
    parts.append(person(x + 90, g, "#0EA5E9", "#6B7280", coat=True))
    parts.append(person(x + 215, g, "#38BDF8", "#1F2937"))
    parts.append(bubble(x + 14, y0 + 14, 272, 64, ["疼痛几周都没好转，", "或膝盖明显肿胀，就去看医生。"], (x + 92, y0 + 104)))
    parts.append(text(xs[1] + 138, y0 + 104, "参考 G350、G345", 10, MUTED))
    for i, x in enumerate(xs):
        parts.append(text(x + pw / 2, y0 + ph - 10, ["生活情境引出问题", "依据 Gray 图版讲解结构", "依据 NHS 指引的就医提示"][i], 13, MUTED, anchor="middle"))
    parts.append("</svg>")
    return "\n".join(parts)


def teaching_svg() -> str:
    W, H = 1000, 470
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', defs(),
             f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>',
             text(30, 40, "教学插画", 22, INK, "bold"),
             text(130, 40, "示例：骨骼肌的结构层次（横截面与纵切面，示意，非按比例）", 15, MUTED)]
    RED, PINK, MEM = "#B91C1C", "#FCA5A5", "#FDE68A"
    cy = 175
    # 1 whole muscle
    cx, r = 130, 82
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{MEM}" stroke="{INK}" stroke-width="2"/>')
    for dx, dy, rr in ((-30, -30, 26), (24, -36, 24), (36, 14, 26), (-6, 6, 22), (-38, 26, 22), (12, 46, 22), (-14, -58, 14), (52, -12, 12)):
        parts.append(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="{rr}" fill="{RED}" stroke="{MEM}" stroke-width="4"/>')
    # 2 fascicle
    cx2, r2 = 370, 70
    parts.append(f'<circle cx="{cx2}" cy="{cy}" r="{r2}" fill="{MEM}" stroke="{INK}" stroke-width="2"/>')
    import math as _m
    for ring, n, rr in ((0, 1, 11), (25, 7, 11), (50, 12, 10)):
        for k in range(n):
            a = 2 * _m.pi * k / n + ring
            parts.append(f'<circle cx="{cx2 + ring * _m.cos(a):.1f}" cy="{cy + ring * _m.sin(a):.1f}" r="{rr}" fill="{PINK}" stroke="#FEF3C7" stroke-width="2.5"/>')
    parts.append(f'<path d="M{cx + 36 + 26},{cy + 14 - 18} L{cx2 - 50},{cy - r2 + 8} M{cx + 36 + 26},{cy + 14 + 18} L{cx2 - 50},{cy + r2 - 8}" stroke="{MUTED}" stroke-dasharray="4 4"/>')
    # 3 fiber cross-section
    cx3, r3 = 600, 70
    parts.append(f'<circle cx="{cx3}" cy="{cy}" r="{r3 + 6}" fill="#FEF3C7" stroke="{INK}" stroke-width="2"/>')
    parts.append(f'<circle cx="{cx3}" cy="{cy}" r="{r3}" fill="{PINK}" stroke="{RED}" stroke-width="2"/>')
    for ring, n in ((0, 1), (14, 6), (28, 12), (42, 18), (56, 24)):
        for k in range(n):
            a = 2 * _m.pi * k / n
            parts.append(f'<circle cx="{cx3 + ring * _m.cos(a):.1f}" cy="{cy + ring * _m.sin(a):.1f}" r="4.6" fill="{RED}"/>')
    for a in (-2.2, 0.5, 2.0):
        parts.append(f'<ellipse cx="{cx3 + 64 * _m.cos(a):.1f}" cy="{cy + 64 * _m.sin(a):.1f}" rx="9" ry="5" transform="rotate({_m.degrees(a) + 90:.0f} {cx3 + 64 * _m.cos(a):.1f} {cy + 64 * _m.sin(a):.1f})" fill="#6D28D9"/>')
    parts.append(f'<path d="M{cx2 + 25},{cy - 11} L{cx3 - 58},{cy - r3 + 30} M{cx2 + 25},{cy + 11} L{cx3 - 58},{cy + r3 - 30}" stroke="{MUTED}" stroke-dasharray="4 4"/>')
    # labels row 1
    lab = [(cx, "① 肌肉", "外包肌外膜"), (cx2, "② 肌束", "外包肌束膜"), (cx3, "③ 肌纤维（肌细胞）", "外包肌内膜；细胞核位于边缘")]
    for x, t, sub in lab:
        parts.append(text(x, cy + 112, t, 16, INK, "bold", "middle"))
        parts.append(text(x, cy + 134, sub, 13, MUTED, anchor="middle"))
    parts.append(text(cx3 + 92, cy - 54, "细胞核", 13, INK))
    parts.append(f'<line x1="{cx3 + 90}" y1="{cy - 58}" x2="{cx3 + 34}" y2="{cy - 52}" stroke="{INK}" stroke-width="1"/>')
    parts.append(text(cx3 + 92, cy + 4, "肌原纤维", 13, INK))
    parts.append(f'<line x1="{cx3 + 90}" y1="{cy}" x2="{cx3 + 28}" y2="{cy}" stroke="{INK}" stroke-width="1"/>')
    # 4 myofibril + 5 sarcomere at right
    x0, y4 = 770, 110
    parts.append(text(x0 + 100, y4 - 24, "④ 肌原纤维（纵切面）", 16, INK, "bold", "middle"))
    parts.append(f'<rect x="{x0}" y="{y4}" width="200" height="34" rx="17" fill="#FECACA" stroke="{INK}" stroke-width="1.5"/>')
    for k in range(5):
        bx = x0 + 6 + k * 38
        if k < 4:
            parts.append(f'<rect x="{bx + 12}" y="{y4 + 2}" width="22" height="30" fill="{RED}" opacity="0.85"/>')
        parts.append(f'<line x1="{bx + 4}" y1="{y4 + 1}" x2="{bx + 4}" y2="{y4 + 33}" stroke="{INK}" stroke-width="1.5"/>')
    parts.append(text(x0 + 100, y4 + 56, "明暗相间的横纹", 13, MUTED, anchor="middle"))
    # sarcomere
    sx0, sx1, sy = 790, 950, 260
    parts.append(text((sx0 + sx1) / 2, sy - 34, "⑤ 肌节（两条 Z 线之间）", 16, INK, "bold", "middle"))
    parts.append(f'<rect x="{x0 + 50}" y="{y4 + 36}" width="40" height="0.1" fill="none"/>')
    parts.append(f'<path d="M{x0 + 48},{y4 + 34} L{sx0},{sy - 22} M{x0 + 90},{y4 + 34} L{sx1},{sy - 22}" stroke="{MUTED}" stroke-dasharray="4 4"/>')
    for zx in (sx0, sx1):
        parts.append(f'<line x1="{zx}" y1="{sy - 10}" x2="{zx}" y2="{sy + 86}" stroke="{INK}" stroke-width="3"/>')
    mid = (sx0 + sx1) / 2
    parts.append(f'<line x1="{mid}" y1="{sy - 2}" x2="{mid}" y2="{sy + 78}" stroke="#6D28D9" stroke-width="2" stroke-dasharray="3 3"/>')
    for k in range(4):
        yy = sy + 6 + k * 22
        parts.append(f'<line x1="{sx0}" y1="{yy}" x2="{sx0 + 62}" y2="{yy}" stroke="#2563EB" stroke-width="2.5"/>')
        parts.append(f'<line x1="{sx1}" y1="{yy}" x2="{sx1 - 62}" y2="{yy}" stroke="#2563EB" stroke-width="2.5"/>')
    for k in range(3):
        yy = sy + 17 + k * 22
        parts.append(f'<line x1="{sx0 + 40}" y1="{yy}" x2="{sx1 - 40}" y2="{yy}" stroke="{RED}" stroke-width="6" stroke-linecap="round"/>')
    by = sy + 104
    parts.append(f'<path d="M{sx0 + 40},{by} L{sx1 - 40},{by}" stroke="{INK}" stroke-width="1.2"/>'
                 f'<path d="M{sx0 + 40},{by - 5} v10 M{sx1 - 40},{by - 5} v10" stroke="{INK}" stroke-width="1.2"/>')
    parts.append(text(mid, by + 18, "A 带", 13, INK, anchor="middle"))
    parts.append(f'<path d="M{sx0},{by} L{sx0 + 40},{by} M{sx1 - 40},{by} L{sx1},{by}" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3 2"/>')
    parts.append(text(sx0 + 2, by + 18, "I 带", 12, MUTED))
    parts.append(text(sx1 - 2, by + 18, "I 带", 12, MUTED, anchor="end"))
    parts.append(text(sx0 - 4, sy - 14, "Z 线", 12, INK, anchor="end"))
    parts.append(text(mid, sy - 8, "M 线", 12, "#6D28D9", anchor="middle"))
    ly = 410
    for x, c, w, t in ((470, "#2563EB", 2.5, "细肌丝（主要为肌动蛋白）"), (700, RED, 6, "粗肌丝（主要为肌球蛋白）")):
        parts.append(f'<line x1="{x}" y1="{ly}" x2="{x + 34}" y2="{ly}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>')
        parts.append(text(x + 44, ly + 5, t, 13, INK))
    parts.append(text(30, ly + 5, "教学图要点：一图一目标，层次逐级放大，标签使用标准术语。", 13, MUTED))
    parts.append(text(30, ly + 35, "参考：①② SEER 骨骼肌结构图、OpenStax A&P 2e 图 10.3；③ 图 4.18、10.4；④⑤ 图 10.5（来源表见 docs/examples/references.md）。", 12, MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


def research_svg() -> str:
    W, H = 1000, 420
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', defs(),
             f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>',
             text(30, 40, "科研示意图", 22, INK, "bold"),
             text(150, 40, "示例：抗阻训练与骨骼肌肥大（演示证据状态图例，非完整信号通路）", 15, MUTED)]
    fx, fy, fw, fh = 250, 80, 480, 250
    parts.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="40" fill="#FEF2F2" stroke="#B91C1C" stroke-width="5"/>')
    parts.append(f'<rect x="{fx + 7}" y="{fy + 7}" width="{fw - 14}" height="{fh - 14}" rx="34" fill="none" stroke="#FCA5A5" stroke-width="2"/>')
    parts.append(text(fx + fw - 24, fy + fh - 18, "骨骼肌纤维（胞质）", 13, "#991B1B", anchor="end"))
    parts.append(text(fx + 18, fy - 8, "肌膜", 13, "#991B1B"))

    def node(x, y, w, t, sub=None, fill="#FFFFFF", stroke=INK):
        h = 56 if sub else 40
        out = f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        out += text(x, y + (-4 if sub else 6), t, 15, INK, "bold", "middle")
        if sub:
            out += text(x, y + 16, sub, 12, MUTED, anchor="middle")
        return out
    load = (130, 205)
    sense = (fx + 110, 205)
    mtor = (fx + 300, 140)
    mps = (fx + 300, 265)
    hyp = (870, 265)
    rapa = (870, 140)
    parts.append(node(*load, 170, "抗阻训练", "机械负荷", "#EFF6FF", "#2563EB"))
    parts.append(node(*sense, 170, "机械感受", "具体感受器尚未明确"))
    parts.append(node(*mtor, 150, "mTORC1 激活"))
    parts.append(node(*mps, 170, "肌蛋白合成 ↑"))
    parts.append(node(*hyp, 190, "肌纤维横截面积 ↑", "肌肥大（长期训练）", "#F0FDF4", "#16A34A"))
    parts.append(node(*rapa, 150, "雷帕霉素", "实验性抑制剂", "#F5F3FF", "#6D28D9"))
    L = lambda a, b, dash=False, end="arrow": (f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{INK}" stroke-width="2.5"'
                                              f'{" stroke-dasharray=\"8 6\"" if dash else ""} marker-end="url(#{end})"/>')
    parts.append(L((load[0] + 86, 205), (sense[0] - 88, 205)))
    parts.append(L((sense[0] + 60, 182), (mtor[0] - 78, 150), dash=True))
    parts.append(L((mtor[0], 162), (mps[0], 236)))
    parts.append(L((mps[0] + 87, 265), (hyp[0] - 98, 265)))
    parts.append(L((rapa[0] - 77, 140), (mtor[0] + 80, 140), end="tee"))
    ly = 370
    items = [("arrow", False, "已证实的促进/过程"), ("arrow", True, "假说或机制未明"), ("tee", False, "抑制")]
    x = 30
    for end, dash, t in items:
        parts.append(L((x, ly), (x + 50, ly), dash=dash, end=end))
        parts.append(text(x + 62, ly + 5, t, 13, INK))
        x += 220
    parts.append(text(30, ly + 34, "来源：Drummond 2009（人体，雷帕霉素与蛋白合成）；Hornberger 2011（机械感受机制）；Joanisse 2020（蛋白合成与肥大）。关系登记见 docs/examples/。", 12, MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    (OUT / "banner.svg").write_text(banner_svg(), encoding="utf-8")
    (OUT / "squat-phases.svg").write_text(squat_svg(), encoding="utf-8")
    (OUT / "workflow.svg").write_text(workflow_svg(), encoding="utf-8")
    (OUT / "comic-example.svg").write_text(comic_svg(), encoding="utf-8")
    (OUT / "teaching-example.svg").write_text(teaching_svg(), encoding="utf-8")
    (OUT / "research-example.svg").write_text(research_svg(), encoding="utf-8")
    print("written:", ", ".join(p.name for p in sorted(OUT.glob("*.svg"))))


if __name__ == "__main__":
    main()
