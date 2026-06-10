import numpy as np
import matplotlib.pyplot as plt

from parcel_model.arg_activation import (
    lognormal_activation_fraction
)

Sc = 0.002296
sigma_g = 1.6

Smax_values = np.linspace(
    0.0005,
    0.006,
    300
)

fractions = [
    lognormal_activation_fraction(
        S,
        Sc,
        sigma_g
    )
    for S in Smax_values
]

plt.figure(figsize=(10,6))

plt.plot(
    Smax_values,
    100*np.array(fractions),
    linewidth=3
)

plt.axvline(
    Sc,
    linestyle="--",
    label="Median Sc"
)

plt.xlabel("Maximum Supersaturation (Smax)")
plt.ylabel("Activated Fraction (%)")

plt.title(
    "Lognormal Aerosol Activation Response"
)

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "ARG_Activation_Response.png",
    dpi=600
)

plt.show()
