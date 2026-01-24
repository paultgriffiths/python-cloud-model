from thermodynamics import saturation_vapor_pressure, supersaturation
from aerosol import AerosolPopulation
from activation import check_activation
from biological_in import BiologicalIN, check_ice_nucleation


def run_case(w, include_ice=True, dt=1.0, t_end=1200.0):
    """
    Run one parcel case at a given updraft velocity w (m/s).
    Returns:
        S_peak, t_peak, ice_onset_time, ice_onset_T
    """

    # -----------------------
    # Liquid CCN populations
    # -----------------------
    sulfate = AerosolPopulation(
        name="sulfate",
        N=500e6,        # m^-3  (500 cm^-3)
        radius=30e-9,
        kappa=1.0,
        rho_p=1770.0
    )

    pollen = AerosolPopulation(
        name="pollen",
        N=3000.0,       # m^-3
        radius=5e-6,
        kappa=0.1,
        rho_p=1000.0
    )

    # -----------------------
    # Biological IN population
    # -----------------------
    bio = BiologicalIN(
        name="bioIN",
        N=50.0,
        T50=263.15,   # -10 C
        width=2.0
    )

    # -----------------------
    # Parcel setup
    # -----------------------
    T = 273.15          # start at 0C
    RH0 = 0.95
    e = RH0 * saturation_vapor_pressure(T)

    # Simple mapping: updraft -> cooling rate
    cooling_rate = 0.01 * w  # K/s

    # Liquid vapour relaxation
    k_relax = 0.2

    # Ice deposition sink (only when ice_active)
    k_ice = 2.0

    ice_active = False
    ice_onset_time = None
    ice_onset_T = None

    S_peak = -999.0
    t_peak = None

    t = 0.0
    while t <= t_end:
        es = saturation_vapor_pressure(T)
        S = supersaturation(e, es)

        # Liquid activation checks
        check_activation(S, sulfate, T=T)
        check_activation(S, pollen, T=T)

        # Ice nucleation onset (switch)
        if include_ice and (not ice_active):
            nucleated, N_active = check_ice_nucleation(T, bio, N_threshold=1.0)
            if nucleated:
                ice_active = True
                ice_onset_time = t
                ice_onset_T = T

        # Liquid relaxation (condensation)
        if S > 0.0 and (sulfate.activated or pollen.activated):
            e = e - (k_relax * S * es * dt)
            if e < 0.0:
                e = 0.0

        # Ice deposition sink (very simple)
        if ice_active and S > 0.0:
            e = e - (k_ice * S * es * dt)
            if e < 0.0:
                e = 0.0

        # Track peak supersaturation using updated e
        es2 = saturation_vapor_pressure(T)
        S2 = supersaturation(e, es2)
        if S2 > S_peak:
            S_peak = S2
            t_peak = t

        # Cool parcel
        T = T - cooling_rate * dt
        t += dt

    return S_peak, t_peak, ice_onset_time, ice_onset_T


def run():
    w_values = [0.2, 0.5, 1.0, 2.0]

    print("Mixed-phase updraft sweep (with vs without ice)")
    print("w (m/s)   S_peak_noice   S_peak_ice    ice_onset_t (s)   ice_onset_T (K)")
    print("--------------------------------------------------------------------------")

    for w in w_values:
        S0, t0, _, _ = run_case(w, include_ice=False)
        S1, t1, ton, Ton = run_case(w, include_ice=True)

        ton_str = f"{ton:.0f}" if ton is not None else "NA"
        Ton_str = f"{Ton:.2f}" if Ton is not None else "NA"

        print(f"{w:6.1f}   {S0: .3e}     {S1: .3e}       {ton_str:>8}         {Ton_str:>8}")


if __name__ == "__main__":
    run()
