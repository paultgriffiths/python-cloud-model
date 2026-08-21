import numpy as np
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Make project root visible
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from experiments.run_cooling_95RH_test import (
    KiDCase1Config,
    initialize_state,
    initialize_history,
    kid_case1_updraft,
    update_liquid_growth,
    update_warm_rain,
    save_diagnostics,
)

from parcel_model.thermodynamics import Sw


from parcel_model.activation import check_activation

def mixing_ratio_to_vapour_pressure(qv: float, p: float) -> float:
    """Convert water vapour mixing ratio [kg/kg] to vapour pressure [Pa]."""
    epsilon = 0.622
    return qv * p / (epsilon + qv)

def update_activation_mode(state, config, mode):
    aerosol = state["aerosol"]

    e = mixing_ratio_to_vapour_pressure(state["qv"], state["p"])
    S = Sw(e, state["T"])

    activated, Sc = check_activation(S, aerosol, T=state["T"])

    state["e"] = e
    state["S"] = S
    state["Sc"] = Sc

    if mode == "python":
        diagnosed_Nc = aerosol.N * aerosol.activated_fraction

        # Persistent Nc: activated droplets do not disappear
        # immediately when supersaturation decreases.
        state["n_droplets"] = max(
            state["n_droplets"],
            diagnosed_Nc
        )

        state["activated_fraction"] = (
            state["n_droplets"] / aerosol.N
            if aerosol.N > 0.0 else 0.0
        )

    elif mode == "kid_fixed_Nd":
        if S > 0.0:
            state["n_droplets"] = 100e6
            state["activated_fraction"] = 1.0
        else:
            state["n_droplets"] = 0.0
            state["activated_fraction"] = 0.0

    else:
        raise ValueError(f"Unknown mode: {mode}")

    return state

def update_saturation_adjustment(state, config):
    epsilon = 0.622
    Lv = 2.5e6
    cp = 1005.0

    p = state["p"]
    qv_initial = state["qv"]
    T_initial = state["T"]

    def saturation_mixing_ratio(T):
        Tc = T - 273.15
        es = 611.2 * np.exp((17.67 * Tc) / (Tc + 243.5))
        return epsilon * es / (p - es)

    qsat_initial = saturation_mixing_ratio(T_initial)

    if state["n_droplets"] <= 0.0:
        state["cond_rate"] = 0.0
        state["dr_dt"] = 0.0

        e = mixing_ratio_to_vapour_pressure(state["qv"], state["p"])
        state["e"] = e
        state["S"] = Sw(e, state["T"])

        return state
    
    if qv_initial <= qsat_initial:
        state["cond_rate"] = 0.0

        e = mixing_ratio_to_vapour_pressure(state["qv"], state["p"])
        state["e"] = e
        state["S"] = Sw(e, state["T"])
        state["dr_dt"] = 0.0

        return state

    low = 0.0
    high = qv_initial

    for _ in range(40):
        dq = 0.5 * (low + high)

        T_new = T_initial + (Lv / cp) * dq
        qv_new = qv_initial - dq
        qsat_new = saturation_mixing_ratio(T_new)

        if qv_new > qsat_new:
            low = dq
        else:
            high = dq

    dq = 0.5 * (low + high)

    state["qv"] = qv_initial - dq
    state["ql"] += dq
    state["T"] = T_initial + (Lv / cp) * dq

    state["cond_rate"] = dq / config.dt
    state["dr_dt"] = 0.0

    e = mixing_ratio_to_vapour_pressure(state["qv"], state["p"])
    state["e"] = e
    state["S"] = Sw(e, state["T"])

    return state


def run_case(mode):
    config = KiDCase1Config()

    # Controlled experiment requested by Paul:
    # start near 95% RH and apply same cooling rate
    config.initial_temperature = 283.15
    config.initial_pressure = 99398.334
    config.initial_qv = 0.0073923
    config.ccn_concentration = 50e6
    config.dt = 0.5
    config.t_end = 3600.0

    cooling_rate = 0.001  # K/s

    state = initialize_state(config)
    history = initialize_history()

    t = 0.0
    while t <= config.t_end:
        w = kid_case1_updraft(t, config.w1, config.t1, config.t2)

        # same cooling applied to both activation modes
        state["T"] -= cooling_rate * config.dt

        state["z"] += w * config.dt

        state = update_activation_mode(state, config, mode)
        state = update_saturation_adjustment(state, config)

        if config.enable_rain:
            state = update_warm_rain(state, config)

        history = save_diagnostics(history, state, t, w)

        t += config.dt

    return pd.DataFrame(history)


def summarize(df, label):
    activated = df[df["n_droplets"] > 0]

    if len(activated) > 0:
        activation_time = activated["time"].iloc[0]
    else:
        activation_time = None

    return {
        "case": label,
        "activation_time_s": activation_time,
        "SSmax": df["S"].max(),
        "qcmax": df["cloud_mass"].max(),
        "max_Nc": df["n_droplets"].max(),
        "max_activated_fraction": df["activated_fraction"].max(),
    }


def main():
    os.makedirs("data", exist_ok=True)

    df_python = run_case("python")
    df_kid = run_case("kid_fixed_Nd")

    df_python.to_csv("data/same_cooling_python_activation.csv", index=False)
    df_kid.to_csv("data/same_cooling_kid_fixed_Nd.csv", index=False)

    summary = pd.DataFrame([
        summarize(df_python, "Python activation"),
        summarize(df_kid, "KiD-like fixed Nd"),
    ])

    summary.to_csv("data/same_cooling_comparison_metrics.csv", index=False)

    print(summary)

    plt.figure(figsize=(10, 6))
    plt.plot(df_python["time"], df_python["S"], label="Python activation")
    plt.plot(df_kid["time"], df_kid["S"], label="KiD-like fixed Nd")
    plt.axhline(0.0, linestyle="--", linewidth=1)
    plt.xlabel("Time (s)")
    plt.ylabel("Supersaturation S")
    plt.title("Same Cooling Rate Comparison: Supersaturation")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("Same_Cooling_Supersaturation.png", dpi=600)

    plt.figure(figsize=(10, 6))
    plt.plot(df_python["time"], df_python["cloud_mass"], label="Python activation")
    plt.plot(df_kid["time"], df_kid["cloud_mass"], label="KiD-like fixed Nd")
    plt.xlabel("Time (s)")
    plt.ylabel("Cloud water qc (kg kg$^{-1}$)")
    plt.title("Same Cooling Rate Comparison: Cloud Water")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("Same_Cooling_Cloud_Water.png", dpi=600)

    plt.figure(figsize=(10, 6))
    plt.plot(df_python["time"], df_python["n_droplets"], label="Python activation")
    plt.plot(df_kid["time"], df_kid["n_droplets"], label="KiD-like fixed Nd")
    plt.xlabel("Time (s)")
    plt.ylabel("Droplet number Nc (m$^{-3}$)")
    plt.title("Same Cooling Rate Comparison: Droplet Number")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("Same_Cooling_Droplet_Number.png", dpi=600)

    print("Saved same-cooling comparison results and figures.")


if __name__ == "__main__":
    main()
