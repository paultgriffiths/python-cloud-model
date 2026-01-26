# ice_growth.py
# Minimal ice deposition growth (toy but stable)

def ice_deposition_sink(S, es, qi, dt, k0=1e-5, alpha=50.0):
    """
    Compute a simple vapour sink due to ice deposition growth.
    Returns vapour removed (Pa) and updated qi (ice proxy).
    """
    if S <= 0.0:
        return 0.0, qi

    growth_factor = (1.0 + alpha * qi)
    de = k0 * growth_factor * S * es * dt

    qi_new = qi + 1e-8 * de  # small update for stability
    return de, qi_new
