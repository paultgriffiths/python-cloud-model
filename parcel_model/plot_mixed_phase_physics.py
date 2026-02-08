import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("mixed_phase_physics_timeseries.csv")

t  = data["t_s"]
T  = data["T_K"]
Sw = data["Sw"]
Si = data["Si"]
qi = data["qi_proxy"]
Cl = data["Cl_Pa_per_s"]
Ci = data["Ci_Pa_per_s"]

# Figure 1: Temperature vs time
plt.figure()
plt.plot(t, T)
plt.xlabel("Time (s)")
plt.ylabel("Temperature (K)")
plt.title("Parcel temperature vs time")
plt.tight_layout()
plt.savefig("temperature_vs_time.png", dpi=200)
print("Saved: temperature_vs_time.png")

# Figure 2: Supersaturation
plt.figure()
plt.plot(t, Sw, label="Sw (liquid)")
plt.plot(t, Si, label="Si (ice)")
plt.xlabel("Time (s)")
plt.ylabel("Supersaturation")
plt.title("Supersaturation vs time")
plt.legend()
plt.tight_layout()
plt.savefig("supersaturation_vs_time.png", dpi=200)
print("Saved: supersaturation_vs_time.png")

# Figure 3: Ice growth
plt.figure()
plt.plot(t, qi)
plt.xlabel("Time (s)")
plt.ylabel("qi (ice proxy)")
plt.title("Ice growth vs time")
plt.tight_layout()
plt.savefig("ice_growth_vs_time.png", dpi=200)
print("Saved: ice_growth_vs_time.png")

# Figure 4: Vapour budget
plt.figure()
plt.plot(t, Cl, label="Liquid tendency")
plt.plot(t, Ci, label="Ice tendency")
plt.xlabel("Time (s)")
plt.ylabel("Vapour tendency (Pa/s)")
plt.title("Vapour budget: liquid vs ice")
plt.legend()
plt.tight_layout()
plt.savefig("vapour_budget_tendencies.png", dpi=200)
print("Saved: vapour_budget_tendencies.png")
