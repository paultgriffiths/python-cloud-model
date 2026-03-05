import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from run_mixed_phase_maxwell import run


def compute_R_masked(df, cond_thresh=1e-12):
    t = df["t_s"].values
    cond = np.abs(df["cond_rate_kgm3s"].values)
    dep  = np.abs(df["dep_rate_kgm3s"].values)

    R = np.full_like(t, np.nan, dtype=float)
    ok = cond > cond_thresh
    R[ok] = dep[ok] / cond[ok]
    return t, R


def main():
    # --- Choose w values (m/s)
    w_cases = [0.2, 0.5, 1.0, 2.0]

    # --- Keep aerosol/IN fixed (edit if you want)
    sulfate_N = 50e6   # baseline CCN
    bio_N = 5.0         # baseline IN

    # --- Mask threshold
    cond_thresh = 1e-12

    plt.figure()

    for w in w_cases:
        outcsv = f"timeseries_w{w:.1f}.csv"

        print("\n" + "-"*70)
        print(f"Running w = {w:.2f} m/s  (CCN={sulfate_N:.2e}, IN={bio_N:.2e})")
        print(f" -> outfile: {outcsv}")
        print("-"*70)

        # Run model
        # (This assumes your run() accepts sulfate_N and bio_N.
        #  If not, tell me and I'll adapt the script to your current version.)
        run(
            w=w,
            dt=1.0,
            t_end=1200.0,
            sulfate_N=sulfate_N,
            bio_N=bio_N,
            outfile=outcsv
        )

        # Load & compute R
        df = pd.read_csv(outcsv)
        t, R = compute_R_masked(df, cond_thresh=cond_thresh)
        R_max = np.nanmax(R)
        print(f"Max R (masked): {R_max:.3e}")

        plt.plot(t, R, label=f"w = {w:.1f} m/s")

    plt.axhline(1.0, linestyle="--", label="R = 1 threshold")
    plt.xlabel("Time (s)")
    plt.ylabel("R = |dep_rate| / |cond_rate|")
    plt.title("Ice-dominance diagnostic across updraft velocity cases")
    plt.yscale("log")
    plt.legend()
    plt.tight_layout()
    plt.savefig("R_w_sweep_vs_time.png", dpi=300)
    print("\nSaved: R_w_sweep_vs_time.png")


if __name__ == "__main__":
    main()