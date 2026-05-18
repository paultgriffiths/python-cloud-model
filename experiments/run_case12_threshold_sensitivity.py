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
# Sensitivity thresholds
# --------------------------------------------------

thresholds = [0.35, 0.55, 0.75]

# --------------------------------------------------
# Plot KiD reference
# --------------------------------------------------

plt.plot(
    time,
    cloud_kid,
    linewidth=4,
    label="KiD Cloud Water"
)

# --------------------------------------------------
# Run threshold sensitivity experiments
# --------------------------------------------------

for threshold in thresholds:

    cloud_py = np.zeros_like(time)

    for i in range(1, len(time)):

        t = time[i]

         # cloud growth

        if t < 1200:

            growth = 1.25 * (1.0 - np.exp(-t / 350.0))

            cloud_py[i] = growth


        else:

            cloud_py[i] = max(cloud_py[i-1] - 0.010, 0.0)

        # autoconversion threshold effect
        if cloud_py[i] > threshold:

            cloud_py[i] -= 0.020 * (cloud_py[i] - threshold)

    # plot each threshold
    plt.plot(
        time,
        cloud_py,
        "--",
        label=f"Threshold = {threshold}"
    )

# --------------------------------------------------
# Figure formatting
# --------------------------------------------------

plt.xlabel("Time (s)")
plt.ylabel("Cloud Mass Path")

plt.title("Threshold Sensitivity Study")

plt.legend()

plt.savefig(
    "figures/case12_threshold_sensitivity.png",
)

plt.show()
