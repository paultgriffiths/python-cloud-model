import os
import pandas as pd

from parcel_model.run_mixed_phase_maxwell_kidforcing import run

os.makedirs("data", exist_ok=True)

bio_values = [1e3, 2.5e3, 1e4, 5e4, 1e5]

results = []

for bio_N in bio_values:

    outfile = f"data/mixed1_bioN_{bio_N:.0f}.csv"

    run(
        w=0.3,
        dt=1.0,
        t_end=3600.0,

        outfile=outfile,

        sulfate_N=5e7,
        pollen_N=1000.0,

        bio_N=bio_N,
        bio_T50=269.15,
        bio_width=4.0,

        r_cloud_init=1e-6,
        r_ice_init=5e-6,

        T_init=253.10,
        RH0=0.999
    )

    df = pd.read_csv(outfile)

    ice = df[df["Nice"] > 0.0]

    first_ice = (
        ice.iloc[0]["t_s"]
        if len(ice)
        else None
    )

    imax = df["qice"].idxmax()

    results.append({
        "bio_N_m3": bio_N,
        "first_ice_time_s": first_ice,
        "max_Nice_m3": df["Nice"].max(),
        "max_qice_kgkg": df["qice"].max(),
        "max_qcloud_kgkg": df["qcloud"].max(),
        "max_Si_percent": df["Si"].max() * 100.0,
        "max_Sw_percent": df["Sw"].max() * 100.0,
        "time_max_qice_s": df.loc[imax, "t_s"],
        "T_at_max_qice_K": df.loc[imax, "T_K"],
    })

summary = pd.DataFrame(results)

summary.to_csv(
    "data/mixed1_bioN_sensitivity_summary.csv",
    index=False
)

print()
print("MIXED1 BIOLOGICAL-IN NUMBER SENSITIVITY")
print("---------------------------------------")
print(summary.to_string(index=False))
