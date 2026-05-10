import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cases.kid_inspired_forcing import kid_inspired_updraft
from parcel_model.run_mixed_phase_maxwell import run


os.makedirs("data", exist_ok=True)

# KiD-inspired forcing settings
w_max = 2.0
t_forcing = 600.0

# Current model expects a constant updraft value.
# For now, we use the maximum KiD-inspired updraft as an aligned forcing case.
w_effective = w_max

run(
    w=w_effective,
    dt=0.5,
    t_end=3600.0,
    outfile="data/case2_from_maxwell.csv",

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

print("Case 2 from Maxwell finished.")
print(f"KiD-inspired alignment case used w_effective = {w_effective} m/s.")