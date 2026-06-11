import os
import pandas as pd
import matplotlib.pyplot as plt

from run_fraction_test import KiDCase1Config
from run_fraction_test import initialize_state
from run_fraction_test import initialize_history
from run_fraction_test import kid_case1_updraft
from run_fraction_test import update_activation
from run_fraction_test import update_liquid_growth
from run_fraction_test import update_warm_rain
from run_fraction_test import save_diagnostics


def run_with_dt(dt):
    config = KiDCase1Config()
    config.dt = dt
    config.initial_qv = 0.00862

    state = initialize_state(config)
    history = initialize_history()

    t = 0.0
    while t <= config.t_end:
        w = kid_case1_updraft(t, config.w1, config.t1, config.t2)

        state["z"] += w * config.dt
        state = update_activation(state, config)
        state = update_liquid_growth(state, config, w)

        if config.enable_rain:
            state = update_warm_rain(state, config)

        history = save_diagnostics(history, state, t, w)
        t += config.dt

    return pd.DataFrame(history)


def extract_metrics(df, dt):
    activated = df[df["n_droplets"] > 0]

    if len(activated) > 0:
        activation_time = activated["time"].iloc[0]
        max_fraction = df["activated_fraction"].max()
    else:
        activation_time = None
        max_fraction = 0.0

    return {
        "dt": dt,
        "activation_time": activation_time,
        "SSmax": df["S"].max(),
        "qcmax": df["cloud_mass"].max(),
        "max_activated_fraction": max_fraction,
    }


def main():
    os.makedirs("data", exist_ok=True)

    dt_values = [0.1, 0.5, 1.0, 2.0]
    metrics = []

    for dt in dt_values:
        df = run_with_dt(dt)
        df.to_csv(f"data/solver_sensitivity_dt_{dt}.csv", index=False)
        metrics.append(extract_metrics(df, dt))

    metrics_df = pd.DataFrame(metrics)
    metrics_df.to_csv("data/solver_sensitivity_metrics.csv", index=False)

    print(metrics_df)

    plt.figure(figsize=(10, 6))
    plt.plot(metrics_df["dt"], metrics_df["SSmax"], marker="o", linewidth=3)
    plt.xlabel("Time step dt (s)")
    plt.ylabel("SSmax")
    plt.title("Solver Sensitivity: SSmax vs Time Step")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("Solver_Sensitivity_SSmax.png", dpi=600)

    plt.figure(figsize=(10, 6))
    plt.plot(
        metrics_df["dt"],
        100 * metrics_df["max_activated_fraction"],
        marker="o",
        linewidth=3,
    )
    plt.xlabel("Time step dt (s)")
    plt.ylabel("Maximum activated fraction (%)")
    plt.title("Solver Sensitivity: Activated Fraction vs Time Step")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("Solver_Sensitivity_Activated_Fraction.png", dpi=600)

    print("Saved solver sensitivity results and figures.")


if __name__ == "__main__":
    main()
