from parcel_model.arg_activation import lognormal_activation_fraction

Sc = 0.002296
sigma_g = 1.6

for Smax in [0.001, 0.002, 0.003, 0.005]:
    frac = lognormal_activation_fraction(
        Smax,
        Sc,
        sigma_g
    )

    print(
        f"Smax={Smax:.4f}  "
        f"fraction={frac:.3f}"
    )
