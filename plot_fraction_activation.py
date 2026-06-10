import numpy as np
import matplotlib.pyplot as plt

Sc = 0.002296

S = np.linspace(0, 0.006, 500)

fraction = np.zeros_like(S)

fraction[S >= 2*Sc] = 1.0

mask = (S >= Sc) & (S < 2*Sc)

fraction[mask] = (S[mask] - Sc)/Sc

plt.figure(figsize=(8,5))

plt.plot(S, fraction, linewidth=3)

plt.axvline(Sc, linestyle="--", label="Sc")
plt.axvline(2*Sc, linestyle="--", label="2Sc")

plt.xlabel("Supersaturation S")
plt.ylabel("Activated Fraction")
plt.title("Prototype Fraction Activation Scheme")

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "Fraction_Activation_Prototype.png",
    dpi=600
)

print("Saved")
