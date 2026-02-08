"""
run_mixed_phase_physics.py

Mixed-phase parcel model (skeleton):
- Separate vapour tendency terms over liquid and ice
- Tracks: T(t), qv(t), Sw(t), Si(t), ql(t), qi(t)
- Includes placeholders for physically-based growth equations (Maxwell-type)

Author: (your name)
"""

from __future__ import annotations
import math
import csv

from thermodynamics import saturation_vapor_pressure, supersaturation
# NOTE: You already have saturation_vapor_pressure(T) for liquid.
# We will add a simple placeholder for ice saturation below.

from aerosol import AerosolPopulation
from activation import check_activation
from biological_in import BiologicalIN, check_ice_nucleation


# ------------------------------------------------------------
# 1) Saturation vapour pressure over ice (placeholder)
# ------------------------------------------------------------
def saturation_vapor_pressure_ice(T: float) -> float:
    """
    Placeholder for e_si(T).
    Replace later with a standard parameterization (Murphy & Koop 2005, etc.).
    For now, we approximate e_si as slightly lower than e_sw.
    """
    e_sw = saturation_vapor_pressure(T)
    return 0.95 * e_sw  # TEMPORARY placeholder (replace with proper formula)


# ------------------------------------------------------------
# 2) Supersaturation wrt liquid and ice
# ------------------------------------------------------------
def supersaturation_wrt_liquid(e: float, T: float) -> float:
    e_sw = saturation_vapor_pressure(T)
    return (e - e_sw) / e_sw


def supersaturation_wrt_ice(e: float, T: float) -> float:
    e_si = saturation_vapor_pressure_ice(T)
    return (e - e_si) / e_si


# ------------------------------------------------------------
# 3) Growth tendency placeholders (Maxwell-type skeleton)
# ------------------------------------------------------------
def liquid_tendency(Sw: float, activated_liquid: bool, esw: float) -> float:
    """
    Returns C_l (vapour sink/source due to liquid), units: Pa/s or arbitrary.
    Positive C_l means vapour REMOVED (condensation), negative means vapour ADDED (evaporation).

    Placeholder: linear relaxation. Replace with Maxwell-type growth later.
    """
    if not activated_liquid:
        return 0.0

    k_l = 0.2  # tune later
    # if Sw > 0 -> condensation (sink), if Sw < 0 -> evaporation (source)
    return k_l * Sw * esw


def ice_tendency(Si: float, ice_active: bool, esi: float, qi: float) -> float:
    """
    Returns C_i (vapour sink/source due to ice), units: Pa/s or arbitrary.
    Positive C_i means vapour REMOVED (deposition), negative means vapour ADDED (sublimation).

    Placeholder: linear deposition sink stronger than liquid.
    """
    if not ice_active:
        return 0.0

    k_i = 1.0  # tune later
    return k_i * Si * esi


def update_ice_mass_proxy(qi: float, Ci: float, dt: float) -> float:
    """
    Very simple ice-mass proxy growth:
    qi increases with positive deposition sink (Ci>0).
    This is a placeholder. Replace with a proper mass budget later.
    """
    if Ci > 0:
        qi = qi + 1e-12 * Ci * dt  # arbitrary scaling
    return qi


# ------------------------------------------------------------
# 4) Main run
# ------------------------------------------------------------
def run_mixed_phase_physics(
    w: float = 1.0,
    dt: float = 1.0,
    t_end: float = 1200.0,
    RH0: float = 0.95,
    T0: float = 273.15,
    include_ice: bool = True,
    save_csv: bool = True,
    csv_name: str = "mixed_phase_physics_timeseries.csv",
    verbose: bool = True,
):
    """
    Mixed-phase parcel model skeleton.
    Uses:
    - separate Sw, Si
    - separate vapour tendencies C_l, C_i
    """

    # ----- Liquid CCN populations -----
    sulfate = AerosolPopulation(
        name="sulfate", N=500e6, radius=30e-9, kappa=1.0, rho_p=1770.0
    )
    pollen = AerosolPopulation(
        name="pollen", N=3000.0, radius=5e-6, kappa=0.1, rho_p=1000.0
    )

    # ----- Biological IN population -----
    bio = BiologicalIN(name="bioIN", N=50.0, T50=263.15, width=2.0)

    # ----- Parcel state -----
    T = T0
    e = RH0 * saturation_vapor_pressure(T)  # vapour partial pressure proxy
    qi = 0.0
    ql = 0.0  # optional placeholder liquid proxy (not yet used)

    cooling_rate = 0.01 * w  # same mapping used before

    ice_active = False
    ice_onset_t = None
    ice_onset_T = None

    # ----- Storage -----
    times, Ts, Sws, Sis, es_list = [], [], [], [], []
    Cis, Cls, qis = [], [], []

    if verbose:
        print("\nMixed-phase physics skeleton run")
        print(f"w={w:.2f} m/s, cooling_rate={cooling_rate:.4f} K/s, dt={dt}, t_end={t_end}")
        print("t(s)   T(K)     Sw         Si        ice_active    qi")

    t = 0.0
    while t <= t_end:
        esw = saturation_vapor_pressure(T)
        esi = saturation_vapor_pressure_ice(T)

        Sw = supersaturation_wrt_liquid(e, T)
        Si = supersaturation_wrt_ice(e, T)

        # Liquid activation checks (existing code)
        check_activation(Sw, sulfate, T=T)
        check_activation(Sw, pollen, T=T)

        activated_liquid = sulfate.activated or pollen.activated

        # Ice nucleation switch
        if include_ice and (not ice_active):
            nucleated, N_active = check_ice_nucleation(T, bio, N_threshold=1.0)
            if nucleated:
                ice_active = True
                ice_onset_t = t
                ice_onset_T = T

        # Separate vapour tendencies (placeholders)
        Cl = liquid_tendency(Sw, activated_liquid, esw)  # Pa/s
        Ci = ice_tendency(Si, ice_active, esi, qi)       # Pa/s

        # Vapour budget: e decreases if sinks are positive
        # Convert tendencies to a change in e over dt
        e = e - (Cl + Ci) * dt
        if e < 0:
            e = 0.0

        # Update ice mass proxy
        qi = update_ice_mass_proxy(qi, Ci, dt)

        # Save
        times.append(t)
        Ts.append(T)
        Sws.append(Sw)
        Sis.append(Si)
        es_list.append(e)
        Cls.append(Cl)
        Cis.append(Ci)
        qis.append(qi)

        if verbose and int(t) % 60 == 0:
            print(f"{int(t):4d}  {T:7.2f}  {Sw: .3e}  {Si: .3e}     {str(ice_active):>5}    {qi: .3e}")

        # Advance parcel temperature
        T = T - cooling_rate * dt
        t += dt

    if include_ice and verbose:
        if ice_active:
            print(f"\nIce onset detected at t={ice_onset_t:.0f}s, T={ice_onset_T:.2f}K")
        else:
            print("\nIce onset not reached in simulation window")

    # Save CSV for plotting
    if save_csv:
        with open(csv_name, "w", newline="") as f:
            wtr = csv.writer(f)
            wtr.writerow(["t_s", "T_K", "Sw", "Si", "e_Pa", "Cl_Pa_per_s", "Ci_Pa_per_s", "qi_proxy"])
            for i in range(len(times)):
                wtr.writerow([times[i], Ts[i], Sws[i], Sis[i], es_list[i], Cls[i], Cis[i], qis[i]])
        if verbose:
            print(f"\nSaved timeseries: {csv_name}")

    return times, Ts, Sws, Sis, es_list, Cls, Cis, qis, ice_onset_t, ice_onset_T


def main():
    run_mixed_phase_physics(w=1.0, include_ice=True, verbose=True)


if __name__ == "__main__":
    main()
