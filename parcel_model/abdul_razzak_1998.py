import math
from dataclasses import dataclass

# ---------------------------------------------------------
# Abdul-Razzak, Ghan & Rivera-Carpio (1998)
# Single aerosol type activation parameterization
# ---------------------------------------------------------

R = 8.314462618       # J mol^-1 K^-1
Mw = 0.01801528       # kg mol^-1
rho_w = 1000.0        # kg m^-3
g = 9.80665            # m s^-2
cp_air = 1004.0        # J kg^-1 K^-1
Ma = 0.02897           # kg mol^-1
Lv = 2.5e6             # J kg^-1

# ---------------------------------------------------------
# Aerosol composition helpers
# ---------------------------------------------------------

def solute_B(
    vanthoff_i: float,
    osmotic_phi: float,
    soluble_mass_fraction: float,
    Mw_water: float,
    rho_aerosol: float,
    M_solute: float,
    rho_water: float = rho_w,
) -> float:
    """
    Abdul-Razzak et al. (1998), Eq. (6).

    B = nu * phi * epsilon * Mw * rho_aerosol
        / (M_solute * rho_water)

    Dimensionless in the ARG/Kohler formulation.
    """
    return (
        vanthoff_i
        * osmotic_phi
        * soluble_mass_fraction
        * Mw_water
        * rho_aerosol
        / (M_solute * rho_water)
    )


def ammonium_sulfate_B(
    soluble_mass_fraction: float = 1.0,
) -> float:
    """
    Pure/partly soluble ammonium sulfate benchmark.

    Values follow the assumptions used in the
    Abdul-Razzak & Ghan papers:
      nu = 3
      phi = 1
      M = 0.132 kg/mol
      rho = 1770 kg/m3
    """
    return solute_B(
        vanthoff_i=3.0,
        osmotic_phi=1.0,
        soluble_mass_fraction=soluble_mass_fraction,
        Mw_water=Mw,
        rho_aerosol=1770.0,
        M_solute=0.132,
    )

# ---------------------------------------------------------
# ARG-1998 condensational growth coefficient
# Equations (16)-(18)
# ---------------------------------------------------------

def modified_vapour_diffusivity_ARG1998(
    r: float,
    T: float,
    Dv: float,
    delta_v: float = 1.096e-7,
    alpha_c: float = 1.0,
) -> float:
    """
    Abdul-Razzak et al. (1998), Eq. (17).

    Parameters
    ----------
    r : droplet radius [m]
    T : temperature [K]
    Dv : continuum water-vapour diffusivity [m2 s-1]
    delta_v : vapour jump length [m]
              1.096e-5 cm = 1.096e-7 m
    alpha_c : condensation coefficient [-]
    """
    if r <= 0.0:
        raise ValueError("r must be positive")
    if Dv <= 0.0:
        raise ValueError("Dv must be positive")
    if alpha_c <= 0.0:
        raise ValueError("alpha_c must be positive")

    kinetic = (
        Dv
        / (r * alpha_c)
        * math.sqrt(2.0 * math.pi * Mw / (R * T))
    )

    return Dv / (
        r / (r + delta_v)
        + kinetic
    )


def modified_thermal_conductivity_ARG1998(
    r: float,
    T: float,
    Ka: float,
    delta_T: float = 2.16e-7,
    alpha_T: float = 0.96,
) -> float:
    """
    Abdul-Razzak et al. (1998), Eq. (18).

    Parameters
    ----------
    r : droplet radius [m]
    T : temperature [K]
    Ka : continuum thermal conductivity of air [W m-1 K-1]
    delta_T : thermal jump length [m]
              2.16e-5 cm = 2.16e-7 m
    alpha_T : thermal accommodation coefficient [-]
    """
    if r <= 0.0:
        raise ValueError("r must be positive")
    if Ka <= 0.0:
        raise ValueError("Ka must be positive")
    if alpha_T <= 0.0:
        raise ValueError("alpha_T must be positive")

    kinetic = (
        Ka
        / (r * alpha_T * cp_air)
        * math.sqrt(2.0 * math.pi * Ma / (R * T))
    )

    return Ka / (
        r / (r + delta_T)
        + kinetic
    )


def growth_coefficient_ARG1998(
    r: float,
    T: float,
    ps: float,
    Dv: float,
    Ka: float,
    delta_v: float = 1.096e-7,
    delta_T: float = 2.16e-7,
    alpha_c: float = 1.0,
    alpha_T: float = 0.96,
) -> float:
    """
    Abdul-Razzak et al. (1998), Eq. (16).

    Returns condensational growth coefficient G [m2 s-1].
    """

    if ps <= 0.0:
        raise ValueError("ps must be positive")

    Dv_prime = modified_vapour_diffusivity_ARG1998(
        r=r,
        T=T,
        Dv=Dv,
        delta_v=delta_v,
        alpha_c=alpha_c,
    )

    Ka_prime = modified_thermal_conductivity_ARG1998(
        r=r,
        T=T,
        Ka=Ka,
        delta_T=delta_T,
        alpha_T=alpha_T,
    )

    diffusion_term = (
        rho_w * R * T
        / (ps * Dv_prime * Mw)
    )

    thermal_term = (
        Lv * rho_w
        / (Ka_prime * T)
        * ((Lv * Mw) / (T * R) - 1.0)
    )

    return 1.0 / (diffusion_term + thermal_term)

@dataclass
class ARGAerosolMode:
    """
    Single lognormal aerosol mode.

    N      : total aerosol number concentration [m^-3]
    am     : geometric mean dry radius [m]
    sigma  : geometric standard deviation [-]
    B      : solute/hygroscopicity coefficient in ARG/Kohler notation [-]
    """
    N: float
    am: float
    sigma: float
    B: float


def curvature_A(T: float, sigma_w: float = 0.072) -> float:
    """
    Equation (5) in Abdul-Razzak et al. (1998)

    A = 2 sigma_w Mw / (rho_w R T)
    """
    return 2.0 * sigma_w * Mw / (rho_w * R * T)


def critical_supersaturation_ARG(aap: float, A: float, B: float) -> float:
    """
    Equation (4)

    Critical supersaturation for a dry aerosol radius aap.

    S* = (2/sqrt(B)) * (A/(3 aap))^(3/2)
    """
    if aap <= 0.0 or B <= 0.0:
        return float("inf")

    return (2.0 / math.sqrt(B)) * (A / (3.0 * aap)) ** 1.5


def mode_critical_supersaturation(mode: ARGAerosolMode, A: float) -> float:
    """
    Equation (8)

    Critical supersaturation associated with the
    geometric mean dry radius am.
    """
    return critical_supersaturation_ARG(mode.am, A, mode.B)


def alpha_coefficient(T: float) -> float:
    """
    Equation (11)

    alpha = g Mw Lv / (cp_air R T^2) - g Ma / (R T)
    """
    return (
        g * Mw * Lv / (cp_air * R * T * T)
        - g * Ma / (R * T)
    )


def gamma_coefficient(T: float, p: float, ps: float) -> float:
    """
    Abdul-Razzak et al. (1998), Eq. (12).

    ps : saturation vapour pressure over liquid water [Pa]
    p  : ambient air pressure [Pa]

    gamma = R*T/(ps*Mw) + Mw*Lv^2/(cp_air*p*Ma*T)
    """
    return (
        R * T / (ps * Mw)
        + Mw * Lv * Lv / (cp_air * p * Ma * T)
    )


def f1_sigma(sigma: float) -> float:
    """
    Equation (28)

    f1(ln sigma) = 1.5 exp[2.25 (ln sigma)^2]
    """
    lns = math.log(sigma)
    return 1.5 * math.exp(2.25 * lns * lns)


def f2_sigma(sigma: float) -> float:
    """
    Equation (29)

    f2(ln sigma) = 1 + 0.25 ln sigma
    """
    return 1.0 + 0.25 * math.log(sigma)


def eta_parameter(alpha: float, V: float, G: float,
                  gamma: float, mode: ARGAerosolMode) -> float:
    """
    Equation (22)

    eta = (alpha V / G)^(3/2) /
          (2 pi rho_w gamma N)
    """
    if V <= 0.0 or G <= 0.0 or mode.N <= 0.0:
        return 0.0

    return (
        (alpha * V / G) ** 1.5
        / (2.0 * math.pi * rho_w * gamma * mode.N)
    )


def zeta_parameter(alpha: float, V: float, G: float, A: float) -> float:
    """
    Equation (23)

    zeta = (2/3) * (alpha V / G)^(1/2) * A
    """
    if V <= 0.0 or G <= 0.0:
        return 0.0

    return (2.0 / 3.0) * math.sqrt(alpha * V / G) * A


def smax_ARG_single(
    mode: ARGAerosolMode,
    T: float,
    p: float,
    ps: float,
    V: float,
    G: float,
    sigma_w: float = 0.072,
) -> dict:
    """
    ARG-1998 single-mode maximum supersaturation.

    Uses equations (22), (23), (28), (29), and (31).
    """

    A = curvature_A(T, sigma_w=sigma_w)
    Sm = mode_critical_supersaturation(mode, A)

    alpha = alpha_coefficient(T)
    gamma = gamma_coefficient(T, p, ps)

    eta = eta_parameter(alpha, V, G, gamma, mode)
    zeta = zeta_parameter(alpha, V, G, A)

    f1 = f1_sigma(mode.sigma)
    f2 = f2_sigma(mode.sigma)

    if eta <= 0.0:
        return {
            "Smax": 0.0,
            "Sm": Sm,
            "eta": eta,
            "zeta": zeta,
            "alpha": alpha,
            "gamma": gamma,
        }

    term1 = f1 * (zeta / eta) ** 1.5
    term2 = f2 * (Sm * Sm / (eta + 3.0 * zeta)) ** 0.75

    denominator = math.sqrt(term1 + term2)

    Smax = Sm / denominator

    return {
        "Smax": Smax,
        "Sm": Sm,
        "eta": eta,
        "zeta": zeta,
        "alpha": alpha,
        "gamma": gamma,
    }


def activated_fraction_ARG(
    mode: ARGAerosolMode,
    Smax: float,
    Sm: float,
) -> float:
    """
    Equations (2), (3), and (9).

    N/Nap = 0.5 * [1 - erf(u)]

    where:
    u = 2 ln(Sm/Smax) / (3 sqrt(2) ln sigma)
    """

    if Smax <= 0.0:
        return 0.0

    if mode.sigma <= 1.0:
        # Monodisperse limiting behaviour
        return 1.0 if Smax >= Sm else 0.0

    u = (
        2.0 * math.log(Sm / Smax)
        / (3.0 * math.sqrt(2.0) * math.log(mode.sigma))
    )

    frac = 0.5 * (1.0 - math.erf(u))

    return max(0.0, min(1.0, frac))
