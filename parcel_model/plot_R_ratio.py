import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    csv_file = "mixed_phase_maxwell_timeseries.csv"
    df = pd.read_csv(csv_file)

    # Required columns
    t = df["t_s"].values
    T = df["T_K"].values
    cond = df["cond_rate_kgm3s"].values
    dep  = df["dep_rate_kgm3s"].values

    # absolute values
    cond_abs = np.abs(cond)
    dep_abs  = np.abs(dep)

    # --- Quick stats (help choose thresholds) ---
    max_dep = dep_abs.max()
    max_cond = cond_abs.max()
    nonzero_cond = cond_abs[cond_abs > 0.0]
    min_nonzero_cond = nonzero_cond.min() if nonzero_cond.size > 0 else 0.0
    p1_cond = np.percentile(nonzero_cond, 1) if nonzero_cond.size > 0 else 0.0

    print(f"Stats: max_dep={max_dep:.3e}, max_cond={max_cond:.3e}, min_nonzero_cond={min_nonzero_cond:.3e}, cond_1pct={p1_cond:.3e}")

    # --- Threshold strategy (automatic but tunable) ---
    # minimum absolute condensation rate considered "meaningful"
    cond_thresh = max(1e-14, min_nonzero_cond * 0.5, p1_cond*0.1)
    # require deposition to be larger than a small fraction of max_cond (so it's not negligible)
    dep_thresh = max(1e-14, max_cond * 1e-6, max_dep * 1e-9)

    print(f"Using thresholds: cond_thresh={cond_thresh:.3e}, dep_thresh={dep_thresh:.3e}")

    # --- Build masked R (NaN when cond too small) ---
    R = np.full_like(t, np.nan, dtype=float)
    valid = cond_abs > cond_thresh
    R[valid] = dep_abs[valid] / cond_abs[valid]

    # --- Find transition: require R crossing 1 AND dep significant ---
    R_valid = R.copy()
    R_valid[np.isnan(R_valid)] = -np.inf  # don't trigger on NaNs

    # find first index where previous <1 and current >=1 AND deposition at current > dep_thresh
    idx = np.where(
        (R_valid[:-1] < 1.0) &
        (R_valid[1:] >= 1.0) &
        (dep_abs[1:] > dep_thresh)
    )[0]

    if len(idx) > 0:
        i = idx[0] + 1
        t_tr = t[i]
        T_tr = T[i]
        print(f"Transition detected: R crosses 1 at t = {t_tr:.1f} s, T = {T_tr:.2f} K")
    else:
        t_tr = None
        T_tr = None
        print("No transition detected (R did not cross 1 under robust criteria).")

    # -------- Plot R vs time (masked) --------
    plt.figure(figsize=(7,5))
    plt.plot(t, R, label="R(t) = |dep_rate| / |cond_rate|")
    plt.axhline(1.0, linestyle="--", color="C1", label="R = 1 threshold")

    if t_tr is not None:
        plt.axvline(t_tr, linestyle=":", color="k", label=f"transition @ {t_tr:.0f}s")

    plt.xlabel("Time (s)")
    plt.ylabel("Dominance ratio R")
    plt.title("Ice-dominated regime diagnostic (R vs time)")
    plt.yscale("log")
    plt.legend()
    plt.tight_layout()
    plt.savefig("R_vs_time.png", dpi=300)
    print("Saved: R_vs_time.png")

    # -------- Plot R vs temperature --------
    order = np.argsort(T)
    plt.figure(figsize=(7,5))
    plt.plot(T[order], R[order], label="R(T)")
    plt.axhline(1.0, linestyle="--", color="C1", label="R = 1 threshold")
    if T_tr is not None:
        plt.axvline(T_tr, linestyle=":", color="k", label=f"transition @ {T_tr:.2f}K")
    plt.xlabel("Temperature (K)")
    plt.ylabel("Dominance ratio R")
    plt.title("Ice-dominated regime diagnostic (R vs temperature)")
    plt.yscale("log")
    plt.gca().invert_xaxis()
    plt.legend()
    plt.tight_layout()
    plt.savefig("R_vs_temperature.png", dpi=300)
    print("Saved: R_vs_temperature.png")

if __name__ == "__main__":
    main()