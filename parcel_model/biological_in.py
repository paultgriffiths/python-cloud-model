# biological_in.py
# Minimal biological ice nucleation (IN) parameterization

import math


class BiologicalIN:
    """
    Minimal representation of a biological ice-nucleating particle (IN) class.

    Parameters
    ----------
    name : str
        Name of the biological IN class
    N : float
        Number concentration (m^-3)
    T50 : float
        Temperature (K) at which 50% of particles are ice-active
    width : float
        Controls how rapidly activation increases with decreasing temperature (K)
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


def check_ice_nucleation(T: float, bio_in: BiologicalIN, N_threshold: float = 1.0):
    """
    Simple ice nucleation check.

    If the number of active IN exceeds a threshold, nucleation is assumed to occur.

    Returns
    -------
    nucleated : bool
        Whether ice nucleation occurs
    N_active : float
        Active IN number concentration (m^-3)
    """
    N_active = bio_in.active_IN_number(T)
    nucleated = (N_active >= N_threshold)
    return nucleated, N_active
