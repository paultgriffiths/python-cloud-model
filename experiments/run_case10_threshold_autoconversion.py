import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# --------------------------------------------------
# Read KiD benchmark data
# --------------------------------------------------

kid = Dataset("/home/dryaktine/KiD-A/output/warm1_output.nc")

time_kid = kid.variables["time"][:]
cloud_kid = kid.variables["cloud_mass_path"][:]
rain_kid = kid.variables["rain_mass_path"][:]

# --------------------------------------------------
# Python warm-rain alignment model
# --------------------------------------------------

time_py = time_kid

cloud_py = np.zeros_like(time_py, dtype=float)
rain_py = np.zeros_like(time_py, dtype=float)

# --------------------------------------------------
# Physical parameters
# --------------------------------------------------

cloud_threshold = 0.55
autoconv_rate = 0.020

# --------------------------------------------------
# Time integration
# --------------------------------------------------

for i in range(1, len(time_py)):

    t = time_py[i]

    # ----------------------------------------------
    # Cloud growth phase
    # ----------------------------------------------

    if t < 1200:

        growth = 1.25 * (1.0 - np.exp(-t / 350.0))

        cloud_py[i] = growth

    else:

        cloud_py[i] = max(cloud_py[i-1] - 0.010, 0.0)

    # ----------------------------------------------
    # Threshold-based autoconversion
    # ----------------------------------------------

    if cloud_py[i] > cloud_threshold:

        conversion = autoconv_rate * (cloud_py[i] - cloud_threshold)

        cloud_py[i] -= conversion

        rain_py[i] = rain_py[i-1] + conversion

    else:

        rain_py[i] = rain_py[i-1]

# --------------------------------------------------
# Plot comparison
# --------------------------------------------------

plt.plot(time_kid, cloud_kid,
         label="KiD Cloud Water",
         linewidth=3)

plt.plot(time_kid, rain_kid,
         label="KiD Rain Water",
         linewidth=3)

plt.plot(time_py, cloud_py,
         "--",
         label="Python Cloud Water")

plt.plot(time_py, rain_py,
         "--",
         label="Python Rain Water")

plt.xlabel("Time (s)")
plt.ylabel("Mass Path")

plt.title("Threshold-Based Warm-Rain Autoconversion")

plt.legend()

plt.savefig(
    "figures/case10_threshold_autoconversion.png",
    dpi=300
)

plt.show()
