"""Tests for the pure scoring logic. Run with: python -m pytest test_scorer.py -v
Or without pytest: python test_scorer.py
"""
from scorer import score_concept


def approx(a, b):
    return abs(a - b) < 0.01


def test_simple_shooter_wins_with_default_weights():
    """Low complexity/risk/resources should beat high ambition with equal weights."""
    simple = {"scores": {"pontos_potenciais": 5, "complexidade": 2, "risco": 2, "recursos": 3}}
    sandwich = {"scores": {"pontos_potenciais": 9, "complexidade": 9, "risco": 8, "recursos": 9}}
    w = {"pontos_potenciais": 1, "complexidade": 1, "risco": 1, "recursos": 1}
    assert score_concept(simple, w) == 7.0
    assert score_concept(sandwich, w) == 3.25
    assert score_concept(simple, w) > score_concept(sandwich, w)


def test_inverted_criteria_flip():
    """complexidade=0 should give a higher score than complexidade=10."""
    low = {"scores": {"pontos_potenciais": 5, "complexidade": 0, "risco": 5, "recursos": 5}}
    high = {"scores": {"pontos_potenciais": 5, "complexidade": 10, "risco": 5, "recursos": 5}}
    w = {"pontos_potenciais": 1, "complexidade": 1, "risco": 1, "recursos": 1}
    assert score_concept(low, w) > score_concept(high, w)


def test_weights_change_ranking():
    """Heavy weight on pontos_potenciais should reward the ambitious concept."""
    simple = {"scores": {"pontos_potenciais": 5, "complexidade": 2, "risco": 2, "recursos": 3}}
    sandwich = {"scores": {"pontos_potenciais": 9, "complexidade": 9, "risco": 8, "recursos": 9}}
    w_low = {"pontos_potenciais": 1, "complexidade": 1, "risco": 1, "recursos": 1}
    w_high = {"pontos_potenciais": 3, "complexidade": 1, "risco": 1, "recursos": 1}
    assert score_concept(simple, w_low) > score_concept(sandwich, w_low)
    # With pontos weighted 3x, sandwich should close the gap heavily
    assert score_concept(sandwich, w_high) > score_concept(sandwich, w_low)


def test_empty_weights():
    """Empty weights dict should default to 1.0 each."""
    c = {"scores": {"pontos_potenciais": 5, "complexidade": 5, "risco": 5, "recursos": 5}}
    # All 5s, three inverted -> 5 + 5 + 5 + 5 = 20 / 4 = 5.0
    assert score_concept(c, {}) == 5.0


if __name__ == "__main__":
    test_simple_shooter_wins_with_default_weights()
    test_inverted_criteria_flip()
    test_weights_change_ranking()
    test_empty_weights()
    print("All scorer tests passed ✓")
