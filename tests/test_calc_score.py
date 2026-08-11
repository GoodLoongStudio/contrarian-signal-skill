import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "calc_score.py"
spec = importlib.util.spec_from_file_location("calc_score", MODULE_PATH)
calc_score = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(calc_score)


class CalculateScoreTests(unittest.TestCase):
    def test_basic_score_excludes_flat_and_unverifiable(self):
        calls = [
            {"outcome": "CONTRARIAN_HIT"},
            {"outcome": "CONTRARIAN_HIT"},
            {"outcome": "ORIGINAL_CORRECT"},
            {"outcome": "FLAT"},
            {"outcome": "UNVERIFIABLE"},
        ]
        result = calc_score.calculate(calls)
        self.assertEqual(result["scored_calls"], 3)
        self.assertEqual(result["contrarian_score"], 66.7)
        self.assertEqual(result["original_accuracy"], 33.3)

    def test_score_is_not_modified_by_sample_strength(self):
        calls = [{"outcome": "CONTRARIAN_HIT"}] * 8 + [
            {"outcome": "ORIGINAL_CORRECT"}
        ] * 2
        result = calc_score.calculate(calls)
        self.assertEqual(result["contrarian_score"], 80.0)
        self.assertEqual(result["sample_strength"], "LOW")

    def test_no_scored_calls_returns_null_score(self):
        calls = [
            {"outcome": "FLAT"},
            {"outcome": "UNSCORABLE"},
            {"outcome": "UNVERIFIABLE"},
        ]
        result = calc_score.calculate(calls)
        self.assertEqual(result["scored_calls"], 0)
        self.assertIsNone(result["contrarian_score"])
        self.assertEqual(result["sample_strength"], "INSUFFICIENT")

    def test_invalid_outcome_raises(self):
        with self.assertRaises(ValueError):
            calc_score.calculate([{"outcome": "MAYBE"}])


if __name__ == "__main__":
    unittest.main()
