import os
import pandas as pd
import numpy as np


def first_time_above(df, column, threshold=0.0, time_col="time"):
    vals = df[column].values
    times = df[time_col].values
    idx = np.where(vals > threshold)[0]
    if len(idx) == 0:
        return None
    return float(times[idx[0]])


def max_with_time(df, column, time_col="time"):
    idx = df[column].idxmax()
    return float(df.loc[idx, column]), float(df.loc[idx, time_col])


def summarize_case1(path):
    df = pd.read_csv(path)

    # safety: expected columns from your Case 1 script
    time_col = "time"

    metrics = {}

    metrics["case"] = "Case 1"
    metrics["n_steps"] = len(df)

    metrics["max_cloud_mass"], metrics["t_max_cloud_mass"] = max_with_time(df, "cloud_mass", time_col)
    metrics["max_rain_mass"], metrics["t_max_rain_mass"] = max_with_time(df, "rain_mass", time_col)
    metrics["max_surface_rain_rate"], metrics["t_max_surface_rain_rate"] = max_with_time(df, "surface_rain_rate", time_col)
    metrics["max_lwp"], metrics["t_max_lwp"] = max_with_time(df, "liquid_water_path", time_col)
    metrics["max_cond_rate"], metrics["t_max_cond_rate"] = max_with_time(df, "cond_rate", time_col)

    metrics["cloud_onset_time"] = first_time_above(df, "cloud_mass", threshold=1e-10, time_col=time_col)
    metrics["rain_onset_time"] = first_time_above(df, "rain_mass", threshold=1e-10, time_col=time_col)
    metrics["rain_rate_onset_time"] = first_time_above(df, "surface_rain_rate", threshold=1e-10, time_col=time_col)

    metrics["final_cloud_mass"] = float(df["cloud_mass"].iloc[-1])
    metrics["final_rain_mass"] = float(df["rain_mass"].iloc[-1])
    metrics["final_lwp"] = float(df["liquid_water_path"].iloc[-1])

    return metrics


def summarize_case2(path):
    df = pd.read_csv(path)

    # Case 2 from Maxwell uses t_s instead of time
    time_col = "t_s"

    metrics = {}

    metrics["case"] = "Case 2"
    metrics["n_steps"] = len(df)

    metrics["max_qcloud"], metrics["t_max_qcloud"] = max_with_time(df, "qcloud", time_col)
    metrics["max_qice"], metrics["t_max_qice"] = max_with_time(df, "qice", time_col)
    metrics["max_R_BF"], metrics["t_max_R_BF"] = max_with_time(df, "R_BF", time_col)
    metrics["max_Sw"], metrics["t_max_Sw"] = max_with_time(df, "Sw", time_col)
    metrics["max_Si"], metrics["t_max_Si"] = max_with_time(df, "Si", time_col)
    metrics["max_cond_sink"], metrics["t_max_cond_sink"] = max_with_time(df, "cond_sink_kgm3s", time_col)
    metrics["max_dep_sink"], metrics["t_max_dep_sink"] = max_with_time(df, "dep_sink_kgm3s", time_col)

    metrics["ice_onset_time"] = first_time_above(df, "qice", threshold=1e-12, time_col=time_col)
    metrics["cloud_onset_time"] = first_time_above(df, "qcloud", threshold=1e-12, time_col=time_col)

    metrics["time_R_above_1"] = first_time_above(df, "R_BF", threshold=1.0, time_col=time_col)
    metrics["time_dep_exceeds_cond"] = first_time_above(
        pd.DataFrame({
            time_col: df[time_col],
            "dep_minus_cond": df["dep_sink_kgm3s"] - df["cond_sink_kgm3s"]
        }),
        "dep_minus_cond",
        threshold=0.0,
        time_col=time_col
    )

    metrics["final_qcloud"] = float(df["qcloud"].iloc[-1])
    metrics["final_qice"] = float(df["qice"].iloc[-1])
    metrics["final_R_BF"] = float(df["R_BF"].iloc[-1])

    return metrics


def print_metrics(title, metrics):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    for k, v in metrics.items():
        print(f"{k}: {v}")


def main():
    case1_path = "data/kid_case1_results.csv"
    case2_path = "data/case2_from_maxwell.csv"

    if os.path.exists(case1_path):
        case1_metrics = summarize_case1(case1_path)
        print_metrics("CASE 1 METRICS", case1_metrics)
    else:
        print(f"\nCase 1 file not found: {case1_path}")

    if os.path.exists(case2_path):
        case2_metrics = summarize_case2(case2_path)
        print_metrics("CASE 2 METRICS", case2_metrics)
    else:
        print(f"\nCase 2 file not found: {case2_path}")


if __name__ == "__main__":
    main()