import pandas as pd
import matplotlib.pyplot as plt

old = pd.read_csv("data/original_python_results.csv")
new = pd.read_csv("data/kidlike_python_results.csv")

# Figure 1: Supersaturation
plt.figure(figsize=(8,5))
plt.plot(old["time"], old["S"], label="Original Python")
plt.plot(new["time"], new["S"], label="KiD-like Python")
plt.xlabel("Time (s)")
plt.ylabel("Supersaturation (S)")
plt.title("Original vs KiD-like Initial Conditions")
plt.legend()
plt.grid(True)
plt.savefig("S_comparison.png", dpi=300)
plt.show()

# Figure 2: Activated droplets
plt.figure(figsize=(8,5))
plt.plot(old["time"], old["n_droplets"], label="Original Python")
plt.plot(new["time"], new["n_droplets"], label="KiD-like Python")
plt.xlabel("Time (s)")
plt.ylabel("Activated droplets")
plt.title("Activated Droplets Comparison")
plt.legend()
plt.grid(True)
plt.savefig("droplets_comparison.png", dpi=300)
plt.show()
