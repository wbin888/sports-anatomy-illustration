#!/usr/bin/env python3
"""Movement spec validation tests. MIT; see ../LICENSE."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "skills/sports-anatomy-illustration"
spec = importlib.util.spec_from_file_location("movement", SKILL / "scripts/check_movement_spec.py")
movement = importlib.util.module_from_spec(spec)
spec.loader.exec_module(movement)
EXAMPLE = json.loads((SKILL / "assets/movement-spec.example.json").read_text(encoding="utf-8"))


def phase(data):
    return data["phases"][0]


class MovementSpecTests(unittest.TestCase):
    def check(self, data):
        return movement.check(data)

    def test_bundled_templates_and_example_are_clean(self):
        bundled = json.loads((SKILL / "data/movements.json").read_text(encoding="utf-8"))
        for item in bundled["movements"] + [EXAMPLE]:
            with self.subTest(item=item.get("id", "example")):
                self.assertEqual(self.check(item), ([], []))

    def test_atlas_actions_use_known_vocabulary(self):
        vocab, muscles = movement.load_reference()
        for mid, muscle in muscles.items():
            for item in muscle["actions"]:
                joint, action = item.split(":")
                self.assertIn(action, vocab["joints"][joint], f"{mid}: {item}")

    def test_unknown_muscle_and_joint_action_are_errors(self):
        data = copy.deepcopy(EXAMPLE)
        phase(data)["muscles"][0]["muscle"] = "biceps_glutealis"
        phase(data)["joint_actions"].append({"joint": "knee", "action": "abduction"})
        errors, _ = self.check(data)
        self.assertTrue(any("unknown muscle" in e for e in errors))
        self.assertTrue(any("knee has no action abduction" in e for e in errors))

    def test_numbers_and_force_arrows_need_sources(self):
        data = copy.deepcopy(EXAMPLE)
        phase(data)["joint_actions"][0]["angle_deg"] = 90
        phase(data)["arrows"][1]["source_ids"] = []
        errors, _ = self.check(data)
        self.assertIn("ascent.joint_actions[0]: angle_deg requires source_ids", errors)
        self.assertIn("ascent.arrows[1]: force arrows require source_ids", errors)

    def test_controls_must_match_phase_motion(self):
        data = copy.deepcopy(EXAMPLE)
        phase(data)["muscles"][0]["controls"] = "hip:flexion"
        errors, _ = self.check(data)
        self.assertTrue(any("not a joint action of phase" in e for e in errors))

    def test_wrong_contraction_direction_warns(self):
        data = copy.deepcopy(EXAMPLE)
        phase(data)["muscles"][0]["contraction"] = "eccentric"
        _, warnings = self.check(data)
        self.assertTrue(any("eccentric gluteus_maximus should resist hip:extension" in w for w in warnings))

    def test_action_outside_view_plane_warns(self):
        data = copy.deepcopy(EXAMPLE)
        phase(data)["joint_actions"].append({"joint": "hip", "action": "adduction"})
        _, warnings = self.check(data)
        self.assertTrue(any("frontal plane" in w for w in warnings))

    def test_cli_strict_fails_on_warning(self):
        import io, contextlib, tempfile
        data = copy.deepcopy(EXAMPLE)
        phase(data)["joint_actions"].append({"joint": "hip", "action": "adduction"})
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spec.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(movement.main([str(path)]), 0)
                self.assertEqual(movement.main([str(path), "--strict"]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
