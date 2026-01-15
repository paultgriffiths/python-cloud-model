from aerosol import AerosolPopulation
from activation import check_activation

# Create two aerosol populations
sulfate = AerosolPopulation(
    name="sulfate",
    N=500e6,        # m^-3 (example)
    radius=30e-9,
    kappa=1.0,
    rho_p=1770.0
)

pollen = AerosolPopulation(
    name="pollen",
    N=1000.0,       # m^-3
    radius=5e-6,
    kappa=0.1,
    rho_p=1000.0
)

# Try a few supersaturation values
for S in [1e-7, 1e-6, 1e-5, 1e-4]:
    act_s, Sc_s = check_activation(S, sulfate)
    act_p, Sc_p = check_activation(S, pollen)

    print("\nS =", S)
    print("  Sulfate: activated =", act_s, " Sc =", Sc_s)
    print("  Pollen : activated =", act_p, " Sc =", Sc_p)
