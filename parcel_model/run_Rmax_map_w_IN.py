import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from run_mixed_phase_maxwell import run


def compute_Rmax(csv_file):

    df = pd.read_csv(csv_file)

    cond = np.abs(df["cond_rate_kgm3s"].values)
    dep = np.abs(df["dep_rate_kgm3s"].values)

    cond_thresh = 1e-12
    valid = cond > cond_thresh

    if np.any(valid):
        R = dep[valid] / cond[valid]
        return np.nanmax(R)
    else:
        return 0.0


def main():

    # Fixed CCN
    CCN_fixed = 50e6

    # Sweep grid
    w_list = [0.2, 0.5, 1.0, 1.5, 2.0]
    IN_list = [5, 50, 500, 5000, 50000]

    Rmax = np.zeros((len(IN_list), len(w_list)))

    for i, IN in enumerate(IN_list):
        for j, w in enumerate(w_list):

            outcsv = f"timeseries_CCN{int(CCN_fixed)}_w{w}_IN{int(IN)}.csv"

            print("-------------------------------------------")
            print(f"Running simulation: w={w}, IN={IN}")
            print("-------------------------------------------")

            run(
                w=w,
                dt=1.0,
                t_end=1200.0,
                sulfate_N=CCN_fixed,
                bio_N=float(IN),
                outfile=outcsv
            )

            Rmax[i, j] = compute_Rmax(outcsv)

            print("R_max =", Rmax[i, j])
            print()

    # =========================
    # HEATMAP
    # =========================

    plt.figure()

    extent = [
        min(w_list),
        max(w_list),
        np.log10(min(IN_list)),
        np.log10(max(IN_list))
    ]

    plt.imshow(
        Rmax,
        origin="lower",
        aspect="auto",
        extent=extent
    )

    plt.colorbar(label="R_max = max(|dep| / |cond|)")
    plt.xlabel("Updraft velocity w (m/s)")
    plt.ylabel("log10(IN)")
    plt.title("R_max map across (w, IN) with CCN fixed = 50e6")

    # Contour line R = 1
    w_vals = np.array(w_list)
    in_vals_log = np.log10(np.array(IN_list))

    W, INLOG = np.meshgrid(w_vals, in_vals_log)

    cs = plt.contour(
        W,
        INLOG,
        Rmax,
        levels=[1.0],
        colors="white",
        linewidths=2
    )

    plt.clabel(cs, fmt={1.0: "R=1"}, inline=True)

    plt.tight_layout()
    plt.savefig("Rmax_map_w_IN_CCN50e6_contour.png", dpi=300)

    print("Saved: Rmax_map_w_IN_CCN50e6_contour.png")

    # =========================
    # 3D SURFACE
    # =========================

    from mpl_toolkits.mplot3d import Axes3D

    W, IN = np.meshgrid(w_list, np.log10(IN_list))
    Z = np.log10(np.maximum(Rmax, 1e-20))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_surface(W, IN, Z)

    ax.set_xlabel("w (m/s)")
    ax.set_ylabel("log10(IN)")
    ax.set_zlabel("log10(R_max)")

    ax.set_title("3D surface: log10(R_max)")

    plt.tight_layout()
    plt.savefig("Rmax_3D_w_IN_CCN50e6.png", dpi=300)

    print("Saved: Rmax_3D_w_IN_CCN50e6.png")


if __name__ == "__main__":
    main()