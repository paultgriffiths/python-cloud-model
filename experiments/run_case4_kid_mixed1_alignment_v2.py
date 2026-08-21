import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from parcel_model.run_mixed_phase_maxwell_kidforcing import run

os.makedirs("data", exist_ok=True)

# KiD mixed1 forcing-aligned single-parcel approximation
# Reference layer: approximately z = 400 m
# KiD forcing shape: w(t) = 0.3 sin(pi t / 600)

run(
    w=0.3,
    dt=1.0,
    t_end=3600.0,

    outfile="data/case4_kid_mixed1_alignment_v2.csv",

    sulfate_N=5e7,
    pollen_N=1000.0,

    bio_N=1e5,
    bio_T50=269.15,
    bio_width=4.0,

    r_cloud_init=1e-6,
    r_ice_init=5e-6,

    T_init=253.10,
    RH0=0.999
)

print("Case 4 v2 forcing-aligned test finished.")
print("Saved: data/case4_kid_mixed1_alignment_v2.csv")
