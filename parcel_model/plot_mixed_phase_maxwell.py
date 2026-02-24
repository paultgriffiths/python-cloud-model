import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("mixed_phase_maxwell_timeseries.csv")

t = df["t_s"]
qcloud = df["qcloud"]
qice   = df["qice"]
Ncloud = df["Ncloud"]
Nice   = df["Nice"]

# qcloud vs qice
plt.figure()
plt.plot(t, qcloud, label="qcloud (liquid)")
plt.plot(t, qice,   label="qice (ice)")
plt.xlabel("Time (s)")
plt.ylabel("Water mass proxy (kg/m^3)")
plt.title("Mixed-phase parcel: liquid vs ice mass (Maxwell)")
plt.legend()
plt.tight_layout()
plt.savefig("maxwell_qcloud_qice_vs_time.png", dpi=200)
print("Saved: maxwell_qcloud_qice_vs_time.png")

# Ncloud vs Nice
plt.figure()
plt.plot(t, Ncloud, label="Ncloud (droplets)")
plt.plot(t, Nice,   label="Nice (ice)")
plt.xlabel("Time (s)")
plt.ylabel("Number concentration (m^-3)")
plt.title("Mixed-phase parcel: droplet vs ice number (Maxwell)")
plt.legend()
plt.tight_layout()
plt.savefig("maxwell_Ncloud_Nice_vs_time.png", dpi=200)
print("Saved: maxwell_Ncloud_Nice_vs_time.png")