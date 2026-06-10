import pandas as pd
import matplotlib.pyplot as plt

old = pd.read_csv("data/original_python_results.csv")
new = pd.read_csv("data/kidlike_python_results.csv")

# Figure 1
plt.figure(figsize=(10,6))

plt.plot(old["time"], old["S"],
         linewidth=2,
         label="Original Python")

plt.plot(new["time"], new["S"],
         linewidth=2,
         label="KiD-like Initialisation")

plt.axhline(0.0, linestyle="--", linewidth=1)

plt.xlabel("Time (s)")
plt.ylabel("Supersaturation (S)")
plt.title("Effect of Initial Thermodynamic Conditions")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig(
    "Effect_of_Initial_Thermodynamic_Conditions_v2.png",
    dpi=600
)

# Figure 2
plt.figure(figsize=(10,6))

plt.plot(old["time"], old["S"],
         linewidth=2,
         label="Original S")

plt.plot(old["time"], old["Sc"],
         linewidth=2,
         label="Original Sc")

plt.plot(new["time"], new["S"],
         linewidth=2,
         label="KiD-like S")

plt.plot(new["time"], new["Sc"],
         linewidth=2,
         label="KiD-like Sc")

plt.xlabel("Time (s)")
plt.ylabel("Supersaturation")
plt.title("Activation Threshold Analysis")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig(
    "Activation_Threshold_Analysis.png",
    dpi=600
)

print("Figures saved successfully")
