import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# --------------------------------------------------
# Read official KiD warm benchmark output
# --------------------------------------------------

kid = Dataset("/home/dryaktine/KiD-A/output/warm1_output.nc")

time_kid = kid.variables["time"][:]
cloud_kid = kid.variables["cloud_mass_path"][:]
rain_kid = kid.variables["rain_mass_path"][:]

# --------------------------------------------------
# Improved physics-inspired Python warm-cloud alignment
# --------------------------------------------------

dt = 30.0
t_end = 3600.0
time_py = np.arange(0, t_end + dt, dt)

cloud_py = np.zeros_like(time_py, dtype=float)
rain_py = np.zeros_like(time_py, dtype=float)

cloud_growth_rate = 0.045
autoconversion_threshold = 0.9
rain_growth_rate = 0.055
cloud_decay_rate = 0.018
rain_decay_rate = 0.010

for i in range(1, len(time_py)):

    cloud_source = cloud_growth_rate * np.exp(-time_py[i] / 1400.0)

    if cloud_py[i - 1] > autoconversion_threshold:
        conversion = rain_growth_rate * (cloud_py[i - 1] - autoconversion_threshold)
    else:
        conversion = 0.0

    cloud_py[i] = max(
        cloud_py[i - 1] + cloud_source - conversion - cloud_decay_rate * rain_py[i - 1],
        0.0
    )

    rain_py[i] = max(
        rain_py[i - 1] + conversion - rain_decay_rate * rain_py[i - 1],
        0.0
    )

# --------------------------------------------------
# Overlay comparison plot
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(time_kid, cloud_kid, label="KiD cloud water", linewidth=3)
plt.plot(time_kid, rain_kid, label="KiD rain water", linewidth=3)

plt.plot(time_py, cloud_py, "--", label="Python cloud water")
plt.plot(time_py, rain_py, "--", label="Python rain water")

plt.xlabel("Time (s)")
plt.ylabel("Mass path")
plt.title("Improved KiD vs Python Warm-Cloud Alignment")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("figures/case7_improved_warm_alignment.png", dpi=300)
plt.show()
