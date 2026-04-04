import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# make sure figures folder exists
os.makedirs("figures", exist_ok=True)

# load data
df = pd.read_csv("data/case2_from_maxwell.csv")

# basic variables
t = df["t_s"]
qcloud = df["qcloud"]
qice = df["qice"]
Sw = df["Sw"]
Si = df["Si"]

# use the correct column names from your CSV
cond_sink = df["cond_sink_kgm3s"]
dep_sink = df["dep_sink_kgm3s"]

# ---------------------------------
# CLEAN Bergeron-Findeisen ratio R
# ---------------------------------
R = np.zeros(len(df))

threshold = 1e-12  # avoid division by very small numbers
mask = cond_sink > threshold

R[mask] = dep_sink[mask] / cond_sink[mask]

# ---------------------------------
# 1) Liquid and Ice mass
# ---------------------------------
plt.figure()
plt.plot(t, qcloud, label="liquid")
plt.plot(t, qice, label="ice")
plt.xlabel("Time (s)")
plt.ylabel("Mass concentration")
plt.title("Case 2 from Maxwell: Liquid and Ice")
plt.legend()
plt.savefig("figures/case2_from_maxwell_liquid_ice.png", dpi=200, bbox_inches="tight")
plt.close()

# ---------------------------------
# 2) Bergeron-Findeisen ratio
# ---------------------------------
plt.figure()
plt.plot(t, R, label="R")
plt.axhline(1.0, linestyle="--", label="R = 1 threshold")
plt.xlabel("Time (s)")
plt.ylabel("R = dep_sink / cond_sink")
plt.title("Case 2 from Maxwell: Bergeron-Findeisen Ratio")
plt.legend()
plt.savefig("figures/case2_from_maxwell_R.png", dpi=200, bbox_inches="tight")
plt.close()

# ---------------------------------
# 3) Supersaturation
# ---------------------------------
plt.figure()
plt.plot(t, Sw, label="Sw")
plt.plot(t, Si, label="Si")
plt.xlabel("Time (s)")
plt.ylabel("Supersaturation")
plt.title("Case 2 from Maxwell: Supersaturation")
plt.legend()
plt.savefig("figures/case2_from_maxwell_S.png", dpi=200, bbox_inches="tight")
plt.close()

# ---------------------------------
# 4) Vapour sinks
# ---------------------------------
plt.figure()
plt.plot(t, cond_sink, label="cond_sink")
plt.plot(t, dep_sink, label="dep_sink")
plt.xlabel("Time (s)")
plt.ylabel("Positive vapour sink")
plt.title("Case 2 from Maxwell: Vapour Sinks")
plt.legend()
plt.savefig("figures/case2_from_maxwell_sinks.png", dpi=200, bbox_inches="tight")
plt.close()

print("Plots generated successfully.")