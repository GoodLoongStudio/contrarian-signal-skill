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


if __name__ == "__main__":
    unittest.main()
