import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# Time setup
# --------------------------------------------------

dt = 30.0
t_end = 3600

time = np.arange(0, t_end + dt, dt)

# --------------------------------------------------
# Ice nucleation strengths
# --------------------------------------------------

ice_factors = [0.5, 1.0, 2.0]

# --------------------------------------------------
# Plot setup
# --------------------------------------------------

plt.figure(figsize=(9,6))

# --------------------------------------------------
# Sensitivity experiments
# --------------------------------------------------

for factor in ice_factors:

    liquid = np.zeros_like(time)
    ice = np.zeros_like(time)

    for i in range(1, len(time)):

        t = time[i]

        # ------------------------------------------
        # Liquid growth
        # ------------------------------------------

        if t < 1200:

            liquid[i] = 1.2 * (1.0 - np.exp(-t / 400.0))

        else:

            liquid[i] = max(liquid[i-1] - 0.008 * factor, 0.0)

        # ------------------------------------------
        # Ice nucleation onset
        # ------------------------------------------

        if t > 900:

            ice_growth = (
                0.003 * factor *
                (t - 900) / 100.0
            )

            ice[i] = ice[i-1] + ice_growth

            liquid[i] = max(
                liquid[i] - 0.0015 * factor,
                0.0
            )

    # ----------------------------------------------
    # Plot liquid
    # ----------------------------------------------

    plt.plot(
        time,
        liquid,
        label=f"Liquid (IN={factor})"
    )

    # ----------------------------------------------
    # Plot ice
    # ----------------------------------------------

    plt.plot(
        time,
        ice,
        "--",
        label=f"Ice (IN={factor})"
    )

# --------------------------------------------------
# Figure formatting
# --------------------------------------------------

plt.xlabel("Time (s)")
plt.ylabel("Mass Path")

plt.title("Ice Nucleation Sensitivity Study")

plt.legend()

plt.savefig(
    "figures/case15_ice_sensitivity.png",
    dpi=300
)

plt.show()
