import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)

df = pd.read_csv("data/case4_kid_mixed1_alignment.csv")

# 1) Bergeron-Findeisen ratio
plt.figure(figsize=(8, 5))
plt.plot(df["t_s"], df["R_BF"], linewidth=2)
plt.axhline(1.0, linestyle="--", linewidth=1.5, label="R = 1 threshold")
plt.xlabel("Time (s)")
plt.ylabel("Bergeron-Findeisen ratio R")
plt.title("Case 4: KiD Mixed1 Alignment - BF Ratio")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("figures/case4_kid_mixed1_alignment_R.png", dpi=300)
plt.close()

# 2) Liquid and ice mass
plt.figure(figsize=(8, 5))
plt.plot(df["t_s"], df["qcloud"], linewidth=2, label="Liquid cloud water")
plt.plot(df["t_s"], df["qice"], linewidth=2, label="Ice")
plt.xlabel("Time (s)")
plt.ylabel("Mass mixing ratio")
plt.title("Case 4: KiD Mixed1 Alignment - Liquid and Ice")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("figures/case4_kid_mixed1_alignment_liquid_ice.png", dpi=300)
plt.close()

# 3) Supersaturation
plt.figure(figsize=(8, 5))
plt.plot(df["t_s"], df["Sw"], linewidth=2, label="Sw")
plt.plot(df["t_s"], df["Si"], linewidth=2, label="Si")
plt.xlabel("Time (s)")
plt.ylabel("Supersaturation")
plt.title("Case 4: KiD Mixed1 Alignment - Supersaturation")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("figures/case4_kid_mixed1_alignment_supersaturation.png", dpi=300)
plt.close()

print("Case 4 KiD mixed1 alignment plots generated successfully.")