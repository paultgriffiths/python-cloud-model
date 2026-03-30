import matplotlib.pyplot as plt

# Data from timestep sensitivity tests
dt = [0.01, 0.1, 1.0, 2.0, 5.0, 10.0]
r_final = [1.17e-05, 1.18e-05, 1.20e-05, 1.20e-05, 1.20e-05, 1.20e-05]

plt.figure(figsize=(8, 5))
plt.plot(dt, r_final, marker="o")

plt.xlabel("Timestep dt (s)")
plt.ylabel("Final ice radius (m)")
plt.title("Sensitivity of final ice radius to timestep")
plt.xscale("log")

plt.savefig("figures/figure_dt_sensitivity.png", dpi=300, bbox_inches="tight")
plt.show()