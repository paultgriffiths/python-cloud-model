# thermodynamics.py
# -----------------
# Drop-in replacement with separate saturation formulations over water and ice,
# plus convenience supersaturation functions Sw and Si.

import numpy as np


def esat_water(T: float) -> float:
    """
    Saturation vapour pressure over liquid water, e_sw(T) [Pa].
    T in Kelvin.

    Uses a common Bolton (1980)-style approximation.
    """
    Tc = T - 273.15  # Celsius
    return 611.2 * np.exp((17.67 * Tc) / (Tc + 243.5))


def esat_ice(T: float) -> float:
    """
    Saturation vapour pressure over ice, e_si(T) [Pa].
    T in Kelvin.

    Murphy & Koop (2005)-type fit (widely used for mixed-phase work).
    """
    return float(np.exp(
        9.550426
        - (5723.265 / T)
        + 3.53068 * np.log(T)
        - 0.00728332 * T
    ))


def Sw(e: float, T: float) -> float:
    """
    Supersaturation with respect to liquid water (dimensionless).
    Sw = (e - e_sw) / e_sw
    """
    ew = esat_water(T)
    return (e - ew) / ew


def Si(e: float, T: float) -> float:
    """
    Supersaturation with respect to ice (dimensionless).
    Si = (e - e_si) / e_si
    """
    ei = esat_ice(T)
    return (e - ei) / ei


def supersaturation(e: float, es: float) -> float:
    """
    Backwards-compatible helper: if the rest of your code calls
    supersaturation(e, esat_water(T)), this keeps working.
    """
    return (e - es) / es

