"""The decision rule of the evaluation protocol, checked at its boundaries."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))

from decision_rule import STATEMENTS, conditions, decide, marking_verdict  # noqa: E402


def cases(pairs, strata=None):
    """Ten cases by default: six health, four other fields, like the held-out set."""
    strata = strata or ["health"] * 6 + ["other fields"] * 4
    return [{"case": "c%02d" % i, "stratum": strata[i], "with": w, "without": b} for i, (w, b) in enumerate(pairs)]


def test_no_cases_gives_no_verdict():
    assert decide([]) is None
    assert decide([{"case": "a", "stratum": "health", "with": 0.5, "without": None}]) is None


def test_beats_needs_margin_seven_cases_and_no_lower_stratum():
    result = decide(cases([(0.9, 0.8)] * 7 + [(0.8, 0.8)] * 3))
    assert result["verdict"] == "beats"
    assert result["better"] == 7 and result["same"] == 3 and result["worse"] == 0
    assert abs(result["mean_diff"] - 0.07) < 1e-9
    assert result["statement"] == STATEMENTS["beats"]


def test_large_gain_on_six_cases_only_is_mixed():
    result = decide(cases([(1.0, 0.8)] * 6 + [(0.8, 0.8)] * 4))
    assert result["mean_diff"] > 0.05
    assert result["better"] == 6 and result["needed_better"] == 7
    assert result["verdict"] == "mixed"


def test_gain_with_a_lower_stratum_is_mixed():
    # health gains a lot on every case, other fields lose a little on one case
    pairs = [(1.0, 0.7)] * 6 + [(0.80, 0.82)] + [(0.9, 0.8)] * 3
    result = decide(cases(pairs))
    assert result["verdict"] == "beats"          # other fields still higher on average
    pairs = [(1.0, 0.7)] * 6 + [(0.70, 0.90)] + [(0.81, 0.80)] * 3
    result = decide(cases(pairs))
    assert result["better"] >= 7 and result["mean_diff"] >= 0.05
    assert result["lower_in_a_stratum"] is True
    assert result["verdict"] == "mixed"


def test_small_difference_either_way_is_level():
    assert decide(cases([(0.84, 0.80)] * 10))["verdict"] == "level"
    assert decide(cases([(0.80, 0.84)] * 10))["verdict"] == "level"
    assert decide(cases([(0.80, 0.80)] * 10))["verdict"] == "level"


def test_exactly_five_points_is_not_level():
    up = decide(cases([(0.85, 0.80)] * 10))
    assert up["verdict"] == "beats"
    down = decide(cases([(0.80, 0.85)] * 10))
    assert down["verdict"] == "worse"


def test_worse():
    result = decide(cases([(0.6, 0.8)] * 5 + [(0.8, 0.8)] * 5))
    assert result["verdict"] == "worse"
    assert result["worse"] == 5


def test_other_arm_and_strata_summary():
    rows = [{"case": "a", "stratum": "health", "with": 0.9, "without": 0.9, "prompted": 0.7},
            {"case": "b", "stratum": "other fields", "with": 0.8, "without": 0.9, "prompted": 0.7},
            {"case": "c", "stratum": "other fields", "with": 0.8, "without": 0.7}]
    against_prompted = decide(rows, "prompted")
    assert against_prompted["n"] == 2 and against_prompted["against"] == "prompted"
    assert abs(against_prompted["mean_diff"] - 0.15) < 1e-9
    main = decide(rows)
    assert main["n"] == 3
    assert abs(main["by_stratum"]["other fields"]["diff"]) < 1e-9
    assert main["by_stratum"]["health"]["n"] == 1


def test_needed_cases_scales_with_the_number_of_cases():
    assert decide(cases([(0.9, 0.8)] * 4, ["health"] * 4))["needed_better"] == 3
    assert decide(cases([(0.9, 0.8)] * 3, ["health"] * 3))["needed_better"] == 3
    assert decide(cases([(0.9, 0.8)] * 10))["needed_better"] == 7


def test_a_case_scored_in_one_arm_only_makes_the_comparison_incomplete():
    rows = cases([(0.9, 0.8)] * 9) + [{"case": "c09", "stratum": "other fields", "with": 0.9, "without": None}]
    result = decide(rows)
    assert result["verdict"] == "incomplete"
    assert result["one_sided_cases"] == ["c09"]
    assert result["statement"] == STATEMENTS["incomplete"]
    # a case absent from both arms of this comparison is simply not part of it
    rows = cases([(0.9, 0.8)] * 9) + [{"case": "c09", "stratum": "other fields", "with": None, "without": None}]
    assert decide(rows)["verdict"] == "beats"


def test_marking_verdict():
    key, sentence = marking_verdict({"today": {"correct": 0.95, "n": 40}, "memory": {"correct": 0.80, "n": 10}})
    assert key == "informative" and "95% of 40" in sentence and "80% of 10" in sentence
    key, sentence = marking_verdict({"today": {"correct": 0.80, "n": 40}, "memory": {"correct": 0.80, "n": 10}})
    assert key == "decoration" and "decoration" in sentence
    key, sentence = marking_verdict({"today": {"correct": 0.70, "n": 40}, "memory": {"correct": 0.90, "n": 10}})
    assert key == "decoration"
    key, sentence = marking_verdict({"today": {"correct": 0.9, "n": 40}, "memory": {"correct": None, "n": 0}})
    assert key == "not assessable" and "40" in sentence
    assert marking_verdict(None)[0] == "not assessable"


def test_conditions_sentence_names_what_was_met():
    text = conditions(decide(cases([(1.0, 0.8)] * 6 + [(0.8, 0.8)] * 4)))
    assert "a mean gain of 5 points or more, met (+12.0)" in text
    assert "at least 7 of the 10 questions, not met (6)" in text
    assert "no stratum lower, met" in text
    assert conditions(None) == ""


def test_marking_verdict_prints_counts_when_the_audit_gives_them():
    key, sentence = marking_verdict({"today": {"correct": 0.975, "n": 40, "right": 39},
                                     "memory": {"correct": 26 / 30, "n": 30, "right": 26}})
    assert key == "informative"
    assert "39 of 40 statements marked as checked today were right, against 26 of 30 marked as recalled" in sentence
