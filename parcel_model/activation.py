from parcel_model.kohler import critical_supersaturation

def check_activation(S, aerosol, T=298.15):
    """
    Returns activation state and critical supersaturation.
    Also computes a simple activated fraction.
    """

    Dp = 2.0 * aerosol.radius
    Sc = critical_supersaturation(
        Dp=Dp,
        kappa=aerosol.kappa,
        T=T
    )

    if S < Sc:
        fraction = 0.0

    elif S >= 2.0 * Sc:
        fraction = 1.0

    else:
        fraction = (S - Sc) / Sc

    aerosol.activated_fraction = fraction
    aerosol.activated = fraction > 0.0

    return aerosol.activated, Sc
