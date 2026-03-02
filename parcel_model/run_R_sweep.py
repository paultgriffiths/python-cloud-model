import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from run_mixed_phase_maxwell import run


def compute_R_masked(df, cond_thresh=1e-12):
    cond = np.abs(df["cond_rate_kgm3s"].values)
    dep  = np.abs(df["dep_rate_kgm3s"].values)
    t    = df["t_s"].values

    R = np.full_like(t, np.nan, dtype=float)
    valid = cond > cond_thresh
    R[valid] = dep[valid] / cond[valid]
    return t, R


def main():
    # --- Define the 3 cases you mentioned ---
    cases = [
        {"name": "Case A: CCN=500e6, IN=5",     "sulfate_N": 500e6, "bio_N": 5.0},
        {"name": "Case B: CCN=50e6,  IN=500",   "sulfate_N": 50e6,  "bio_N": 500.0},
        {"name": "Case C: CCN=5e6,   IN=5000",  "sulfate_N": 5e6,   "bio_N": 5000.0},
    ]

    # Threshold to avoid blow-ups when cond_rate ~ 0
    cond_thresh = 1e-12

    plt.figure()

    for c in cases:
        outcsv = f"timeseries_{int(c['sulfate_N']):d}_{int(c['bio_N']):d}.csv"

        print("\n" + "-"*70)
        print(f"Running: {c['name']}")
        print(f" -> outfile: {outcsv}")
        print("-"*70)

        # Run model
        run(
            w=1.0,
            dt=1.0,
            t_end=1200.0,
            sulfate_N=c["sulfate_N"],
            bio_N=c["bio_N"],
            outfile=outcsv
        )

        # Load output and compute masked R
        df = pd.read_csv(outcsv)
        t, R = compute_R_masked(df, cond_thresh=cond_thresh)

        # Print max R (valid only)
        R_max = np.nanmax(R) if np.isfinite(np.nanmax(R)) else np.nan
        print(f"Max R (masked, cond_thresh={cond_thresh:.1e}): {R_max:.3e}")

        # Plot
        plt.plot(t, R, label=c["name"])

    # Threshold line
    plt.axhline(1.0, linestyle="--", label="R = 1 threshold")

    plt.xlabel("Time (s)")
    plt.ylabel("R(t) = |dep_rate| / |cond_rate|")
    plt.title("Ice-dominance diagnostic across aerosol scenarios")
    plt.yscale("log")
    plt.legend()
    plt.tight_layout()
    plt.savefig("R_sweep_vs_time.png", dpi=300)
    print("\nSaved: R_sweep_vs_time.png")


if __name__ == "__main__":
    main()