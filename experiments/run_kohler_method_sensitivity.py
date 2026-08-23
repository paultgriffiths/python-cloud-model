import os
import pandas as pd

from parcel_model.kohler import (
    critical_supersaturation,
    critical_supersaturation_classical,
)

os.makedirs("data", exist_ok=True)

# Dry particle diameters [m]
diameters_nm = [20, 30, 50, 75, 100, 150, 200, 300]

# Hygroscopicity values for kappa-Kohler
kappa_values = [0.1, 0.3, 0.6, 1.0]

T = 283.15

results = []

for D_nm in diameters_nm:
    Dp = D_nm * 1e-9

    for kappa in kappa_values:

        Sc_kappa = critical_supersaturation(
            Dp=Dp,
            kappa=kappa,
            T=T,
        )

        # For this implementation, using the same numerical
        # coefficient allows a direct mathematical comparison
        # between the two implemented formulations.
        Sc_classical = critical_supersaturation_classical(
            Dp=Dp,
            solubility_factor=kappa,
            T=T,
        )

        results.append({
            "Dp_nm": D_nm,
            "kappa": kappa,
            "T_K": T,
            "Sc_kappa_fraction": Sc_kappa,
            "Sc_kappa_percent": 100.0 * Sc_kappa,
            "Sc_classical_fraction": Sc_classical,
            "Sc_classical_percent": 100.0 * Sc_classical,
            "classical_over_kappa": (
                Sc_classical / Sc_kappa
                if Sc_kappa > 0
                else float("nan")
            ),
            "absolute_difference_percent": (
                100.0 * abs(Sc_classical - Sc_kappa)
            ),
        })

df = pd.DataFrame(results)

outfile = "data/kohler_method_sensitivity.csv"
df.to_csv(outfile, index=False)

print()
print("## KAPPA-KOHLER VS SIMPLIFIED CLASSICAL KOHLER")
print("T =", T, "K")
print()
print(df.to_string(index=False))
print()
print("Saved:", outfile)
