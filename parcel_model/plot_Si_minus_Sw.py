import pandas as pd
import matplotlib.pyplot as plt

# read simulation output
df = pd.read_csv("mixed_phase_maxwell_timeseries.csv")

T = df["T_K"]
Sw = df["Sw"]
Si = df["Si"]

deltaS = Si - Sw

plt.figure()

plt.plot(T, deltaS, label="Si - Sw")

plt.axhline(0, linestyle="--")

plt.xlabel("Temperature (K)")
plt.ylabel("Supersaturation difference")
plt.title("Thermodynamic driver of the Bergeron-Findeisen process")

plt.gca().invert_xaxis()

plt.legend()

plt.tight_layout()

plt.savefig("Si_minus_Sw_vs_T.png", dpi=300)

print("Saved: Si_minus_Sw_vs_T.png")