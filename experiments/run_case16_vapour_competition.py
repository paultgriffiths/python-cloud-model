import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# Time setup
# --------------------------------------------------

dt = 30.0
t_end = 3600

time = np.arange(0, t_end + dt, dt)

# --------------------------------------------------
# Mixed-phase fields
# --------------------------------------------------

liquid = np.zeros_like(time)
ice = np.zeros_like(time)
R_BF = np.zeros_like(time)

# --------------------------------------------------
# Ice nucleation strength
# --------------------------------------------------

ice_factor = 1.0

# --------------------------------------------------
# Time integration
# --------------------------------------------------

for i in range(1, len(time)):

    t = time[i]

    # Liquid growth before mixed-phase transition
    if t < 1200:
        liquid[i] = 1.2 * (1.0 - np.exp(-t / 400.0))
    else:
        liquid[i] = max(liquid[i-1] - 0.008 * ice_factor, 0.0)

    # Ice nucleation and growth
    if t > 900:
        ice_growth = 0.003 * ice_factor * (t - 900) / 100.0
        ice[i] = ice[i-1] + ice_growth
        liquid[i] = max(liquid[i] - 0.0015 * ice_factor, 0.0)

    # Bergeron-Findeisen-type ratio
    if liquid[i] > 1e-8:
        R_BF[i] = ice[i] / liquid[i]
    else:
        R_BF[i] = np.nan

# --------------------------------------------------
# Plot
# --------------------------------------------------

plt.plot(time, R_BF, label="R_BF = Ice / Liquid")
plt.axhline(1.0, linestyle="--", label="R_BF = 1 threshold")

plt.xlabel("Time (s)")
plt.ylabel("Competition Ratio")
plt.title("Vapour Competition Diagnostic")

plt.legend()

plt.savefig("figures/case16_vapour_competition.png", dpi=300)

plt.show()
