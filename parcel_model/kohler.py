# kohler.py
# Simple kappa-Kohler critical supersaturation approximation

import math
from constants import R, Mw, rho_w

def critical_supersaturation(Dp, kappa, sigma=0.072, T=298.15):
    """
    Approximate critical supersaturation (dimensionless, e.g. 0.001 = 0.1%)
    Dp : dry particle diameter (m)
    kappa : hygroscopicity parameter
    sigma : surface tension of water (N/m)
    T : temperature (K)
    """
    if kappa <= 0:
        return float("inf")
    A = (4.0 * sigma * Mw) / (R * T * rho_w)
    Sc = (4.0 * A**3) / (27.0 * (Dp**3) * kappa)
    return Sc
