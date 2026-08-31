import math

from parcel_model.abdul_razzak_1998 import (
    R, Mw, rho_w, Lv,
    ARGAerosolMode,
    ammonium_sulfate_B,
    curvature_A,
    critical_supersaturation_ARG,
    alpha_coefficient,
    gamma_coefficient,
    growth_coefficient_ARG1998,
    smax_ARG_single,
    activated_fraction_ARG,
)


# ---------------------------------------------------------
# Abdul-Razzak et al. (1998) Figure-5 benchmark conditions
# ---------------------------------------------------------

T = 283.15
p = 80000.0
ps = 1226.0
V = 5.0

N = 200e6
am = 0.01e-6
sigma = 2.5

# Water-vapour diffusivity using the temperature/pressure scaling
# already used elsewhere in this project.
D0 = 2.11e-5
Dv = D0 * (T / 273.15) ** 1.94 * (101325.0 / p)

Ka = 0.0249

# IAPWS surface-tension correlation for pure water.
Tc = 647.096
tau = 1.0 - T / Tc
sigma_w = 235.8e-3 * tau**1.256 * (1.0 - 0.625 * tau)

# Published reference quantities
Sm_ref = 1.762e-2
eta_ref = 4.037e-4
zeta_ref = 3.966e-6


print()
print("=" * 65)
print("ABDUL-RAZZAK ET AL. (1998) VALIDATION")
print("=" * 65)


# ---------------------------------------------------------
# 1. Aerosol composition and critical supersaturation
# ---------------------------------------------------------

B = ammonium_sulfate_B()

A = curvature_A(T, sigma_w=sigma_w)

Sm = critical_supersaturation_ARG(
    am,
    A,
    B,
)

print()
print("1. CRITICAL SUPERSATURATION")
print("---------------------------")
print("A =", A)
print("B =", B)
print("Sm model =", Sm)
print("Sm paper =", Sm_ref)
print("model/paper =", Sm / Sm_ref)
print("relative difference (%) =", 100.0 * (Sm / Sm_ref - 1.0))


# ---------------------------------------------------------
# 2. Thermodynamic coefficients
# ---------------------------------------------------------

alpha = alpha_coefficient(T)
gamma = gamma_coefficient(T, p, ps)

print()
print("2. THERMODYNAMIC COEFFICIENTS")
print("-----------------------------")
print("alpha =", alpha)
print("gamma =", gamma)


# ---------------------------------------------------------
# 3. Continuum and size-dependent growth coefficients
# ---------------------------------------------------------

G_cont = 1.0 / (
    rho_w * R * T / (ps * Dv * Mw)
    +
    Lv * rho_w / (Ka * T)
    * ((Lv * Mw) / (R * T) - 1.0)
)

print()
print("3. GROWTH COEFFICIENT")
print("---------------------")
print("Continuum G =", G_cont)

for r_um in [0.01, 0.1, 1.0, 10.0, 100.0]:

    G_r = growth_coefficient_ARG1998(
        r=r_um * 1e-6,
        T=T,
        ps=ps,
        Dv=Dv,
        Ka=Ka,
    )

    print(
        f"r={r_um:7.2f} um   "
        f"G={G_r:.8e} m2/s"
    )


# ---------------------------------------------------------
# 4. Full model-generated ARG calculation
# ---------------------------------------------------------

mode = ARGAerosolMode(
    N=N,
    am=am,
    sigma=sigma,
    B=B,
)

G_model = growth_coefficient_ARG1998(
    r=10e-6,
    T=T,
    ps=ps,
    Dv=Dv,
    Ka=Ka,
)

out = smax_ARG_single(
    mode=mode,
    T=T,
    p=p,
    ps=ps,
    V=V,
    G=G_model,
    sigma_w=sigma_w,
)

frac_model = activated_fraction_ARG(
    mode=mode,
    Smax=out["Smax"],
    Sm=out["Sm"],
)

print()
print("4. FULL MODEL-GENERATED ARG CALCULATION")
print("---------------------------------------")
print("G =", G_model)
print("Sm =", out["Sm"])
print("eta =", out["eta"])
print("zeta =", out["zeta"])
print("Smax =", out["Smax"])
print("Smax percent =", 100.0 * out["Smax"])
print("activated fraction =", frac_model)
print("Nd =", frac_model * N, "m^-3")


# ---------------------------------------------------------
# 5. Published-parameter algebra check
# ---------------------------------------------------------

ln_sigma = math.log(sigma)

f1 = 1.5 * math.exp(2.25 * ln_sigma**2)
f2 = 1.0 + 0.25 * ln_sigma

term1 = f1 * (zeta_ref / eta_ref) ** 1.5
term2 = f2 * (Sm_ref**2 / (eta_ref + 3.0 * zeta_ref)) ** 0.75

Smax_ref_algebra = Sm_ref / math.sqrt(term1 + term2)

u = (
    2.0 * math.log(Sm_ref / Smax_ref_algebra)
    / (3.0 * math.sqrt(2.0) * math.log(sigma))
)

frac_ref_algebra = 0.5 * (1.0 - math.erf(u))

print()
print("5. PUBLISHED-PARAMETER ALGEBRA CHECK")
print("------------------------------------")
print("f1 =", f1)
print("f2 =", f2)
print("Smax =", Smax_ref_algebra)
print("Smax percent =", 100.0 * Smax_ref_algebra)
print("activated fraction =", frac_ref_algebra)
print("Nd =", frac_ref_algebra * N, "m^-3")


# ---------------------------------------------------------
# 6. Summary
# ---------------------------------------------------------

print()
print("6. VALIDATION SUMMARY")
print("---------------------")

print(
    "Sm relative difference (%) =",
    100.0 * (Sm / Sm_ref - 1.0)
)

print(
    "eta relative difference (%) =",
    100.0 * (out["eta"] / eta_ref - 1.0)
)

print(
    "zeta relative difference (%) =",
    100.0 * (out["zeta"] / zeta_ref - 1.0)
)

print(
    "Smax difference: model-generated minus "
    "published-parameter algebra =",
    out["Smax"] - Smax_ref_algebra,
)

print(
    "Activated-fraction difference =",
    frac_model - frac_ref_algebra,
)

print()
print("Validation script completed.")
