# activation.py

from kohler import critical_supersaturation

def check_activation(S, aerosol, T=298.15):
    """
    Returns True if aerosol activates at supersaturation S.
    Also sets aerosol.activated = True/False.
    """
    Dp = 2.0 * aerosol.radius  # convert radius to diameter
    Sc = critical_supersaturation(Dp=Dp, kappa=aerosol.kappa, T=T)

    aerosol.activated = (S >= Sc)
    return aerosol.activated, Sc
