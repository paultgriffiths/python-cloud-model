from thermodynamics import saturation_vapor_pressure, supersaturation
from aerosol import AerosolPopulation
from activation import check_activation
from biological_in import BiologicalIN, check_ice_nucleation


def run_case(label, w, include_ice=True, verbose=True):
    """
    Minimal mixed-phase prototype:
    - Liquid activation (kappa-Köhler)
    - Biological IN onset (optional)
    - Simple vapour relaxation + simple ice deposition sink
    - Simple ice growth proxy qi(t)
    Returns: times, S_series, qi_series, ice_onset_time, ice_onset_T
    """

    # -----------------------
    # Aerosol populations (liquid CCN)
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
    # Biological IN population (ice)
    # -----------------------
    bio = BiologicalIN(
        name="bioIN",
        N=50.0,
        T50=263.15,     # -10 C (example)
        width=2.0
    )

    # -----------------------
    # Parcel setup
    # -----------------------
    dt = 1.0
    t_end = 1200.0

    T = 273.15          # start at 0C
    RH0 = 0.95
    e = RH0 * saturation_vapor_pressure(T)

    # Updraft -> cooling-rate mapping (simple, consistent with earlier)
    cooling_rate = 0.01 * w  # K/s

    # Liquid vapour relaxation (stable small coefficient)
    k_relax = 0.2

    # Ice deposition sink coefficient (make small; increase later if needed)
    k_ice = 0.4

    # -----------------------
    # Ice growth proxy qi(t)
    # -----------------------
    qi = 0.0
    qi_growth_coeff = 5e-12  # controls qi increase rate (tunable)

    # Ice onset control
    ice_active = False
    ice_onset_time = None
    ice_onset_T = None

    # Output time series for plotting
    times = []
    S_series = []
    qi_series = []

    # Track peak S (diagnostic)
    S_peak = -999.0
    t_peak = None

    if verbose:
        print(f"\n=== {label} | w={w:.2f} m/s | include_ice={include_ice} ===")
        print("t(s)   T(K)      S         ice_active    qi        sulfate_act  pollen_act")

    t = 0.0
    while t <= t_end:
        es = saturation_vapor_pressure(T)
        S = supersaturation(e, es)

        # Liquid activation
        check_activation(S, sulfate, T=T)
        check_activation(S, pollen, T=T)

        # -----------------------
        # Step 1: Biological IN onset switch
        # -----------------------
        if include_ice and (not ice_active):
            nucleated, N_active = check_ice_nucleation(T, bio, N_threshold=1.0)
            if nucleated:
                ice_active = True
                ice_onset_time = t
                ice_onset_T = T

        # -----------------------
        # Liquid vapour relaxation (only when supersaturated and activated)
        # -----------------------
        if S > 0.0 and (sulfate.activated or pollen.activated):
            e = e - (k_relax * S * es * dt)
            if e < 0.0:
                e = 0.0

        # -----------------------
        # Step 2: Minimal ice deposition sink + simple growth proxy
        # -----------------------
        if ice_active and S > 0.0:
            # remove additional vapour when supersaturated (simple deposition)
            e = e - (k_ice * S * es * dt)
            if e < 0.0:
                e = 0.0

            # update qi proxy (just to show growth once ice is active)
            qi += qi_growth_coeff * S * es * dt

        # Recompute S after sinks
        es2 = saturation_vapor_pressure(T)
        S2 = supersaturation(e, es2)

        # Save time series
        times.append(t)
        S_series.append(S2)
        qi_series.append(qi)

        # Track peak S
        if S2 > S_peak:
            S_peak = S2
            t_peak = t

        # Print every 60s
        if verbose and (int(t) % 60 == 0):
            print(
                f"{int(t):4d}  {T:7.2f}  {S2: .3e}    {str(ice_active):>5}   "
                f"{qi:10.3e}     {str(sulfate.activated):>5}       {str(pollen.activated):>5}"
            )

        # Update temperature (cooling)
        T = T - cooling_rate * dt
        t += dt

    if verbose:
        print(f"Peak S: {S_peak:.3e} at t={t_peak:.0f}s")
        if include_ice:
            if ice_active:
                print(f"Ice onset: t={ice_onset_time:.0f}s, T={ice_onset_T:.2f}K")
            else:
                print("Ice onset: not reached within simulation")

    return times, S_series, qi_series, ice_onset_time, ice_onset_T


def run():
    w = 1.0
    run_case(label="Case A (no ice)", w=w, include_ice=False, verbose=True)
    run_case(label="Case B (biological IN enabled)", w=w, include_ice=True, verbose=True)


if __name__ == "__main__":
    run()
