# biological_in.py
# Minimal biological ice nucleation (IN) parameterization

import math


class BiologicalIN:
    """
    Minimal representation of a biological ice-nucleating particle (IN) class.
    """

    def __init__(self, name: str, N: float, T50: float = 263.15, width: float = 2.0):
        self.name = name
        self.N = float(N)
        self.T50 = float(T50)
        self.width = float(width)

    def ice_active_fraction(self, T: float) -> float:
        """
        Fraction of particles that are ice-active at temperature T (K).
        Uses a logistic function: colder temperatures -> higher active fraction.
        """
        x = (self.T50 - T) / max(self.width, 1e-12)
        f = 1.0 / (1.0 + math.exp(-x))
        return max(0.0, min(1.0, f))

    def active_IN_number(self, T: float) -> float:
        """
        Active ice-nucleating particle number concentration (m^-3)
        """
        return self.N * self.ice_active_fraction(T)


def check_ice_nucleation(
    T: float,
    bio_in: BiologicalIN,
    N_threshold: float = 1.0,
    frac_threshold: float = 0.1,
    T_max: float = 273.15
):
    """
    Physically constrained ice nucleation check.
    """

    N_active = bio_in.active_IN_number(T)

    # Guard: no nucleation above freezing
    if T > T_max:
        return False, N_active

    # Require meaningful active fraction
    crit = max(float(N_threshold), float(frac_threshold) * bio_in.N)
    nucleated = (N_active >= crit)

    return nucleated, N_active