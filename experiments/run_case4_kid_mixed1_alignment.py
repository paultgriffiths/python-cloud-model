import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from parcel_model.run_mixed_phase_maxwell import run

os.makedirs("data", exist_ok=True)

# KiD mixed1-inspired alignment case
# Based on KiD mixed-phase Case 8 / mixed1.nml:
# dt = 1 s
# aerosol number ~ 50e6 m^-3
# weak oscillating updraft scale w1 ~ 0.3 m/s
# This is a first direct-alignment test, not a full KiD reproduction.

run(
    w=0.3,
    dt=1.0,
    t_end=3600.0,

    outfile="data/case4_kid_mixed1_alignment.csv",

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

print("Case 4 KiD mixed1 alignment test finished.")
print("Saved: data/case4_kid_mixed1_alignment.csv")