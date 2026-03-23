import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from run_mixed_phase_maxwell import run


def compute_rmax(csv_file: str, cond_thresh: float = 1e-12) -> float:
    """
    Compute R_max = max(|dep_rate| / |cond_rate|) from a simulation CSV.
    Small condensation rates are masked to avoid numerical blow-up.
    """
    df = pd.read_csv(csv_file)

    cond = np.abs(df["cond_rate_kgm3s"].values)
    dep = np.abs(df["dep_rate_kgm3s"].values)

    valid = cond > cond_thresh
    if np.any(valid):
        r = dep[valid] / cond[valid]
        return float(np.nanmax(r))
    return 0.0


def main():
    # -----------------------------
    # Fixed dynamical settings
    # -----------------------------
    w_fixed = 2.0
    dt = 1.0
    t_end = 1200.0
    pollen_N = 0.0  # keep pollen off for a clean CCN-IN comparison

    # -----------------------------
    # Parameter space
    # -----------------------------
    ccn_list = [5e5, 5e6, 5e7, 5e8]
    in_list = [5, 50, 500, 5000, 50000, 500000]

    rmax_map = np.zeros((len(in_list), len(ccn_list)))

    for i, bio_N in enumerate(in_list):
        for j, sulfate_N in enumerate(ccn_list):
            outcsv = f"heatmap_CCN{int(sulfate_N)}_IN{int(bio_N)}.csv"

            print("-" * 70)
            print(f"Running case: CCN={sulfate_N:.2e}, IN={bio_N:.2e}, w={w_fixed:.1f}")
            print("-" * 70)

            run(
                w=w_fixed,
                dt=dt,
                t_end=t_end,
                outfile=outcsv,
                sulfate_N=sulfate_N,
                pollen_N=pollen_N,
                bio_N=bio_N
            )

            rmax = compute_rmax(outcsv)
            rmax_map[i, j] = rmax

            print(f"R_max = {rmax:.3e}")
            print()

    # Save numeric table
    rows = []
    for i, bio_N in enumerate(in_list):
        for j, sulfate_N in enumerate(ccn_list):
            rows.append({
                "CCN": sulfate_N,
                "IN": bio_N,
                "R_max": rmax_map[i, j]
            })

    df_out = pd.DataFrame(rows)
    df_out.to_csv("Rmax_heatmap_CCN_IN.csv", index=False)
    print("Saved: Rmax_heatmap_CCN_IN.csv")

    # -----------------------------
    # Plot heatmap
    # -----------------------------
    plt.figure(figsize=(7, 5))

    # plot log10(Rmax) to show wide range clearly
    z = np.log10(np.maximum(rmax_map, 1e-20))

    im = plt.imshow(
        z,
        origin="lower",
        aspect="auto"
    )

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
    plt.title("Heatmap of R_max across CCN and IN")

    # Optional: mark cells where R_max >= 1
    for i in range(len(in_list)):
        for j in range(len(ccn_list)):
            if rmax_map[i, j] >= 1.0:
                plt.text(j, i, "R≥1", ha="center", va="center")

    plt.tight_layout()
    plt.savefig("Rmax_heatmap_CCN_IN.png", dpi=300)
    print("Saved: Rmax_heatmap_CCN_IN.png")


if __name__ == "__main__":
    main()