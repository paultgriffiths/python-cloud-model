import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from run_mixed_phase_maxwell import run


def compute_rmax(csv_file):
    df = pd.read_csv(csv_file)

    cond = np.abs(df["cond_rate_kgm3s"].values)
    dep = np.abs(df["dep_rate_kgm3s"].values)

    # avoid division by very small values
    valid = cond > 1e-12

    if np.any(valid):
        r = dep[valid] / cond[valid]
        return np.max(r)
    else:
        return 0.0


def main():

    # -----------------------------
    # FIXED SETTINGS
    # -----------------------------
    w_fixed = 2.0
    dt = 1.0
    t_end = 1200.0

    # -----------------------------
    # PARAMETER SPACE
    # -----------------------------
    ccn_list = [5e5, 5e6, 5e7, 5e8]
    in_list = [5, 50, 500, 5000, 50000, 500000]

    rmax_map = np.zeros((len(in_list), len(ccn_list)))

    # -----------------------------
    # RUN SIMULATIONS
    # -----------------------------
    for i, IN in enumerate(in_list):
        for j, CCN in enumerate(ccn_list):

            outcsv = f"heatmap_CCN{int(CCN)}_IN{int(IN)}.csv"

            print("-" * 60)
            print(f"Running: CCN={CCN:.2e}, IN={IN:.2e}")
            print("-" * 60)

            run(
                w=w_fixed,
                dt=dt,
                t_end=t_end,
                sulfate_N=CCN,
                bio_N=IN,
                outfile=outcsv
            )

            rmax = compute_rmax(outcsv)
            rmax_map[i, j] = rmax

            print(f"R_max = {rmax:.3e}\n")

    # -----------------------------
    # PLOT HEATMAP
    # -----------------------------
    plt.figure(figsize=(7, 5))

    # log scale
    z = np.log10(np.maximum(rmax_map, 1e-20))

    im = plt.imshow(z, origin="lower", aspect="auto")
    plt.colorbar(im, label="log10(R_max)")

    plt.xticks(
        ticks=np.arange(len(ccn_list)),
        labels=[f"{x:.0e}" for x in ccn_list]
    )

    plt.yticks(
        ticks=np.arange(len(in_list)),
        labels=[f"{y:.0e}" for y in in_list]
    )

    plt.xlabel("CCN concentration")
    plt.ylabel("IN concentration")
    plt.title("R_max heatmap with R = 1 boundary")

    # -----------------------------
    #    BOUNDARY R = 1
    # -----------------------------
    CS = plt.contour(
        z,
        levels=[0],   # log10(1) = 0
        colors="white",
        linewidths=2
    )

    plt.clabel(CS, fmt="R = 1", inline=True, fontsize=10)

    # -----------------------------
    # SAVE FIGURE
    # -----------------------------
    plt.tight_layout()
    plt.savefig("Rmax_heatmap_CCN_IN_boundary.png", dpi=300)

    print("Saved: Rmax_heatmap_CCN_IN_boundary.png")


if __name__ == "__main__":
    main()