# thermodynamics.py

import math
from constants import Lv, Rv

def saturation_vapor_pressure(T):
    """
    Saturation vapor pressure (Pa) using a simple Clausius–Clapeyron form.
    T : temperature in Kelvin
    """
    T0 = 273.15
    es0 = 610.94  # Pa at T0
    return es0 * math.exp((Lv / Rv) * (1 / T0 - 1 / T))


def supersaturation(e, es):
    """
    Supersaturation S = e/es - 1
    """
    return (e / es) - 1

