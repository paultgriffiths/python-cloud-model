import matplotlib.pyplot as plt

# Data from timestep sensitivity tests
dt = [0.01, 0.1, 1.0]
r_final = [1.17e-05, 1.18e-05, 1.20e-05]

# Create plot
plt.figure(figsize=(8, 5))
plt.plot(dt, r_final, marker="o")

# Labels and title
plt.xlabel("Timestep dt (s)")
plt.ylabel("Final ice radius (m)")
plt.title("Sensitivity of final ice radius to timestep")

# Use log scale on x-axis
plt.xscale("log")

# Save figure
plt.savefig("figures/figure_dt_sensitivity.png", dpi=300, bbox_inches="tight")

# Show figure
plt.show()