import os
import sys
from dataclasses import dataclass

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd

from parcel_model.activation import check_activation
from parcel_model.aerosol import AerosolPopulation
from parcel_model.thermodynamics import Sw


@dataclass
class KiDCase1Config:
    dt: float = 0.5
    t_end: float = 3600.0

    # KiD Case 1 style forcing
    z_top: float = 3000.0
    w1: float = 2.0
    t1: float = 3600.0
    t2: float = 600.0

    # Warm-rain benchmark assumptions
    temperature_fixed: bool = True
    initial_temperature: float = 283.15
    initial_pressure: float = 90000.0
    initial_qv: float = 0.00817

    # Aerosol setup
    ccn_concentration: float = 100e6
    aerosol_radius: float = 0.05e-6
    aerosol_kappa: float = 0.3
    aerosol_density: float = 1770.0

    enable_ice: bool = False
    enable_rain: bool = True
    initial_height: float = 0.0

    # Maxwell growth parameters
    initial_droplet_radius: float = 1.0e-6
    G_liquid = 8.0e-12

    # Bulk conversion constants
    rho_water: float = 1000.0
    rho_air: float = 1.0

    # Warm-rain tuning
    ql_threshold = 4.0e-4
    autoconv_coeff = 1.5e-4
    accretion_coeff: float = 2.0


def kid_case1_updraft(t: float, w1: float, t1: float, t2: float) -> float:
    if t < t2:
        return w1 * np.sin(np.pi * t / t2)
    return 0.0


def mixing_ratio_to_vapour_pressure(qv: float, p: float) -> float:
    """
    Convert water vapour mixing ratio qv [kg/kg]
    to vapour pressure e [Pa].
    """
    epsilon = 0.622
    return qv * p / (epsilon + qv)


def initialize_state(config: KiDCase1Config) -> dict:
    aerosol = AerosolPopulation(
        name="CCN",
        N=config.ccn_concentration,
        radius=config.aerosol_radius,
        kappa=config.aerosol_kappa,
        rho_p=config.aerosol_density
    )

    return {
        "z": config.initial_height,
        "T": config.initial_temperature,
        "p": config.initial_pressure,
        "qv": config.initial_qv,
        "ql": 0.0,
        "qr": 0.0,
        "qi": 0.0,
        "cond_rate": 0.0,
        "rain_source": 0.0,
        "n_droplets": 0.0,
        "S": 0.0,
        "Sc": 0.0,
        "e": 0.0,
        "droplet_radius": config.initial_droplet_radius,
        "aerosol": aerosol,
    }


def update_activation(state: dict, config: KiDCase1Config) -> dict:
    """
    Kohler activation with persistent cloud droplet number.

    Once droplets activate, Nc is retained rather than being
    diagnosed downward immediately when supersaturation decreases.
    """
    aerosol = state["aerosol"]

    e = mixing_ratio_to_vapour_pressure(state["qv"], state["p"])
    S = Sw(e, state["T"])

    activated, Sc = check_activation(S, aerosol, T=state["T"])

    state["e"] = e
    state["S"] = S
    state["Sc"] = Sc

    diagnosed_Nc = aerosol.N * aerosol.activated_fraction

    # Keep previously activated droplets.
    state["n_droplets"] = max(
        state["n_droplets"],
        diagnosed_Nc
    )

    return state


def update_liquid_growth(state: dict, config: KiDCase1Config, w: float) -> dict:
    """
    Maxwell-type condensational growth and evaporation.

    S > 0 : droplets grow and cloud water increases.
    S < 0 : existing droplets evaporate and cloud water decreases.

    Activated droplet number is retained during evaporation and is
    removed only when cloud liquid water has essentially evaporated.
    """
    e = mixing_ratio_to_vapour_pressure(state["qv"], state["p"])
    S = Sw(e, state["T"])

    n_droplets = state["n_droplets"]
    r = max(state["droplet_radius"], 1.0e-9)

    dr_dt = 0.0
    cond_rate = 0.0

    if n_droplets > 0.0:

        # Maxwell growth/evaporation:
        # positive for supersaturation, negative for subsaturation
        dr_dt = (config.G_liquid / r) * S

        r_new = r + dr_dt * config.dt
        r_new = max(r_new, 1.0e-9)

        cond_rate = (
            n_droplets
            * 4.0
            * np.pi
            * config.rho_water
            * (r ** 2)
            * dr_dt
            / config.rho_air
        )

        if cond_rate > 0.0:
            # Condensation: cannot consume more vapour than available.
            max_condensation = state["qv"] / config.dt
            cond_rate = min(cond_rate, max_condensation)

            # Preserve the existing weak updraft dependence for growth.
            cond_rate *= (1.0 + 0.05 * max(w, 0.0))

        elif cond_rate < 0.0:
            # Evaporation: cannot evaporate more cloud water than exists.
            max_evaporation = state["ql"] / config.dt
            cond_rate = max(cond_rate, -max_evaporation)

        state["droplet_radius"] = r_new

    # Positive cond_rate transfers vapour -> liquid.
    # Negative cond_rate transfers liquid -> vapour.
    state["qv"] -= cond_rate * config.dt
    state["ql"] += cond_rate * config.dt

    state["ql"] = max(state["ql"], 0.0)
    state["qv"] = max(state["qv"], 0.0)

    # Once all cloud water has evaporated under subsaturated conditions,
    # the cloud droplets are considered returned to haze particles.
    if state["ql"] <= 1.0e-12 and S < 0.0:
        state["ql"] = 0.0
        state["n_droplets"] = 0.0
        state["droplet_radius"] = config.initial_droplet_radius

    state["cond_rate"] = cond_rate
    state["e"] = e
    state["S"] = S
    state["dr_dt"] = dr_dt

    return state


def update_warm_rain(state: dict, config: KiDCase1Config) -> dict:
    ql = state["ql"]
    qr = state["qr"]

    autoconv = 0.0
    if ql > config.ql_threshold:
        autoconv = config.autoconv_coeff * (ql - config.ql_threshold)

    accretion = config.accretion_coeff * ql * qr
    rain_source = autoconv + accretion

    state["ql"] -= rain_source * config.dt
    state["qr"] += rain_source * config.dt
    state["rain_source"] = rain_source

    state["ql"] = max(state["ql"], 0.0)
    state["qr"] = max(state["qr"], 0.0)

    return state


def diagnose_surface_rain_rate(state: dict) -> float:
    fall_speed_rain = 5.0
    return state["qr"] * fall_speed_rain


def initialize_history() -> dict:
    return {
        "time": [],
        "height": [],
        "w": [],
        "temperature": [],
        "qv": [],
        "vapour_pressure": [],
        "cloud_mass": [],
        "rain_mass": [],
        "surface_rain_rate": [],
        "liquid_water_path": [],
        "cond_rate": [],
        "n_droplets": [],
        "activated_fraction": [],
        "S": [],
        "Sc": [],
        "droplet_radius": [],
        "dr_dt": [],
    }


def save_diagnostics(history: dict, state: dict, t: float, w: float) -> dict:
    history["time"].append(t)
    history["height"].append(state["z"])
    history["w"].append(w)
    history["temperature"].append(state["T"])
    history["qv"].append(state["qv"])
    history["vapour_pressure"].append(state["e"])
    history["cloud_mass"].append(state["ql"])
    history["rain_mass"].append(state["qr"])
    history["surface_rain_rate"].append(diagnose_surface_rain_rate(state))
    history["liquid_water_path"].append(state["ql"])
    history["cond_rate"].append(state["cond_rate"])
    history["n_droplets"].append(state["n_droplets"])
    history["activated_fraction"].append(state["n_droplets"] / 1.0e8)
    history["S"].append(state["S"])
    history["Sc"].append(state["Sc"])
    history["droplet_radius"].append(state["droplet_radius"])
    history["dr_dt"].append(state.get("dr_dt", 0.0))
    return history


def run_case1() -> pd.DataFrame:
    config = KiDCase1Config()
    state = initialize_state(config)
    history = initialize_history()

    t = 0.0
    while t <= config.t_end:
         w = kid_case1_updraft(t, config.w1, config.t1, config.t2)

         # Controlled thermodynamic cycle:
         # 1) cool parcel to trigger activation
         # 2) then warm parcel to force subsaturation and evaporation

         if t < 1200.0:
             cooling_rate = 0.001  # K/s
             state["T"] -= cooling_rate * config.dt
         else:
             warming_rate = 0.001  # K/s
             state["T"] += warming_rate * config.dt

         state["z"] += w * config.dt
         state = update_activation(state, config)
         state = update_liquid_growth(state, config, w)

         if config.enable_rain:
             state = update_warm_rain(state, config)

         history = save_diagnostics(history, state, t, w)
         t += config.dt

    return pd.DataFrame(history)


def main():
    os.makedirs("data", exist_ok=True)

    df = run_case1()
    output_path = "data/persistent_Nc_results.csv"
    df.to_csv(output_path, index=False)

    print(df.head())
    print(f"\nSaved to {output_path}")
    print("Activation mode: real check_activation() with AerosolPopulation")
    print("Supersaturation mode: real Sw(e, T) from thermodynamics.py")
    print("Growth mode: Maxwell-type droplet growth")


if __name__ == "__main__":
    main()
