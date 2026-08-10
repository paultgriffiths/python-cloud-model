import pandas as pd
import matplotlib.pyplot as plt

# Read results
df = pd.read_csv("data/persistent_Nc_results.csv")

# Convert Nc to cm^-3 for easier interpretation
Nc_cm3 = df["n_droplets"] / 1.0e6

# Create figure
fig, axes = plt.subplots(3, 1, figsize=(9, 10), sharex=True)

# 1. Supersaturation
axes[0].plot(df["time"], df["S"])
axes[0].axhline(0.0, linestyle="--")
axes[0].set_ylabel("Supersaturation S")
axes[0].set_title("Persistent Nc and Maxwell Evaporation Test")
axes[0].grid(True)

# 2. Droplet number
axes[1].plot(df["time"], Nc_cm3)
axes[1].set_ylabel("Nc (cm$^{-3}$)")
axes[1].grid(True)

# 3. Cloud water
axes[2].plot(df["time"], df["cloud_mass"])
axes[2].set_ylabel("qc (kg kg$^{-1}$)")
axes[2].set_xlabel("Time (s)")
axes[2].grid(True)

plt.tight_layout()

output = "Persistent_Nc_Maxwell_Evaporation.png"
plt.savefig(output, dpi=300)

print(f"Saved {output}")
