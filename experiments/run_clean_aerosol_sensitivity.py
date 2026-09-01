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


def run_case(N=50e6, radius=0.05e-6, kappa=0.3, dt=0.5):
    config = KiDCase1Config()

    config.initial_temperature = 283.15
    config.initial_pressure = 99398.334
    config.initial_qv = 0.0073923

    config.ccn_concentration = N
    config.aerosol_radius = radius
    config.aerosol_kappa = kappa

    config.dt = dt
    config.t_end = 3600.0

    cooling_rate = 0.001

    state = initialize_state(config)
    history = initialize_history()

    t = 0.0

    while t <= config.t_end:
        w = 0.0

        state["T"] -= cooling_rate * config.dt
        state = update_activation_mode(state, config, "python")
        state = update_liquid_growth(state, config, w)

        if config.enable_rain:
            state = update_warm_rain(state, config)

        history = save_diagnostics(history, state, t, w)
        t += config.dt

    df = pd.DataFrame(history)

    df["frac_true"] = (
        df["n_droplets"] / config.ccn_concentration
    )

    sat = df[df["S"] >= 0.0]
    active = df[df["n_droplets"] > 0.0]
    cloud = df[df["cloud_mass"] >= 1e-7]

    t_sat = sat.iloc[0]["time"] if len(sat) else None
    t_act = active.iloc[0]["time"] if len(active) else None
    t_cloud = cloud.iloc[0]["time"] if len(cloud) else None

    thresholds = {
        "t_1pct_s": 0.01,
        "t_10pct_s": 0.10,
        "t_50pct_s": 0.50,
        "t_90pct_s": 0.90,
    }

    threshold_times = {}

    for label, threshold in thresholds.items():
        rows = df[df["frac_true"] >= threshold]
        threshold_times[label] = (
            rows.iloc[0]["time"] if len(rows) else None
        )

    return {
        "saturation_time_s": t_sat,
        "first_activation_time_s": t_act,
        "sat_to_first_activation_s": (
            t_act - t_sat
            if t_act is not None and t_sat is not None
            else None
        ),
        "t_1pct_s": threshold_times["t_1pct_s"],
        "t_10pct_s": threshold_times["t_10pct_s"],
        "t_50pct_s": threshold_times["t_50pct_s"],
        "t_90pct_s": threshold_times["t_90pct_s"],
        "SSmax_percent": df["S"].max() * 100.0,
        "max_Nc_m3": df["n_droplets"].max(),
        "qc_1e-7_time_s": t_cloud,
        "qcmax_kgkg": df["cloud_mass"].max(),
    }


def run_sweep(values, parameter_name):
    results = []

    for value in values:
        kwargs = {}

        if parameter_name == "aerosol_N_m3":
            kwargs["N"] = value
        elif parameter_name == "aerosol_radius_um":
            kwargs["radius"] = value * 1e-6
        elif parameter_name == "kappa":
            kwargs["kappa"] = value

        row = run_case(**kwargs)
        row = {parameter_name: value, **row}
        results.append(row)

    return pd.DataFrame(results)


number_df = run_sweep(
    [25e6, 50e6, 100e6, 200e6],
    "aerosol_N_m3",
)

radius_df = run_sweep(
    [0.03, 0.05, 0.07, 0.10],
    "aerosol_radius_um",
)

kappa_df = run_sweep(
    [0.1, 0.3, 0.6, 1.0],
    "kappa",
)

number_df.to_csv(
    "data/clean_aerosol_number_sensitivity.csv",
    index=False,
)

radius_df.to_csv(
    "data/clean_aerosol_radius_sensitivity.csv",
    index=False,
)

kappa_df.to_csv(
    "data/clean_kappa_sensitivity.csv",
    index=False,
)

print()
print("AEROSOL NUMBER SENSITIVITY")
print(number_df.to_string(index=False))

print()
print("AEROSOL RADIUS SENSITIVITY")
print(radius_df.to_string(index=False))

print()
print("KAPPA SENSITIVITY")
print(kappa_df.to_string(index=False))
