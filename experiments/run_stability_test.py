import numpy as np
import pandas as pd
import os
import sys

# allow import from parcel_model
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "parcel_model"))

from run_mixed_phase_maxwell import run


def check_stability(csv_file):
    df = pd.read_csv(csv_file)

    if df.isna().any().any():
        return "UNSTABLE (NaN detected)"

    numeric_df = df.select_dtypes(include=[np.number])
    if np.isinf(numeric_df.values).any():
        return "UNSTABLE (Inf detected)"

    if "Si" in df.columns and np.max(np.abs(df["Si"].values)) > 1.0:
        return "UNSTABLE (Si exploded)"

    if "r_ice_m" in df.columns and (df["r_ice_m"] < 0).any():
        return "UNSTABLE (negative ice radius)"

    return "STABLE"


def main():
    w_list = [10.0]
    dt_list = [20.0, 50.0, 100.0]
    r_ice_list = [1e-7]   # 1 micron, 500 nm, 100 nm

    os.makedirs("data", exist_ok=True)

    results = []

    for w in w_list:
        for dt in dt_list:
            for r_ice in r_ice_list:
                outfile = f"data/stability_w{w}_dt{dt}_rice{r_ice:.0e}.csv"

                print("-" * 70)
                print(f"Running case: w={w}, dt={dt}, r_ice_init={r_ice:.1e} m")
                print("-" * 70)

                try:
                    run(
                        w=w,
                        dt=dt,
                        t_end=600.0,
                        outfile=outfile,
                        r_ice_init=r_ice
                    )
                    status = check_stability(outfile)

                except Exception as e:
                    status = f"FAILED ({type(e).__name__}: {e})"

                print(f"Result: {status}\n")

                results.append({
                    "w_m_per_s": w,
                    "dt_s": dt,
                    "r_ice_init_m": r_ice,
                    "status": status
                })

    df = pd.DataFrame(results)
    df.to_csv("data/stability_results.csv", index=False)
    print("Saved: data/stability_results.csv")


if __name__ == "__main__":
    main()