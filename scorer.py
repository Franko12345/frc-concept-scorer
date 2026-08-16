"""Pure scoring logic — shared between Flask backend and JS port.

Tests live in test_scorer.py. Keep this module dependency-free so it
can be re-implemented identically in static/app.js.
"""
WEIGHTS = {"pontos_potenciais": 1.0, "complexidade": 1.0, "risco": 1.0, "recursos": 1.0}
INVERTED = {"pontos_potenciais": False, "complexidade": True, "risco": True, "recursos": True}


def score_concept(concept: dict, weights: dict) -> float:
    """Weighted score 0-10. Higher = better.

    'complexidade', 'risco', 'recursos' are inverted (LOWER raw value = BETTER).
    """
    total = 0.0
    wsum = 0.0
    for key, raw in concept["scores"].items():
        v = float(raw)
        if INVERTED.get(key, False):
            v = 10 - v
        w = float(weights.get(key, 1.0))
        total += v * w
        wsum += w
    return round(total / wsum, 2) if wsum else 0.0
