import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

kid = Dataset("/home/dryaktine/KiD-A/output/warm1_output.nc")

time = kid.variables["time"][:]
cloud_kid = kid.variables["cloud_mass_path"][:]

aerosol_factors = [0.5, 1.0, 2.0]

cloud_threshold = 0.55
autoconv_rate = 0.020

plt.plot(time, cloud_kid, linewidth=4, label="KiD Cloud Water")

for aerosol_factor in aerosol_factors:

    cloud_py = np.zeros_like(time)

    for i in range(1, len(time)):

        t = time[i]

        if t < 1200:
            growth = 1.25 * aerosol_factor * (1.0 - np.exp(-t / 350.0))
            cloud_py[i] = growth
        else:
            cloud_py[i] = max(cloud_py[i-1] - 0.010, 0.0)

        if cloud_py[i] > cloud_threshold:
            conversion = autoconv_rate * (cloud_py[i] - cloud_threshold)
            cloud_py[i] -= conversion

    plt.plot(time, cloud_py, "--", label=f"Aerosol factor = {aerosol_factor}")

plt.xlabel("Time (s)")
plt.ylabel("Cloud Mass Path")
plt.title("Aerosol Sensitivity Study")
plt.legend()

plt.savefig("figures/case14_aerosol_sensitivity.png", dpi=300)
plt.show()
