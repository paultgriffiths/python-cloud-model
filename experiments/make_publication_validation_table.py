import math

import pandas as pd

from parcel_model.abdul_razzak_1998 import (
    ARGAerosolMode,
    ammonium_sulfate_B,
    curvature_A,
    critical_supersaturation_ARG,
    smax_ARG_single,
    activated_fraction_ARG,
)

OUTPUT_FILE = "data/publication_validation_table.csv"

# --------------------------------------------------
# Abdul-Razzak et al. (1998) benchmark
# --------------------------------------------------

T = 283.15
p = 80000.0
ps = 1226.0
V = 5.0

N = 200e6
am = 0.01e-6
sigma = 2.5

D0 = 2.11e-5
Dv = D0 * (T / 273.15) ** 1.94 * (101325.0 / p)

Ka = 0.0249

Tc = 647.096
tau = 1.0 - T / Tc
sigma_w = 235.8e-3 * tau**1.256 * (1.0 - 0.625 * tau)

Sm_ref = 1.762e-2
eta_ref = 4.037e-4
zeta_ref = 3.966e-6

B = ammonium_sulfate_B()
A = curvature_A(T, sigma_w=sigma_w)

Sm = critical_supersaturation_ARG(am, A, B)

mode = ARGAerosolMode(
    N=N,
    am=am,
    sigma=sigma,
    B=B,
)

# Continuum growth coefficient used by the validation script
from parcel_model.abdul_razzak_1998 import R, Mw, rho_w, Lv

G_cont = 1.0 / (
    rho_w * R * T / (ps * Dv * Mw)
    +
    Lv * rho_w / (Ka * T)
    * ((Lv * Mw) / (R * T) - 1.0)
)

out = smax_ARG_single(
    mode=mode,
    T=T,
    p=p,
    ps=ps,
    V=V,
    G=G_cont,
    sigma_w=sigma_w,
)

frac_model = activated_fraction_ARG(
    mode=mode,
    Smax=out["Smax"],
    Sm=out["Sm"],
)

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

# --------------------------------------------------
# Clean timestep-convergence test
# --------------------------------------------------

dt = pd.read_csv("data/clean_timestep_sensitivity.csv")

dt_coarse = dt.loc[dt["dt_s"].idxmax()]
dt_fine = dt.loc[dt["dt_s"].idxmin()]

table = pd.DataFrame(
    [
        {
            "validation_test": "ARG1998 critical supersaturation",
            "model_value": Sm,
            "comparison_value": Sm_ref,
            "relative_difference_percent": 100.0 * (Sm / Sm_ref - 1.0),
            "units": "fraction",
            "notes": "Abdul-Razzak et al. (1998) Figure-5 benchmark conditions",
        },
        {
            "validation_test": "ARG1998 eta",
            "model_value": out["eta"],
            "comparison_value": eta_ref,
            "relative_difference_percent": 100.0 * (out["eta"] / eta_ref - 1.0),
            "units": "dimensionless",
            "notes": "Published benchmark quantity",
        },
        {
            "validation_test": "ARG1998 zeta",
            "model_value": out["zeta"],
            "comparison_value": zeta_ref,
            "relative_difference_percent": 100.0 * (out["zeta"] / zeta_ref - 1.0),
            "units": "dimensionless",
            "notes": "Published benchmark quantity",
        },
        {
            "validation_test": "ARG1998 Smax",
            "model_value": 100.0 * out["Smax"],
            "comparison_value": 100.0 * Smax_ref_algebra,
            "relative_difference_percent": 100.0
            * (out["Smax"] / Smax_ref_algebra - 1.0),
            "units": "%",
            "notes": "Model-generated versus published-parameter algebra",
        },
        {
            "validation_test": "ARG1998 activated fraction",
            "model_value": frac_model,
            "comparison_value": frac_ref_algebra,
            "relative_difference_percent": 100.0
            * (frac_model / frac_ref_algebra - 1.0),
            "units": "fraction",
            "notes": "Model-generated versus published-parameter algebra",
        },
        {
            "validation_test": "Timestep convergence: SSmax",
            "model_value": dt_coarse["SSmax_percent"],
            "comparison_value": dt_fine["SSmax_percent"],
            "relative_difference_percent": 100.0
            * (dt_coarse["SSmax_percent"] / dt_fine["SSmax_percent"] - 1.0),
            "units": "%",
            "notes": "dt = 2.0 s compared with dt = 0.1 s",
        },
        {
            "validation_test": "Timestep convergence: t50",
            "model_value": dt_coarse["t_50pct_s"],
            "comparison_value": dt_fine["t_50pct_s"],
            "relative_difference_percent": 100.0
            * (dt_coarse["t_50pct_s"] / dt_fine["t_50pct_s"] - 1.0),
            "units": "s",
            "notes": "dt = 2.0 s compared with dt = 0.1 s",
        },
        {
            "validation_test": "Timestep convergence: qcmax",
            "model_value": dt_coarse["qcmax_kgkg"],
            "comparison_value": dt_fine["qcmax_kgkg"],
            "relative_difference_percent": 100.0
            * (dt_coarse["qcmax_kgkg"] / dt_fine["qcmax_kgkg"] - 1.0),
            "units": "kg kg^-1",
            "notes": "dt = 2.0 s compared with dt = 0.1 s",
        },
    ]
)

table.to_csv(OUTPUT_FILE, index=False)

print(table.to_string(index=False))
print()
print(f"Saved: {OUTPUT_FILE}")
