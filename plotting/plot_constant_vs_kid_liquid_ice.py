import pandas as pd
import matplotlib.pyplot as plt

# Load results
df_constant = pd.read_csv("data/case2_constant_w1.csv")
df_kid = pd.read_csv("data/case2_kid_effective_w2.csv")

plt.figure(figsize=(8, 5))

# Constant forcing
plt.plot(
    df_constant["t_s"],
    df_constant["qcloud"],
    linewidth=2,
    label="Liquid - constant forcing"
)

plt.plot(
    df_constant["t_s"],
    df_constant["qice"],
    linewidth=2,
    linestyle="--",
    label="Ice - constant forcing"
)

# KiD-inspired forcing
plt.plot(
    df_kid["t_s"],
    df_kid["qcloud"],
    linewidth=2,
    label="Liquid - KiD-inspired forcing"
)

plt.plot(
    df_kid["t_s"],
    df_kid["qice"],
    linewidth=2,
    linestyle="--",
    label="Ice - KiD-inspired forcing"
)

plt.xlabel("Time (s)")
plt.ylabel("Mixing ratio (kg/kg)")
plt.title("Effect of Forcing on Liquid and Ice Water")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("figures/constant_vs_kid_liquid_ice.png", dpi=300)
plt.show()