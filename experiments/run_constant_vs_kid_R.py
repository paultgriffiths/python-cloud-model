import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parcel_model.run_mixed_phase_maxwell import run

os.makedirs("data", exist_ok=True)

# Case A: constant updraft
run(
    w=1.0,
    dt=0.5,
    t_end=3600.0,
    outfile="data/case2_constant_w1.csv",
    sulfate_N=5e7,
    pollen_N=3000.0,
    bio_N=1e5,
    bio_T50=269.15,
    bio_width=4.0,
    r_cloud_init=1e-6,
    r_ice_init=5e-6,
    T_init=268.15,
    RH0=0.999
)

# Case B: KiD-inspired effective updraft
run(
    w=2.0,
    dt=0.5,
    t_end=3600.0,
    outfile="data/case2_kid_effective_w2.csv",
    sulfate_N=5e7,
    pollen_N=3000.0,
    bio_N=1e5,
    bio_T50=269.15,
    bio_width=4.0,
    r_cloud_init=1e-6,
    r_ice_init=5e-6,
    T_init=268.15,
    RH0=0.999
)

print("Constant vs KiD-inspired effective forcing simulations completed.")
print("Saved:")
print("data/case2_constant_w1.csv")
print("data/case2_kid_effective_w2.csv")