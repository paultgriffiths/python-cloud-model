def run_simulation(config):
    """
    Run parcel model simulation.
    """

    results = {
        "time": [],
        "temperature": [],
        "R": []
    }

    t = 0.0

    while t < config.t_end:

        R = 0.5  # example

        results["time"].append(t)
        results["temperature"].append(config.T0)
        results["R"].append(R)

        t += config.dt

    return results
