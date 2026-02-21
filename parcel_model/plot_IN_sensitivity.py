import pandas as pd
import matplotlib.pyplot as plt

files = [
    ("mixed_phase_N5.csv", "Nice=5"),
    ("mixed_phase_N50.csv", "Nice=50"),
    ("mixed_phase_N500.csv", "Nice=500"),
]

plt.figure()

for fname, label in files:
    df = pd.read_csv(fname)
    plt.plot(df["t_s"], df["qice"], label=label)

plt.xlabel("Time (s)")
plt.ylabel("Ice mass proxy (qice)")
plt.title("Sensitivity of ice growth to IN number")
plt.legend()
plt.tight_layout()
plt.savefig("IN_sensitivity_qice.png", dpi=200)
print("Saved: IN_sensitivity_qice.png")