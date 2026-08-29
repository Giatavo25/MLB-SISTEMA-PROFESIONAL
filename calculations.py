"""
Cálculos estadísticos: distribución de Poisson para carreras,
conversión de cuotas americanas y detección de valor (edge).
"""
import math


def poisson_pmf(lam, k):
    return math.exp(-lam) * lam ** k / math.factorial(k)


def combined_over_under(lam_home, lam_away, line, max_runs=40):
    """Probabilidad de over/under en el total combinado de carreras."""
    total_lambda = lam_home + lam_away
    floor_line = math.floor(line)
    p_under_or_equal = sum(
        poisson_pmf(total_lambda, k) for k in range(0, floor_line + 1)
    )
    p_over = 1 - p_under_or_equal
    return {
        "expected_total": round(total_lambda, 2),
        "p_over": round(p_over, 4),
        "p_under": round(p_under_or_equal, 4),
    }


def team_over_under(lam_team, line):
    """Probabilidad de over/under en el total de carreras de UN equipo."""
    floor_line = math.floor(line)
    p_under_or_equal = sum(poisson_pmf(lam_team, k) for k in range(0, floor_line + 1))
    p_over = 1 - p_under_or_equal
    return {"p_over": round(p_over, 4), "p_under": round(p_under_or_equal, 4)}


def american_to_implied(odds):
    odds = float(odds)
    if odds > 0:
        return 100 / (odds + 100)
    return -odds / (-odds + 100)


def remove_vig(prob_a, prob_b):
    """Quita el margen de la casa (vig) de un mercado a dos vías."""
    overround = prob_a + prob_b
    return prob_a / overround, prob_b / overround


def edge(my_prob, fair_prob):
    """Diferencia en puntos porcentuales entre tu estimación y el mercado."""
    return round((my_prob - fair_prob) * 100, 2)
