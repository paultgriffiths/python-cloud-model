import csv
from thermodynamics import saturation_vapor_pressure, supersaturation
from aerosol import AerosolPopulation
from activation import check_activation
from biological_in import BiologicalIN, check_ice_nucleation

# If you already have an ice vapour pressure function in your code, use it.
# Otherwise, we approximate e_si using a simple factor to keep the skeleton stable.
# (You can later replace this with a proper e_si(T) parameterisation.)
def saturation_vapor_pressure_ice_approx(T):
    # crude approximation: ice saturation slightly lower than liquid near 0C
    # replace later with a proper e_si(T)
    return 0.9 * saturation_vapor_pressure(T)

def run(w=1.0, dt=1.0, t_end=1200.0, outfile="mixed_phase_physics_timeseries.csv"):
    # --- Aerosol populations (liquid CCN)
    sulfate = AerosolPopulation("sulfate", N=500e6, radius=30e-9, kappa=1.0, rho_p=1770.0)
    pollen  = AerosolPopulation("pollen",  N=3000.0, radius=5e-6, kappa=0.1, rho_p=1000.0)

    # --- Biological IN population (ice)
    bio = BiologicalIN(name="bioIN", N=50.0, T50=263.15, width=2.0)  # tweak later

    # --- Parcel setup
    T = 273.15
    RH0 = 0.95
    e = RH0 * saturation_vapor_pressure(T)

    cooling_rate = 0.01 * w  # K/s

    # --- Simple bulk “water substance” proxies
    qcloud = 0.0  # liquid water proxy
    qice   = 0.0  # ice water proxy

    ice_active = False
    ice_onset_t = None
    ice_onset_T = None

    # --- Tunable sink strengths (prototype)
    k_liq = 0.20    # liquid condensation/evap strength
    k_ice = 0.80    # ice deposition/sublim strength (make larger to see B-F)

    print("\nMixed-phase physics run")
    print(f"w={w:.2f} m/s, cooling_rate={cooling_rate:.4f} K/s, dt={dt}, t_end={t_end}")
    print("t(s)   T(K)     Sw         Si        ice_active    qcloud      qice        Ncloud     Nice")

    with open(outfile, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "t_s","T_K","Sw","Si","e_Pa",
            "dqcloud_dt","dqice_dt",
            "qcloud","qice",
            "Ncloud","Nice",
            "ice_active"
        ])

        t = 0.0
        while t <= t_end:
            esw = saturation_vapor_pressure(T)
            esi = saturation_vapor_pressure_ice_approx(T)

            Sw = supersaturation(e, esw)
            Si = (e/esi) - 1.0

            # --- Liquid activation (counts)
            check_activation(Sw, sulfate, T=T)
            check_activation(Sw, pollen,  T=T)

            Ncloud = 0.0
            if sulfate.activated:
                Ncloud += sulfate.N
            if pollen.activated:
                Ncloud += pollen.N

            # --- Ice nucleation (Nice)
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
                # once ice is active, keep Nice as “active fraction” * N
                # (simple; you can later evolve Nice with time)
                _, N_active = check_ice_nucleation(T, bio, N_threshold=0.0)
                Nice = N_active

            # --- Vapour tendencies (prototype, sign-aware)
            # Liquid: if Sw>0 => condense (dqcloud_dt positive, vapour decreases)
            #         if Sw<0 => evaporate (dqcloud_dt negative, vapour increases)
            dqcloud_dt = 0.0
            if Ncloud > 0.0:
                dqcloud_dt = k_liq * Sw

            # Ice: if Si>0 and ice_active => deposition (dqice_dt positive)
            #      if Si<0 => sublimation (dqice_dt negative)
            dqice_dt = 0.0
            if ice_active and Nice > 0.0:
                dqice_dt = k_ice * Si

            # --- Update proxies
            qcloud += dqcloud_dt * dt
            qice   += dqice_dt   * dt

            # --- Vapour update: remove vapour when condens/deposit; add when evap/sublim
            # (This is a toy mapping; later you’ll replace with proper vapour budget in Pa/s)
            e = e - (dqcloud_dt + dqice_dt) * esw * dt
            if e < 0.0:
                e = 0.0

            # --- Print every 60s
            if int(t) % 60 == 0:
                print(f"{int(t):4d}  {T:7.2f}  {Sw: .3e}  {Si: .3e}   {str(ice_active):>5}   "
                      f"{qcloud: .3e}  {qice: .3e}  {Ncloud: .3e}  {Nice: .3e}")

            writer.writerow([t, T, Sw, Si, e, dqcloud_dt, dqice_dt, qcloud, qice, Ncloud, Nice, int(ice_active)])

            # --- advance
            T = T - cooling_rate * dt
            t += dt

    if ice_onset_t is not None:
        print(f"\nIce onset detected at t={ice_onset_t:.0f}s, T={ice_onset_T:.2f}K")
    else:
        print("\nIce onset not reached within simulation")

    print(f"Saved timeseries: {outfile}")

if __name__ == "__main__":
    run()
