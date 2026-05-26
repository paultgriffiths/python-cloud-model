def run_simulation(config):
    """
    Run cloud parcel model simulation.

    Parameters
    ----------
    config : ParcelConfig
        Configuration object containing model parameters.

    Returns
    -------
    dict
        Dictionary containing time series of model variables:
        - time (s)
        - temperature (K)
        - R (dimensionless)
    """

    # Initialize storage
    results = {
        "time": [],
        "temperature": [],
        "R": []
    }

    # Initial conditions
    t = 0.0
    T = config.T0  # Temperature (K)

    # Time integration loop
    while t < config.t_end:

        # ---------------------------
        # Example physics (replace later)
        # ---------------------------

        cond_rate = 1.0      # condensation rate (kg/kg/s) - placeholder
        dep_rate = 0.5       # deposition rate (kg/kg/s) - placeholder

        # Avoid division by zero
        if cond_rate == 0:
            R = 0.0
        else:
            R = abs(dep_rate) / abs(cond_rate)

        # ---------------------------
        # Store results
        # ---------------------------

        results["time"].append(t)
        results["temperature"].append(T)
        results["R"].append(R)

        # ---------------------------
        # Update time
        # ---------------------------

        t += config.dt

    return results
