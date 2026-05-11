import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from parcel_model.run_mixed_phase_maxwell import run

os.makedirs("data", exist_ok=True)

run(
    w=2.0,
    dt=1.0,
    t_end=1200.0,

    outfile="data/case3_literature_benchmark.csv",

    sulfate_N=5e7,
    pollen_N=1000.0,

    bio_N=1e5,
    bio_T50=269.15,
    bio_width=4.0,

    r_cloud_init=1e-6,
    r_ice_init=5e-6,

    T_init=268.15,
    RH0=0.999
)

print("Case 3 literature-inspired benchmark finished.")