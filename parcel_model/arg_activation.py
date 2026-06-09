import numpy as np
from math import erf, sqrt


def lognormal_activation_fraction(Smax, Sc_median, sigma_g):
    """
    Activated fraction for a lognormal aerosol mode.

    Parameters
    ----------
    Smax : float
        Maximum supersaturation.

    Sc_median : float
        Median critical supersaturation.

    sigma_g : float
        Geometric standard deviation.

    Returns
    -------
    frac : float
        Activated fraction (0-1).
    """

    if Smax <= 0.0:
        return 0.0

    x = np.log(Smax / Sc_median)

    frac = 0.5 * (
        1.0 + erf(
            x / (sqrt(2.0) * np.log(sigma_g))
        )
    )

    return max(0.0, min(frac, 1.0))
