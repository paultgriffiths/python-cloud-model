import pandas as pd

from experiments.run_python_clean_matched_to_kid import (
    KiDCase1Config,
    initialize_state,
    initialize_history,
    update_activation_mode,
    update_liquid_growth,
    update_warm_rain,
    save_diagnostics,
)

dt_values = [2.0, 1.0, 0.5, 0.25, 0.1]

results = []

for dt in dt_values:

    config = KiDCase1Config()

    # Same clean baseline used in the KiD comparison
    config.initial_temperature = 283.15
    config.initial_pressure = 99398.334
    config.initial_qv = 0.0073923

    config.ccn_concentration = 50e6
    config.aerosol_radius = 0.05e-6
    config.aerosol_kappa = 0.3

    config.dt = dt
    config.t_end = 3600.0

    cooling_rate = 0.001

    state = initialize_state(config)
    history = initialize_history()

    t = 0.0

    while t <= config.t_end:

        w = 0.0

        state["T"] -= cooling_rate * config.dt

        state = update_activation_mode(
            state, config, "python"
        )

        state = update_liquid_growth(
            state, config, w
        )

        if config.enable_rain:
            state = update_warm_rain(
                state, config
            )

        history = save_diagnostics(
            history, state, t, w
        )

        t += config.dt

    df = pd.DataFrame(history)

    # Recalculate activated fraction using the actual aerosol number
    df["frac_true"] = (
        df["n_droplets"] / config.ccn_concentration
    )

    sat = df[df["S"] >= 0.0]
    active = df[df["n_droplets"] > 0.0]
    cloud = df[df["cloud_mass"] >= 1e-7]

    t_sat = sat.iloc[0]["time"] if len(sat) else None
    t_act = active.iloc[0]["time"] if len(active) else None
    t_cloud = cloud.iloc[0]["time"] if len(cloud) else None

    frac_first = (
        active.iloc[0]["frac_true"]
        if len(active)
        else 0.0
    )

    # More robust threshold-based activation diagnostics
    activation_thresholds = {
        "t_1pct_s": 0.01,
        "t_10pct_s": 0.10,
        "t_50pct_s": 0.50,
        "t_90pct_s": 0.90,
    }

    threshold_times = {}

    for label, threshold in activation_thresholds.items():
        rows = df[df["frac_true"] >= threshold]

        threshold_times[label] = (
            rows.iloc[0]["time"]
            if len(rows)
            else None
        )

    results.append({
        "dt_s": dt,
        "saturation_time_s": t_sat,
        "first_activation_time_s": t_act,
        "sat_to_first_activation_s": (
            t_act - t_sat
            if t_act is not None and t_sat is not None
            else None
        ),
        "fraction_at_first_activation": frac_first,

        "t_1pct_s": threshold_times["t_1pct_s"],
        "t_10pct_s": threshold_times["t_10pct_s"],
        "t_50pct_s": threshold_times["t_50pct_s"],
        "t_90pct_s": threshold_times["t_90pct_s"],

        "SSmax_percent": df["S"].max() * 100.0,
        "max_Nc_m3": df["n_droplets"].max(),
        "qc_1e-7_time_s": t_cloud,
        "qcmax_kgkg": df["cloud_mass"].max(),
    })

summary = pd.DataFrame(results)

summary.to_csv(
    "data/clean_timestep_sensitivity.csv",
    index=False
)

print()
print("CLEAN TIMESTEP SENSITIVITY")
print("--------------------------")
print(summary.to_string(index=False))
