import pandas as pd
import matplotlib.pyplot as plt

# Load results
df_constant = pd.read_csv("data/case2_constant_w1.csv")
df_kid = pd.read_csv("data/case2_kid_effective_w2.csv")

plt.figure(figsize=(8, 5))

# Constant forcing
plt.plot(
    df_constant["t_s"],
    df_constant["Sw"],
    linewidth=2,
    label="Sw - constant forcing"
)

plt.plot(
    df_constant["t_s"],
    df_constant["Si"],
    linewidth=2,
    linestyle="--",
    label="Si - constant forcing"
)

# KiD-inspired forcing
plt.plot(
    df_kid["t_s"],
    df_kid["Sw"],
    linewidth=2,
    label="Sw - KiD-inspired forcing"
)

plt.plot(
    df_kid["t_s"],
    df_kid["Si"],
    linewidth=2,
    linestyle="--",
    label="Si - KiD-inspired forcing"
)

plt.xlabel("Time (s)")
plt.ylabel("Supersaturation")
plt.title("Effect of Forcing on Supersaturation Evolution")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "figures/constant_vs_kid_supersaturation.png",
    dpi=300
)

plt.show()