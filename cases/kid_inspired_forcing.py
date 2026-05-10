import numpy as np


def kid_inspired_updraft(t_s, w_max=2.0, t_forcing=600.0):
    """
    KiD-inspired time-dependent updraft forcing.
    """

    # Before forcing
    if t_s < 0:
        return 0.0

    # During forcing
    if t_s <= t_forcing:
        return w_max * np.sin(np.pi * t_s / t_forcing)

    # After forcing
    return 0.0