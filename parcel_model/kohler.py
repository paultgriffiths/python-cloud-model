# kohler.py

import math
from parcel_model.constants import R, Mw, rho_w

def critical_supersaturation(Dp, kappa, sigma=0.072, T=298.15):
    """
    Kappa-Kohler critical supersaturation.
    """
    if kappa <= 0:
        return float("inf")

    A = (4.0 * sigma * Mw) / (R * T * rho_w)
    Sc = math.sqrt((4.0 * A**3) / (27.0 * (Dp**3) * kappa))
    return Sc


def critical_supersaturation_classical(Dp, solubility_factor=1.0, sigma=0.072, T=298.15):
    """
    Simple classical Kohler-like critical supersaturation approximation.

    This is a simplified comparison function for sensitivity testing,
    not a full solute-resolved Kohler model.
    """
    A = (4.0 * sigma * Mw) / (R * T * rho_w)

    # Effective Raoult/solute term.
    B = solubility_factor * Dp**3

    if B <= 0:
        return float("inf")

    Sc = math.sqrt((4.0 * A**3) / (27.0 * B))
    return Sc
