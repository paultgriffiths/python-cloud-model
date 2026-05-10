import pandas as pd
import matplotlib.pyplot as plt

# Load data
df_constant = pd.read_csv("data/case2_constant_w1.csv")
df_kid = pd.read_csv("data/case2_kid_effective_w2.csv")

# Remove initial numerical spike
df_constant = df_constant[df_constant["t_s"] > 50]
df_kid = df_kid[df_kid["t_s"] > 50]

# Find first time where R >= 1
constant_transition = df_constant[df_constant["R_BF"] >= 1]
kid_transition = df_kid[df_kid["R_BF"] >= 1]

t_constant = constant_transition["t_s"].iloc[0] if not constant_transition.empty else None
t_kid = kid_transition["t_s"].iloc[0] if not kid_transition.empty else None

# Use a visible placeholder for "No transition"
max_time = max(df_constant["t_s"].max(), df_kid["t_s"].max())

cases = ["Constant forcing", "KiD-inspired forcing"]
times = [
    t_constant if t_constant is not None else 0,
    t_kid if t_kid is not None else max_time
]

labels = [
    f"{int(t_constant)} s" if t_constant is not None else "No transition",
    f"{int(t_kid)} s" if t_kid is not None else "No transition"
]

plt.figure(figsize=(8, 6))

bars = plt.bar(cases, times)

plt.ylabel("Time (s)")
plt.title("Timing of Bergeron–Findeisen Transition")

for bar, label in zip(bars, labels):
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 80,
        label,
        ha="center",
        va="bottom"
    )

plt.ylim(0, max_time * 1.15)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout(pad=2.0)

plt.savefig("figures/BF_transition_timing.png", dpi=300)
plt.show()