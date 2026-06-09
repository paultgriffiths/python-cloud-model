import numpy as np
import matplotlib.pyplot as plt

from parcel_model.kohler import (
    critical_supersaturation,
    critical_supersaturation_classical
)

radii = np.linspace(20e-9, 200e-9, 100)
Dp_values = 2 * radii

sc_kappa = [
    critical_supersaturation(Dp=Dp, kappa=0.3, T=298.15)
    for Dp in Dp_values
]

sc_classical = [
    critical_supersaturation_classical(Dp=Dp, solubility_factor=0.3, T=298.15)
    for Dp in Dp_values
]

plt.figure(figsize=(8, 5))
plt.plot(radii * 1e9, sc_kappa, linewidth=2.5, label="κ-Köhler")
plt.plot(radii * 1e9, sc_classical, "--", linewidth=2.5, label="Classical Köhler-like")

plt.xlabel("Dry particle radius (nm)")
plt.ylabel("Critical supersaturation, Sc")
plt.title("κ-Köhler vs Classical Köhler-like Activation Threshold")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("Kohler_Method_Comparison.png", dpi=600)
print("Saved Kohler_Method_Comparison.png")
