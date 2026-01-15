from thermodynamics import saturation_vapor_pressure, supersaturation
from aerosol import AerosolPopulation
from activation import check_activation

def run():
    # --- Define aerosol populations ---
    sulfate = AerosolPopulation(
        name="sulfate",
        N=500e6,        # m^-3
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

    # --- Simple parcel setup ---
    dt = 1.0            # time step (s)
    t_end = 600.0       # total time (s)

    T = 288.0           # initial temperature (K)
    cooling_rate = 0.01 # K/s

    RH0 = 0.95          # initial relative humidity (0-1)

    # Initial vapor pressure e
    es0 = saturation_vapor_pressure(T)
    e = RH0 * es0

    # --- Simple condensation "sink" strength ---
    # Larger k_cond -> stronger removal of vapor when S > 0
    k_cond = 0.5

    print("t(s)   T(K)        S          e(Pa)    sulfate_act  pollen_act")

    t = 0.0
    while t <= t_end:
        es = saturation_vapor_pressure(T)
        S = supersaturation(e, es)

        # --- Simple condensation: if supersaturated, reduce e to limit S ---
        if S > 0.0:
            e = e - (k_cond * S * es * dt)
            # Safety: do not allow e to go negative
            if e < 0.0:
                e = 0.0
            # Recompute S after condensation adjustment
            S = supersaturation(e, es)

        act_s, Sc_s = check_activation(S, sulfate, T=T)
        act_p, Sc_p = check_activation(S, pollen, T=T)

        # Print every 60 seconds
        if int(t) % 60 == 0:
            print(f"{int(t):4d}  {T:6.2f}  {S: .3e}  {e:9.2f}     {str(act_s):>5}       {str(act_p):>5}")

        # Update temperature (cooling)
        T = T - cooling_rate * dt
        t = t + dt

if __name__ == "__main__":
    run()

