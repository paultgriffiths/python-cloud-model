import pandas as pd
import matplotlib.pyplot as plt

# Load KiD-inspired forcing output
df = pd.read_csv("data/kid_inspired_alignment.csv")

# Plot updraft forcing
plt.figure(figsize=(8, 5))
plt.plot(df["time_s"], df["w_mps"], linewidth=2)
plt.xlabel("Time (s)")
plt.ylabel("Updraft velocity (m/s)")
plt.title("KiD-inspired prescribed updraft forcing")
plt.grid(True)
plt.tight_layout()

plt.savefig("figures/kid_inspired_updraft.png", dpi=300)
plt.show()