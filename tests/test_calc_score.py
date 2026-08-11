import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "calc_score.py"
spec = importlib.util.spec_from_file_location("calc_score", MODULE_PATH)
calc_score = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(calc_score)


class CalculateScoreTests(unittest.TestCase):
    def test_raw_score_excludes_flat_and_unverifiable(self):
        calls = [
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 95},
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 75},
            {"outcome": "ORIGINAL_CORRECT", "opinion_confidence": 55},
            {"outcome": "FLAT", "opinion_confidence": 95},
            {"outcome": "UNVERIFIABLE", "opinion_confidence": 35},
        ]
        result = calc_score.calculate(calls)
        self.assertEqual(result["raw"]["scored_calls"], 3)
        self.assertEqual(result["raw"]["contrarian_score"], 66.7)
        self.assertEqual(result["raw"]["original_accuracy"], 33.3)

    def test_confidence_buckets_are_independent(self):
        calls = [
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 99},
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 90},
            {"outcome": "ORIGINAL_CORRECT", "opinion_confidence": 95},
            {"outcome": "ORIGINAL_CORRECT", "opinion_confidence": 80},
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 75},
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 52},
            {"outcome": "ORIGINAL_CORRECT", "opinion_confidence": 31},
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 18},
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 5},
        ]
        result = calc_score.calculate(calls)
        buckets = {item["range"]: item for item in result["confidence_buckets"]}

        self.assertEqual(buckets["90-100"]["contrarian_score"], 66.7)
        self.assertEqual(buckets["70-89"]["contrarian_score"], 50.0)
        self.assertEqual(buckets["50-69"]["contrarian_score"], 100.0)
        self.assertEqual(buckets["30-49"]["contrarian_score"], 0.0)
        self.assertEqual(buckets["10-29"]["contrarian_score"], 100.0)
        self.assertEqual(buckets["0-9"]["contrarian_score"], 100.0)

    def test_raw_score_does_not_require_confidence(self):
        calls = [
            {"outcome": "CONTRARIAN_HIT"},
            {"outcome": "ORIGINAL_CORRECT"},
            {"outcome": "CONTRARIAN_HIT", "opinion_confidence": 95},
        ]
        result = calc_score.calculate(calls)
        self.assertEqual(result["raw"]["contrarian_score"], 66.7)
        self.assertEqual(result["confidence_missing_calls"], 2)
        buckets = {item["range"]: item for item in result["confidence_buckets"]}
        self.assertEqual(buckets["90-100"]["scored_calls"], 1)
        self.assertEqual(buckets["90-100"]["contrarian_score"], 100.0)

    def test_score_is_not_modified_by_sample_strength(self):
        calls = [{"outcome": "CONTRARIAN_HIT", "opinion_confidence": 95}] * 8 + [
            {"outcome": "ORIGINAL_CORRECT", "opinion_confidence": 95}
        ] * 2
        result = calc_score.calculate(calls)
        self.assertEqual(result["raw"]["contrarian_score"], 80.0)
        self.assertEqual(result["raw"]["sample_strength"], "LOW")
        bucket = result["confidence_buckets"][0]
        self.assertEqual(bucket["contrarian_score"], 80.0)

    def test_no_scored_calls_returns_null_score(self):
        calls = [
            {"outcome": "FLAT", "opinion_confidence": 95},
            {"outcome": "UNSCORABLE"},
            {"outcome": "UNVERIFIABLE", "opinion_confidence": 55},
        ]
        result = calc_score.calculate(calls)
        self.assertEqual(result["raw"]["scored_calls"], 0)
        self.assertIsNone(result["raw"]["contrarian_score"])
        self.assertEqual(result["raw"]["sample_strength"], "INSUFFICIENT")

    def test_invalid_outcome_raises(self):
        with self.assertRaises(ValueError):
            calc_score.calculate([{"outcome": "MAYBE", "opinion_confidence": 90}])

    def test_invalid_confidence_raises(self):
        with self.assertRaises(ValueError):
            calc_score.calculate([{"outcome": "CONTRARIAN_HIT", "opinion_confidence": 101}])
        with self.assertRaises(ValueError):
            calc_score.calculate([{"outcome": "CONTRARIAN_HIT", "opinion_confidence": "high"}])


if __name__ == "__main__":
    unittest.main()
