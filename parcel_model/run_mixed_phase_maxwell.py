import csv
import math

from parcel_model.thermodynamics import esat_water, esat_ice, Sw, Si
from parcel_model.aerosol import AerosolPopulation
from parcel_model.activation import check_activation
from parcel_model.biological_in import BiologicalIN, check_ice_nucleation

# ---------------------------
# Basic constants (SI)
# ---------------------------
Rv = 461.5        # J/kg/K  (water vapour gas constant)
rho_l = 1000.0    # kg/m^3  (liquid water density)
rho_i = 917.0     # kg/m^3  (ice density)
Lv = 2.5e6        # J/kg    (latent heat of vaporization)
Ls = 2.834e6      # J/kg    (latent heat of sublimation)
P0 = 101325.0     # Pa
cp = 1005.0       # J/kg/K  (specific heat of air)

# ---------------------------
# Diffusivity + thermal conductivity
# ---------------------------
def diffusivity_water_vapour(T, P=P0):
    D0 = 2.11e-5  # m^2/s at ~273K, 1 atm
    return D0 * (T / 273.15) ** 1.94 * (P0 / P)

def thermal_conductivity_air(T):
    k0 = 0.024  # W/m/K
    return k0 * (T / 273.15) ** 0.9

# ---------------------------
# Maxwell-type growth coefficient G(T) [m^2/s]
# dr/dt = (G / r) * S
# ---------------------------
def G_liquid(T, esw, P=P0):
    D = diffusivity_water_vapour(T, P)
    k = thermal_conductivity_air(T)

    A = (rho_l * Rv * T) / (D * esw)
    B = (rho_l * Lv * Lv) / (k * Rv * T * T)
    return 1.0 / (A + B)

def G_ice(T, esi, P=P0):
    D = diffusivity_water_vapour(T, P)
    k = thermal_conductivity_air(T)

    A = (rho_i * Rv * T) / (D * esi)
    B = (rho_i * Ls * Ls) / (k * Rv * T * T)
    return 1.0 / (A + B)

# ---------------------------
# Helper: mass per volume from N and radius
# q = N * (4/3) pi rho r^3
# ---------------------------
def q_from_N_r(N, r, rho):
    return N * (4.0 / 3.0) * math.pi * rho * r**3

def run(
    w=1.0,
    dt=1.0,
    t_end=1200.0,
    outfile="mixed_phase_maxwell_timeseries.csv",
    sulfate_N=500e6,
    pollen_N=3000.0,
    bio_N=5.0,
    bio_T50=263.15,
    bio_width=2.0,
    r_cloud_init=1e-6,
    r_ice_init=5e-6,
    T_init=273.15,
    RH0=0.95
):
    sulfate = AerosolPopulation(
        "sulfate",
        N=sulfate_N,
        radius=30e-9,
        kappa=1.0,
        rho_p=1770.0
    )

    pollen = AerosolPopulation(
        "pollen",
        N=pollen_N,
        radius=5e-6,
        kappa=0.1,
        rho_p=1000.0
    )

    bio = BiologicalIN(
        name="bioIN",
        N=bio_N,
        T50=bio_T50,
        width=bio_width
    )

    # ---------------------------
    # Parcel initial state
    # ---------------------------
    T = T_init
    e = RH0 * esat_water(T)

    # Simple imposed cooling
    cooling_rate = 0.01 * w  # K/s

    # Mean radii
    r_cloud = r_cloud_init
    r_ice = r_ice_init

    ice_active = False
    ice_onset_t = None
    ice_onset_T = None

    print("\nMixed-phase Maxwell growth run (with latent heating)")
    print(f"w={w:.2f} m/s, cooling_rate={cooling_rate:.4f} K/s, dt={dt}, t_end={t_end}")
    print("t(s)   T(K)     Sw         Si        r_cloud(um)  r_ice(um)   Ncloud      Nice        qcloud      qice")

    with open(outfile, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow([
            "t_s", "T_K", "e_Pa", "Sw", "Si",
            "Ncloud", "Nice",
            "r_cloud_m", "r_ice_m",
            "drcloud_dt", "drice_dt",
            "qcloud", "qice",
            "cond_rate_kgm3s", "dep_rate_kgm3s",
            "cond_sink_kgm3s", "dep_sink_kgm3s",
            "R_BF",
            "latent_heating_Ks", "dT_dt_Ks",
            "ice_active"
        ])

        t = 0.0
        while t <= t_end:
            # ---------------------------
            # Saturation vapour pressures
            # ---------------------------
            esw = esat_water(T)
            esi = esat_ice(T)

            # ---------------------------
            # Supersaturation
            # ---------------------------
            Sw_val = Sw(e, T)
            Si_val = Si(e, T)

            # ---------------------------
            # Liquid activation
            # ---------------------------
            check_activation(Sw_val, sulfate, T=T)
            check_activation(Sw_val, pollen, T=T)

            Ncloud = 0.0
            if sulfate.activated:
                Ncloud += sulfate.N
            if pollen.activated:
                Ncloud += pollen.N

            # ---------------------------
            # Ice nucleation
            # ---------------------------
            Nice = 0.0
            if not ice_active:
                nucleated, N_active = check_ice_nucleation(T, bio, N_threshold=1.0)
                if nucleated:
                    ice_active = True
                    ice_onset_t = t
                    ice_onset_T = T
                    Nice = N_active
                else:
                    Nice = 0.0
            else:
                _, N_active = check_ice_nucleation(T, bio, N_threshold=0.0)
                Nice = N_active

            # ---------------------------
            # Maxwell growth rates
            # ---------------------------
            drcloud_dt = 0.0
            if Ncloud > 0.0:
                Gc = G_liquid(T, esw, P0)
                drcloud_dt = (Gc / max(r_cloud, 1e-9)) * Sw_val

            drice_dt = 0.0
            if ice_active and Nice > 0.0:
                Gi = G_ice(T, esi, P0)
                drice_dt = (Gi / max(r_ice, 1e-9)) * Si_val

            # Prevent negative radii
            r_cloud = max(r_cloud + drcloud_dt * dt, 0.0)
            r_ice = max(r_ice + drice_dt * dt, 0.0)

            # ---------------------------
            # Phase masses
            # ---------------------------
            qcloud = q_from_N_r(Ncloud, r_cloud, rho_l) if Ncloud > 0 else 0.0
            qice = q_from_N_r(Nice, r_ice, rho_i) if Nice > 0 else 0.0

            # ---------------------------
            # Condensation / deposition rates
            # Positive = growth
            # Negative = evaporation / sublimation
            # ---------------------------
            cond_rate = 0.0
            if Ncloud > 0.0:
                dm_dt_one = 4.0 * math.pi * r_cloud**2 * rho_l * drcloud_dt
                cond_rate = Ncloud * dm_dt_one

            dep_rate = 0.0
            if ice_active and Nice > 0.0:
                dm_dt_one = 4.0 * math.pi * r_ice**2 * rho_i * drice_dt
                dep_rate = Nice * dm_dt_one

            # ---------------------------
            # Clean positive sinks only
            # ---------------------------
            cond_sink = max(cond_rate, 0.0)
            dep_sink = max(dep_rate, 0.0)

            # ---------------------------
            # Clean Bergeron-Findeisen ratio
            # ---------------------------
            eps = 1e-12
            R_BF = dep_sink / max(cond_sink, eps)

            # ---------------------------
            # Temperature tendency with latent heating
            # ---------------------------
            latent_heating = (Lv * cond_rate + Ls * dep_rate) / cp
            dT_dt = -cooling_rate + latent_heating

            # ---------------------------
            # Vapour density tendency -> vapour pressure tendency
            # rho_v = e/(Rv*T)
            # drho_v/dt = -(cond_rate + dep_rate)
            # de/dt = Rv*T*drho_v/dt + (e/T)*dT_dt
            # ---------------------------
            drhov_dt = -(cond_rate + dep_rate)
            de_dt = Rv * T * drhov_dt + (e / T) * dT_dt
            e = max(e + de_dt * dt, 0.0)

            if abs(t % 60.0) < 1e-9:
                print(
                    f"{int(t):4d}  {T:7.2f}  {Sw_val: .3e}  {Si_val: .3e}   "
                    f"{1e6*r_cloud:8.3f}   {1e6*r_ice:7.3f}  "
                    f"{Ncloud: .3e}  {Nice: .3e}  {qcloud: .3e}  {qice: .3e}"
                )

            wr.writerow([
                t, T, e, Sw_val, Si_val,
                Ncloud, Nice,
                r_cloud, r_ice,
                drcloud_dt, drice_dt,
                qcloud, qice,
                cond_rate, dep_rate,
                cond_sink, dep_sink,
                R_BF,
                latent_heating, dT_dt,
                int(ice_active)
            ])

            # Advance
            T = T + dT_dt * dt
            t += dt

    if ice_onset_t is not None:
        print(f"\nIce onset detected at t={ice_onset_t:.0f}s, T={ice_onset_T:.2f}K")
    else:
        print("\nIce onset not reached within simulation")

    print(f"Saved timeseries: {outfile}")

if __name__ == "__main__":
    run()