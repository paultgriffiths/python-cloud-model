import csv
import math

from thermodynamics import saturation_vapor_pressure, supersaturation
from aerosol import AerosolPopulation
from activation import check_activation
from biological_in import BiologicalIN, check_ice_nucleation

# ---------------------------
# Basic constants (SI)
# ---------------------------
Rv = 461.5        # J/kg/K  (water vapour gas constant)
rho_l = 1000.0    # kg/m^3  (liquid water density)
rho_i = 917.0     # kg/m^3  (ice density)
Lv = 2.5e6        # J/kg    (latent heat vap)
Ls = 2.834e6      # J/kg    (latent heat subl, approx)
P0 = 101325.0     # Pa (use constant for now)

# ---------------------------
# Ice saturation vapour pressure (simple physical placeholder)
# IMPORTANT: Replace later with a published e_si(T) formula.
# For now: scale liquid es by factor < 1 so e_si < e_sw.
# ---------------------------
def saturation_vapor_pressure_ice_simple(T):
    return 0.9 * saturation_vapor_pressure(T)

# ---------------------------
# Diffusivity + thermal conductivity (simple T scalings)
# (Enough for a stable Level-B prototype.)
# ---------------------------
def diffusivity_water_vapour(T, P=P0):
    # rough scaling around 273K
    D0 = 2.11e-5  # m^2/s at ~273K, 1 atm
    return D0 * (T / 273.15) ** 1.94 * (P0 / P)

def thermal_conductivity_air(T):
    # rough scaling around 273K
    k0 = 0.024  # W/m/K
    return k0 * (T / 273.15) ** 0.9

# ---------------------------
# Maxwell-type growth coefficient G(T) [m^2/s]
# dr/dt = (G / r) * S
# where S is supersaturation wrt liquid or ice.
# ---------------------------
def G_liquid(T, esw, P=P0):
    D = diffusivity_water_vapour(T, P)
    k = thermal_conductivity_air(T)

    # "resistance" terms (diffusion + thermal)
    # This is a standard Maxwell-style structure; coefficients are simplified.
    A = (rho_l * Rv * T) / (D * esw)              # diffusion resistance
    B = (rho_l * Lv * Lv) / (k * Rv * T * T)      # thermal resistance

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

def run(w=1.0, dt=1.0, t_end=1200.0, outfile="mixed_phase_maxwell_timeseries.csv"):
    # Aerosols (liquid CCN)
    sulfate = AerosolPopulation("sulfate", N=500e6, radius=30e-9, kappa=1.0, rho_p=1770.0)
    pollen  = AerosolPopulation("pollen",  N=3000.0, radius=5e-6,  kappa=0.1, rho_p=1000.0)

    # Biological IN (ice)
    bio = BiologicalIN(name="bioIN", N=5e0, T50=263.15, width=2.0)  # tune later

    # Parcel state
    T = 273.15
    RH0 = 0.95
    e = RH0 * saturation_vapor_pressure(T)

    cooling_rate = 0.01 * w  # K/s (toy dynamics for now)

    # Mean radii (start tiny; will grow when activated/nucleated)
    r_cloud = 1e-6   # m
    r_ice   = 5e-6   # m

    ice_active = False
    ice_onset_t = None
    ice_onset_T = None

    print("\nMixed-phase Maxwell growth run")
    print(f"w={w:.2f} m/s, cooling_rate={cooling_rate:.4f} K/s, dt={dt}, t_end={t_end}")
    print("t(s)   T(K)     Sw         Si        r_cloud(um)  r_ice(um)   Ncloud      Nice        qcloud      qice")

    with open(outfile, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow([
            "t_s","T_K","e_Pa","Sw","Si",
            "Ncloud","Nice",
            "r_cloud_m","r_ice_m",
            "drcloud_dt","drice_dt",
            "qcloud","qice",
            "cond_rate_kgm3s","dep_rate_kgm3s",
            "ice_active"
        ])

        t = 0.0
        while t <= t_end:
            esw = saturation_vapor_pressure(T)
            esi = saturation_vapor_pressure_ice_simple(T)

            Sw = supersaturation(e, esw)          # (e/esw) - 1
            Si = (e / esi) - 1.0

            # --- Liquid activation
            check_activation(Sw, sulfate, T=T)
            check_activation(Sw, pollen,  T=T)

            Ncloud = 0.0
            if sulfate.activated: Ncloud += sulfate.N
            if pollen.activated:  Ncloud += pollen.N

            # --- Ice nucleation
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

            # --- Maxwell growth rates (mean-radius)
            drcloud_dt = 0.0
            if Ncloud > 0.0:
                Gc = G_liquid(T, esw, P0)
                drcloud_dt = (Gc / max(r_cloud, 1e-9)) * Sw

            drice_dt = 0.0
            if ice_active and Nice > 0.0:
                Gi = G_ice(T, esi, P0)
                drice_dt = (Gi / max(r_ice, 1e-9)) * Si

            # prevent radii going negative
            r_cloud = max(r_cloud + drcloud_dt * dt, 0.0)
            r_ice   = max(r_ice   + drice_dt   * dt, 0.0)

            # --- Compute qcloud, qice
            qcloud = q_from_N_r(Ncloud, r_cloud, rho_l) if Ncloud > 0 else 0.0
            qice   = q_from_N_r(Nice,   r_ice,   rho_i) if Nice   > 0 else 0.0

            # --- Condensation/deposition rates as vapour sink
            # dm/dt per particle = 4*pi*r^2*rho * dr/dt
            cond_rate = 0.0
            if Ncloud > 0.0:
                dm_dt_one = 4.0 * math.pi * r_cloud**2 * rho_l * drcloud_dt
                cond_rate = Ncloud * dm_dt_one   # kg/m^3/s (can be negative if evaporation)

            dep_rate = 0.0
            if ice_active and Nice > 0.0:
                dm_dt_one = 4.0 * math.pi * r_ice**2 * rho_i * drice_dt
                dep_rate  = Nice * dm_dt_one

            # --- Update vapour pressure e using vapour mass sink:
            # ρv = e/(Rv*T)  =>  dρv/dt ≈ -(cond_rate + dep_rate)
            # de/dt = Rv*T*dρv/dt + (e/T)*dT/dt  (include cooling term)
            dT_dt = -cooling_rate
            drhov_dt = -(cond_rate + dep_rate)
            de_dt = Rv * T * drhov_dt + (e / T) * dT_dt

            e = max(e + de_dt * dt, 0.0)

            if int(t) % 60 == 0:
                print(f"{int(t):4d}  {T:7.2f}  {Sw: .3e}  {Si: .3e}   "
                      f"{1e6*r_cloud:8.3f}   {1e6*r_ice:7.3f}  "
                      f"{Ncloud: .3e}  {Nice: .3e}  {qcloud: .3e}  {qice: .3e}")

            wr.writerow([
                t, T, e, Sw, Si,
                Ncloud, Nice,
                r_cloud, r_ice,
                drcloud_dt, drice_dt,
                qcloud, qice,
                cond_rate, dep_rate,
                int(ice_active)
            ])

            # advance
            T = T + dT_dt * dt
            t += dt

    if ice_onset_t is not None:
        print(f"\nIce onset detected at t={ice_onset_t:.0f}s, T={ice_onset_T:.2f}K")
    else:
        print("\nIce onset not reached within simulation")

    print(f"Saved timeseries: {outfile}")

if __name__ == "__main__":
    run()