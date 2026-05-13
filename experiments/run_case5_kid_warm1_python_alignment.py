import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# KiD-inspired warm cloud alignment experiment
# --------------------------------------------------

dt = 1.0                 # timestep [s]
t_end = 3600             # total simulation time [s]
w = 2.0                  # updraft velocity [m/s]

# Time array
time = np.arange(0, t_end + dt, dt)

# Simplified cloud/rain evolution
cloud = np.zeros_like(time, dtype=float)
rain = np.zeros_like(time, dtype=float)

# --------------------------------------------------
# Simple conceptual warm-cloud evolution
# --------------------------------------------------

for i in range(1, len(time)):

    t = time[i]

    # cloud growth phase
    if t < 1200:
        cloud[i] = cloud[i-1] + 0.0015 * w

    # conversion to rain
    else:
        cloud[i] = max(cloud[i-1] - 0.0008 * w, 0.0)
        rain[i] = rain[i-1] + 0.0012 * w

# --------------------------------------------------
# Plot
# --------------------------------------------------

plt.plot(time, cloud, label="Python Cloud Water")
plt.plot(time, rain, label="Python Rain Water")

plt.xlabel("Time (s)")
plt.ylabel("Mass Path")
plt.title("KiD-inspired Warm Cloud Alignment")

plt.legend()

plt.savefig("figures/case5_kid_alignment.png", dpi=300)

plt.show()

