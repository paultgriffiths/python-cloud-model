import pandas as pd
import matplotlib.pyplot as plt

# Load results
df_constant = pd.read_csv("data/case2_constant_w1.csv")
df_kid = pd.read_csv("data/case2_kid_effective_w2.csv")

# Remove initial numerical spike
df_constant = df_constant[df_constant["t_s"] > 50]
df_kid = df_kid[df_kid["t_s"] > 50]

plt.figure(figsize=(8, 5))

plt.plot(
    df_constant["t_s"],
    df_constant["R_BF"],
    linewidth=2,
    label="Constant updraft (w = 1.0 m/s)"
)

plt.plot(
    df_kid["t_s"],
    df_kid["R_BF"],
    linewidth=2,
    label="KiD-inspired effective updraft (w = 2.0 m/s)"
)

plt.axhline(
    1.0,
    linestyle="--",
    linewidth=1.5,
    label="R = 1 threshold"
)

plt.xlabel("Time (s)")
plt.ylabel("Bergeron–Findeisen ratio R")
plt.title("Effect of Forcing on Vapour Competition")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("figures/constant_vs_kid_R.png", dpi=300)

plt.show()