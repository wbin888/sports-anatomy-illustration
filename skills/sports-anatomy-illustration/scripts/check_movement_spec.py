#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate a sports-anatomy movement spec against the bundled muscle atlas (Python 3.9+, stdlib only).

MIT License; see ../LICENSE-CODE.

Errors cover structural problems that would make a figure untraceable or self-contradictory.
Warnings flag biomechanical inconsistencies that need a source check (the atlas is simplified).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
ROLES = {"agonist", "antagonist", "synergist", "stabilizer"}
CONTRACTIONS = {"concentric", "eccentric", "isometric"}
ARROW_TYPES = {"motion", "force", "torque", "sequence"}
NUMERIC_FIELDS = ("angle_deg", "range_deg", "timing_pct", "emg_pct", "velocity", "force_n")


def load_reference():
    vocab = json.loads((DATA / "joint-actions.json").read_text(encoding="utf-8"))
    atlas = json.loads((DATA / "muscles.json").read_text(encoding="utf-8"))
    return vocab, {m["id"]: m for m in atlas["muscles"]}


def opposite(vocab, action):
    pairs = vocab["opposites"]
    if action in pairs:
        return pairs[action]
    return next((a for a, b in pairs.items() if b == action), None)


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def check(spec, vocab=None, muscles=None):
    """Return (errors, warnings) for one movement spec."""
    if vocab is None or muscles is None:
        vocab, muscles = load_reference()
    errors, warnings = [], []
    if not isinstance(spec, dict):
        return ["spec: must be a JSON object"], []

    joints = vocab["joints"]
    sources = spec.get("sources", [])
    source_ids = set()
    for index, source in enumerate(as_list(sources)):
        sid = source.get("id") if isinstance(source, dict) else None
        if not sid:
            errors.append(f"sources[{index}]: missing id")
            continue
        if sid in source_ids:
            errors.append(f"sources[{index}]: duplicate id {sid}")
        source_ids.add(sid)
        if not source.get("citation") or not source.get("checked_scope"):
            errors.append(f"source {sid}: citation and checked_scope are required")

    def check_refs(where, item):
        refs = item.get("source_ids", [])
        if not isinstance(refs, list):
            errors.append(f"{where}: source_ids must be a list")
            return []
        for ref in refs:
            if ref not in source_ids:
                errors.append(f"{where}: unknown source {ref}")
        for field in NUMERIC_FIELDS:
            if item.get(field) is not None and not refs:
                errors.append(f"{where}: {field} requires source_ids")
        return refs

    planes = set(as_list((spec.get("view") or {}).get("plane")))
    for plane in planes:
        if plane not in vocab["planes"]:
            errors.append(f"view: unknown plane {plane}")

    phases = spec.get("phases")
    if not isinstance(phases, list) or not phases:
        errors.append("phases: at least one phase is required")
        return errors, warnings

    phase_ids = set()
    for p_index, phase in enumerate(phases):
        if not isinstance(phase, dict):
            errors.append(f"phases[{p_index}]: must be an object")
            continue
        pid = phase.get("id") or f"phases[{p_index}]"
        if not phase.get("id"):
            errors.append(f"{pid}: missing id")
        elif pid in phase_ids:
            errors.append(f"{pid}: duplicate phase id")
        phase_ids.add(pid)

        moving = set()
        for j_index, item in enumerate(as_list(phase.get("joint_actions"))):
            where = f"{pid}.joint_actions[{j_index}]"
            joint, action = item.get("joint"), item.get("action")
            if joint not in joints:
                errors.append(f"{where}: unknown joint {joint}")
                continue
            if action not in joints[joint]:
                errors.append(f"{where}: {joint} has no action {action}")
                continue
            moving.add(f"{joint}:{action}")
            check_refs(where, item)
            plane = vocab["action_plane"].get(action)
            if planes and plane and plane not in planes:
                warnings.append(f"{where}: {joint}:{action} occurs in the {plane} plane, not shown by view {sorted(planes)}")

        for m_index, item in enumerate(as_list(phase.get("muscles"))):
            where = f"{pid}.muscles[{m_index}]"
            mid, role, contraction = item.get("muscle"), item.get("role"), item.get("contraction")
            if mid not in muscles:
                errors.append(f"{where}: unknown muscle {mid}")
                continue
            if role not in ROLES:
                errors.append(f"{where}: invalid role {role}")
            if contraction not in CONTRACTIONS:
                errors.append(f"{where}: invalid contraction {contraction}")
            check_refs(where, item)
            controls = item.get("controls")
            if role in ("agonist", "antagonist") and not controls and contraction != "isometric":
                errors.append(f"{where}: {role} {mid} needs controls (joint:action)")
            if not controls:
                continue
            if controls not in moving:
                errors.append(f"{where}: controls {controls} is not a joint action of phase {pid}")
                continue
            joint, action = controls.split(":", 1)
            known = set(muscles[mid]["actions"])
            on_joint = {a for a in known if a.startswith(joint + ":")}
            if not on_joint:
                warnings.append(f"{where}: atlas lists no {joint} action for {mid}; verify with a source")
                continue
            reverse = opposite(vocab, action)
            if contraction == "concentric" and controls not in known:
                warnings.append(f"{where}: concentric {mid} does not produce {controls} in the atlas")
            if contraction == "eccentric" and f"{joint}:{reverse}" not in known:
                warnings.append(f"{where}: eccentric {mid} should resist {controls} by producing {joint}:{reverse}")

        for a_index, arrow in enumerate(as_list(phase.get("arrows"))):
            where = f"{pid}.arrows[{a_index}]"
            if arrow.get("type") not in ARROW_TYPES:
                errors.append(f"{where}: invalid type {arrow.get('type')}")
            refs = check_refs(where, arrow)
            if arrow.get("type") in ("force", "torque") and not refs:
                errors.append(f"{where}: {arrow.get('type')} arrows require source_ids")
    return errors, warnings


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="校验运动解剖动作规格（movement spec）与随包肌肉图谱的一致性。")
    parser.add_argument("spec", nargs="*", type=Path, help="movement-spec JSON 文件；不填则校验随包 data/movements.json")
    parser.add_argument("--strict", action="store_true", help="将警告视为错误")
    args = parser.parse_args(argv)
    vocab, muscles = load_reference()

    specs = []
    if args.spec:
        for path in args.spec:
            try:
                specs.append((str(path), json.loads(path.read_text(encoding="utf-8"))))
            except (OSError, ValueError) as error:
                print(f"{path}: 无法读取 JSON: {error}", file=sys.stderr)
                return 1
    else:
        bundled = json.loads((DATA / "movements.json").read_text(encoding="utf-8"))
        specs = [(f"movements.json#{m['id']}", m) for m in bundled["movements"]]

    failed = False
    for name, spec in specs:
        errors, warnings = check(spec, vocab, muscles)
        for message in errors:
            print(f"ERROR {name}: {message}")
        for message in warnings:
            print(f"WARN  {name}: {message}")
        if errors or (args.strict and warnings):
            failed = True
        elif not warnings:
            print(f"OK    {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
