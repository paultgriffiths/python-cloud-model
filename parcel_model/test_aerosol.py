from aerosol import AerosolPopulation

pollen = AerosolPopulation(
    name="pollen",
    N=1000.0,
    radius=5e-6,
    kappa=0.1,
    rho_p=1000.0
)

print("Name:", pollen.name)
print("N:", pollen.N)
print("Radius (m):", pollen.radius)
print("Kappa:", pollen.kappa)
print("Activated:", pollen.activated)
