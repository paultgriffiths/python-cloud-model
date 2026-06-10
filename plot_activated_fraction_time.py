import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/kid_case1_results.csv")

plt.figure(figsize=(10,6))
plt.plot(df["time"], 100 * df["activated_fraction"], linewidth=3)

plt.xlabel("Time (s)")
plt.ylabel("Activated fraction (%)")
plt.title("Activated Fraction vs Time")
plt.grid(True)

plt.tight_layout()
plt.savefig("Activated_Fraction_vs_Time.png", dpi=600)
plt.show()
