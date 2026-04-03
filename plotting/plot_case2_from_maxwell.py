import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)

df = pd.read_csv("data/case2_from_maxwell.csv")

# 1) Liquid and ice
plt.figure()
plt.plot(df["t_s"], df["qcloud"], label="liquid")
plt.plot(df["t_s"], df["qice"], label="ice")
plt.xlabel("Time (s)")
plt.ylabel("Mass concentration")
plt.title("Case 2 from Maxwell: Liquid and Ice")
plt.legend()
plt.savefig("figures/case2_from_maxwell_liquid_ice.png", dpi=200, bbox_inches="tight")
plt.close()

# 2) R ratio
plt.figure()
plt.plot(df["t_s"], df["R_BF"])
plt.axhline(1.0, linestyle="--")
plt.xlabel("Time (s)")
plt.ylabel("R = dep_sink / cond_sink")
plt.title("Case 2 from Maxwell: Bergeron-Findeisen Ratio")
plt.savefig("figures/case2_from_maxwell_R.png", dpi=200, bbox_inches="tight")
plt.close()

# 3) Supersaturation
plt.figure()
plt.plot(df["t_s"], df["Sw"], label="Sw")
plt.plot(df["t_s"], df["Si"], label="Si")
plt.xlabel("Time (s)")
plt.ylabel("Supersaturation")
plt.title("Case 2 from Maxwell: Supersaturation")
plt.legend()
plt.savefig("figures/case2_from_maxwell_S.png", dpi=200, bbox_inches="tight")
plt.close()

# 4) Vapour sinks
plt.figure()
plt.plot(df["t_s"], df["cond_sink_kgm3s"], label="cond_sink")
plt.plot(df["t_s"], df["dep_sink_kgm3s"], label="dep_sink")
plt.xlabel("Time (s)")
plt.ylabel("Positive vapour sink")
plt.title("Case 2 from Maxwell: Vapour Sinks")
plt.legend()
plt.savefig("figures/case2_from_maxwell_sinks.png", dpi=200, bbox_inches="tight")
plt.close()

print("Plots saved in figures/")