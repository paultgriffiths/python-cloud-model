import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)

df = pd.read_csv("data/case3_literature_benchmark.csv")

# 1) Bergeron-Findeisen ratio
plt.figure(figsize=(8, 5))
plt.plot(df["t_s"], df["R_BF"], linewidth=2)
plt.axhline(1.0, linestyle="--", linewidth=1.5, label="R = 1 threshold")
plt.xlabel("Time (s)")
plt.ylabel("Bergeron-Findeisen ratio R")
plt.title("Case 3: Bergeron-Findeisen Ratio")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("figures/case3_literature_benchmark_R.png", dpi=300)
plt.show()

# 2) Liquid and ice mass mixing
plt.figure(figsize=(8, 5))
plt.plot(df["t_s"], df["qcloud"], linewidth=2, label="Liquid cloud water")
plt.plot(df["t_s"], df["qice"], linewidth=2, label="Ice")
plt.xlabel("Time (s)")
plt.ylabel("Mass mixing ratio")
plt.title("Case 3: Liquid and Ice Evolution")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("figures/case3_literature_benchmark_liquid_ice.png", dpi=300)
plt.show()

# 3) Supersaturation
plt.figure(figsize=(8, 5))
plt.plot(df["t_s"], df["Sw"], linewidth=2, label="Sw")
plt.plot(df["t_s"], df["Si"], linewidth=2, label="Si")
plt.xlabel("Time (s)")
plt.ylabel("Supersaturation")
plt.title("Case 3: Supersaturation Evolution")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("figures/case3_literature_benchmark_supersaturation.png", dpi=300)
plt.show()

print("Case 3 plots generated successfully.")