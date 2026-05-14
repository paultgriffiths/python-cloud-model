import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# --------------------------------------------------
# Read KiD benchmark
# --------------------------------------------------

kid = Dataset("/home/dryaktine/KiD-A/output/warm1_output.nc")

time = kid.variables["time"][:]
cloud_kid = kid.variables["cloud_mass_path"][:]

# --------------------------------------------------
# Updraft sensitivity values
# --------------------------------------------------

updrafts = [1.0, 2.0, 4.0]

cloud_threshold = 0.55
autoconv_rate = 0.020

# --------------------------------------------------
# Plot KiD reference
# --------------------------------------------------

plt.plot(time, cloud_kid, linewidth=4, label="KiD Cloud Water")

# --------------------------------------------------
# Run updraft sensitivity experiments
# --------------------------------------------------

for w in updrafts:

    cloud_py = np.zeros_like(time)

    for i in range(1, len(time)):

        t = time[i]

        if t < 1200:
            growth = (1.25 * w / 2.0) * (1.0 - np.exp(-t / 350.0))
            cloud_py[i] = growth
        else:
            cloud_py[i] = max(cloud_py[i-1] - 0.010, 0.0)

        if cloud_py[i] > cloud_threshold:
            conversion = autoconv_rate * (cloud_py[i] - cloud_threshold)
            cloud_py[i] -= conversion

    plt.plot(time, cloud_py, "--", label=f"w = {w} m/s")

# --------------------------------------------------
# Figure formatting
# --------------------------------------------------

plt.xlabel("Time (s)")
plt.ylabel("Cloud Mass Path")
plt.title("Updraft Sensitivity Study")
plt.legend()

plt.savefig("figures/case13_updraft_sensitivity.png", dpi=300)
plt.show()
