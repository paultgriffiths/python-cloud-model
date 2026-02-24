import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("mixed_phase_maxwell_timeseries.csv")

T = df["T_K"]
Sw = df["Sw"]
Si = df["Si"]
qcloud = df["qcloud"]
qice = df["qice"]

# Supersaturation vs Temperature
plt.figure()
plt.plot(T, Sw, label="Sw (liquid)")
plt.plot(T, Si, label="Si (ice)")
plt.xlabel("Temperature (K)")
plt.ylabel("Supersaturation")
plt.title("Supersaturation vs Temperature (Maxwell)")
plt.legend()
plt.gca().invert_xaxis()
plt.tight_layout()
plt.savefig("maxwell_S_vs_T.png", dpi=200)
print("Saved: maxwell_S_vs_T.png")

# Mass vs Temperature
plt.figure()
plt.plot(T, qcloud, label="qcloud")
plt.plot(T, qice, label="qice")
plt.xlabel("Temperature (K)")
plt.ylabel("Water mass (kg/m^3)")
plt.title("Liquid vs Ice mass vs Temperature (Maxwell)")
plt.legend()
plt.gca().invert_xaxis()
plt.tight_layout()
plt.savefig("maxwell_q_vs_T.png", dpi=200)
print("Saved: maxwell_q_vs_T.png")