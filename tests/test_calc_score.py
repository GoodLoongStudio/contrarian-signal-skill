import importlib.util
import pathlib
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "calc_score.py"
spec = importlib.util.spec_from_file_location("calc_score", MODULE_PATH)
calc_score = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(calc_score)


class CalculateScoreTests(unittest.TestCase):
    def test_raw_score_and_event_type_split(self):
        calls = [
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 95, "event_type": "ACTION", "attribution": "TARGET"},
            {"outcome": "ORIGINAL_CORRECT", "opinion_confidence": 95, "event_type": "ACTION", "attribution": "TARGET"},
            {"outcome": "ORIGINAL_CORRECT", "opinion_confidence": 75, "event_type": "OPINION", "attribution": "TARGET"},
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 55, "event_type": "OPINION", "attribution": "TARGET"},
        ]
        result = calc_score.calculate(calls)
        self.assertEqual(result["raw"]["contrarian_score"], 50.0)
        self.assertEqual(result["by_event_type"]["ACTION"]["contrarian_score"], 50.0)
        self.assertEqual(result["by_event_type"]["OPINION"]["contrarian_score"], 50.0)

    def test_action_and_opinion_can_diverge(self):
        calls = [
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 99, "event_type": "ACTION", "attribution": "TARGET"},
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 92, "event_type": "ACTION", "attribution": "TARGET"},
            {"outcome": "ORIGINAL_CORRECT", "opinion_confidence": 80, "event_type": "OPINION", "attribution": "TARGET"},
            {"outcome": "ORIGINAL_CORRECT", "opinion_confidence": 75, "event_type": "OPINION", "attribution": "TARGET"},
        ]
        result = calc_score.calculate(calls)
        self.assertEqual(result["by_event_type"]["ACTION"]["contrarian_score"], 100.0)
        self.assertEqual(result["by_event_type"]["OPINION"]["contrarian_score"], 0.0)
        self.assertEqual(result["raw"]["contrarian_score"], 50.0)

    def test_confidence_buckets_inside_event_type(self):
        calls = [
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 95, "event_type": "ACTION", "attribution": "TARGET"},
            {"outcome": "ORIGINAL_CORRECT", "opinion_confidence": 75, "event_type": "ACTION", "attribution": "TARGET"},
            {"outcome": "ORIGINAL_CORRECT", "opinion_confidence": 95, "event_type": "OPINION", "attribution": "TARGET"},
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 75, "event_type": "OPINION", "attribution": "TARGET"},
        ]
        result = calc_score.calculate(calls)
        action = {x["range"]: x for x in result["confidence_buckets_by_event_type"]["ACTION"]}
        opinion = {x["range"]: x for x in result["confidence_buckets_by_event_type"]["OPINION"]}
        self.assertEqual(action["90-100"]["contrarian_score"], 100.0)
        self.assertEqual(action["70-89"]["contrarian_score"], 0.0)
        self.assertEqual(opinion["90-100"]["contrarian_score"], 0.0)
        self.assertEqual(opinion["70-89"]["contrarian_score"], 100.0)

    def test_style_tags_are_conditioned_independently(self):
        calls = [
            {"outcome": "ORIGINAL_CORRECT", "event_type": "OPINION", "attribution": "TARGET", "style_tags": ["thesis", "long-horizon"]},
            {"outcome": "ORIGINAL_CORRECT", "event_type": "OPINION", "attribution": "TARGET", "style_tags": ["THESIS"]},
            {"outcome": "CONTRARIAN_HIT", "event_type": "ACTION", "attribution": "TARGET", "style_tags": ["breakout chase", "HIGH_CONVICTION"]},
            {"outcome": "CONTRARIAN_HIT", "event_type": "ACTION", "attribution": "TARGET", "style_tags": ["BREAKOUT_CHASE"]},
        ]
        result = calc_score.calculate(calls)
        self.assertEqual(result["by_style_tag"]["THESIS"]["contrarian_score"], 0.0)
        self.assertEqual(result["by_style_tag"]["BREAKOUT_CHASE"]["contrarian_score"], 100.0)
        self.assertEqual(result["by_style_tag_and_event_type"]["OPINION"]["THESIS"]["scored_calls"], 2)
        self.assertEqual(result["by_style_tag_and_event_type"]["ACTION"]["BREAKOUT_CHASE"]["scored_calls"], 2)

    def test_style_adjustment_shrinks_toward_neutral(self):
        calls = [
            {"outcome": "CONTRARIAN_HIT", "event_type": "ACTION", "attribution": "TARGET"},
            {"outcome": "CONTRARIAN_HIT", "event_type": "ACTION", "attribution": "TARGET"},
            {"outcome": "CONTRARIAN_HIT", "event_type": "OPINION", "attribution": "TARGET"},
            {"outcome": "ORIGINAL_CORRECT", "event_type": "OPINION", "attribution": "TARGET"},
        ]
        profile = {
            "primary_archetype": "MIXED",
            "style_transferability_components": {
                "horizon_consistency": 50,
                "action_opinion_consistency": 50,
                "regime_stability": 50,
                "directional_persistence": 50,
                "corpus_representativeness": 50,
            },
        }
        result = calc_score.calculate(calls, profile)
        self.assertEqual(result["style_profile"]["style_transferability"], 50.0)
        # RAW empirical = 75; shrink halfway toward 50 => 62.5
        self.assertEqual(result["style_adjusted"]["RAW"]["style_adjusted_contrarian_score"], 62.5)
        # ACTION empirical = 100; halfway => 75
        self.assertEqual(result["style_adjusted"]["ACTION"]["style_adjusted_contrarian_score"], 75.0)
        # OPINION empirical = 50; remains neutral
        self.assertEqual(result["style_adjusted"]["OPINION"]["style_adjusted_contrarian_score"], 50.0)

    def test_incomplete_style_profile_does_not_guess_adjusted_score(self):
        calls = [{"outcome": "CONTRARIAN_HIT", "event_type": "ACTION", "attribution": "TARGET"}]
        profile = {
            "style_transferability_components": {
                "horizon_consistency": 80,
                "action_opinion_consistency": 70,
            }
        }
        result = calc_score.calculate(calls, profile)
        self.assertIsNone(result["style_profile"]["style_transferability"])
        self.assertIsNone(result["style_adjusted"]["RAW"])
        self.assertIn("regime_stability", result["style_profile"]["style_transferability_missing_components"])

    def test_third_party_cannot_enter_target_score(self):
        with self.assertRaises(ValueError):
            calc_score.calculate([{"outcome": "CONTRARIAN_HIT", "event_type": "ACTION", "attribution": "THIRD_PARTY"}])
        with self.assertRaises(ValueError):
            calc_score.calculate([{"outcome": "ORIGINAL_CORRECT", "event_type": "OPINION", "attribution": "UNCERTAIN"}])

    def test_unscorable_third_party_is_allowed_for_audit(self):
        result = calc_score.calculate([
            {"outcome": "UNSCORABLE", "event_type": "OPINION", "attribution": "THIRD_PARTY", "opinion_confidence": 80}
        ])
        self.assertEqual(result["raw"]["scored_calls"], 0)
        self.assertEqual(result["counts"]["UNSCORABLE"], 1)

    def test_legacy_missing_event_type_goes_to_unknown(self):
        result = calc_score.calculate([{"outcome": "CONTRARIAN_HIT", "opinion_confidence": 95}])
        self.assertEqual(result["event_type_missing_calls"], 1)
        self.assertEqual(result["by_event_type"]["UNKNOWN"]["scored_calls"], 1)
        self.assertEqual(result["raw"]["contrarian_score"], 100.0)

    def test_raw_excludes_flat_and_unverifiable(self):
        calls = [
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 95, "event_type": "ACTION", "attribution": "TARGET"},
            {"outcome": "ORIGINAL_CORRECT", "opinion_confidence": 55, "event_type": "OPINION", "attribution": "TARGET"},
            {"outcome": "FLAT", "opinion_confidence": 95, "event_type": "ACTION", "attribution": "TARGET"},
            {"outcome": "UNVERIFIABLE", "opinion_confidence": 35, "event_type": "OPINION", "attribution": "TARGET"},
        ]
        result = calc_score.calculate(calls)
        self.assertEqual(result["raw"]["scored_calls"], 2)
        self.assertEqual(result["raw"]["contrarian_score"], 50.0)

    def test_invalid_fields_raise(self):
        with self.assertRaises(ValueError):
            calc_score.calculate([{"outcome": "MAYBE"}])
        with self.assertRaises(ValueError):
            calc_score.calculate([{"outcome": "CONTRARIAN_HIT", "event_type": "TRADE"}])
        with self.assertRaises(ValueError):
            calc_score.calculate([{"outcome": "CONTRARIAN_HIT", "opinion_confidence": 101}])
        with self.assertRaises(ValueError):
            calc_score.calculate([{"outcome": "CONTRARIAN_HIT", "opinion_confidence": "high"}])
        with self.assertRaises(ValueError):
            calc_score.calculate([{"outcome": "CONTRARIAN_HIT", "style_tags": "THESIS"}])
        with self.assertRaises(ValueError):
            calc_score.calculate(
                [{"outcome": "CONTRARIAN_HIT"}],
                {"style_transferability_components": {
                    "horizon_consistency": 120,
                    "action_opinion_consistency": 50,
                    "regime_stability": 50,
                    "directional_persistence": 50,
                    "corpus_representativeness": 50,
                }},
            )


if __name__ == "__main__":
    unittest.main()
