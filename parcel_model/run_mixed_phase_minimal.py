from thermodynamics import saturation_vapor_pressure, supersaturation
from aerosol import AerosolPopulation
from activation import check_activation
from biological_in import BiologicalIN, check_ice_nucleation


def run_case(label, w, include_ice=True, verbose=True):
    """
    Minimal mixed-phase prototype:
    - Liquid activation (kappa-Köhler)
    - Optional biological ice nucleation
    - Simple vapour relaxation + ice deposition sink
    Returns time series for plotting.
    """

    sulfate = AerosolPopulation(
        name="sulfate",
        N=500e6,
        radius=30e-9,
        kappa=1.0,
        rho_p=1770.0
    )

    pollen = AerosolPopulation(
        name="pollen",
        N=3000.0,
        radius=5e-6,
        kappa=0.1,
        rho_p=1000.0
    )

    bio = BiologicalIN(
        name="bioIN",
        N=50.0,
        T50=263.15,
        width=2.0
    )

    dt = 1.0
    t_end = 1200.0

    T = 273.15
    RH0 = 0.95
    e = RH0 * saturation_vapor_pressure(T)

    cooling_rate = 0.01 * w
    k_relax = 0.2

    ice_active = False
    ice_onset_time = None
    ice_onset_T = None

    S_peak = -999.0
    t_peak = None

    # time series storage
    times = []
    Ss = []
    Ts = []
    ice_flags = []

    if verbose:
        print(f"\n=== {label} | w={w:.2f} m/s | include_ice={include_ice} ===")
        print("t(s)   T(K)      S        ice_active  sulfate_act  pollen_act")

    t = 0.0
    while t <= t_end:
        es = saturation_vapor_pressure(T)
        S = supersaturation(e, es)

        check_activation(S, sulfate, T=T)
        check_activation(S, pollen, T=T)

        if include_ice and not ice_active:
            nucleated, _ = check_ice_nucleation(T, bio, N_threshold=1.0)
            if nucleated:
                ice_active = True
                ice_onset_time = t
                ice_onset_T = T

        # liquid sink
        if S > 0.0 and (sulfate.activated or pollen.activated):
            e -= k_relax * S * es * dt
            if e < 0.0:
                e = 0.0

        # ice sink (minimal)
        if ice_active and S > 0.0:
            k_ice = 2.0
            e -= k_ice * S * es * dt
            if e < 0.0:
                e = 0.0

        S2 = supersaturation(e, saturation_vapor_pressure(T))

        # store series
        times.append(t)
        Ss.append(S2)
        Ts.append(T)
        ice_flags.append(ice_active)

        if S2 > S_peak:
            S_peak = S2
            t_peak = t

        if verbose and int(t) % 60 == 0:
            print(f"{int(t):4d}  {T:7.2f}  {S2: .3e}    {str(ice_active):>5}        {str(sulfate.activated):>5}       {str(pollen.activated):>5}")

        T -= cooling_rate * dt
        t += dt

    if verbose:
        print(f"Peak S: {S_peak:.3e} at t={t_peak:.0f}s")
        if include_ice:
            if ice_active:
                print(f"Ice onset: t={ice_onset_time:.0f}s, T={ice_onset_T:.2f}K")
            else:
                print("Ice onset: not reached")

    return {
        "label": label,
        "w": w,
        "times": times,
        "Ss": Ss,
        "Ts": Ts,
        "ice_flags": ice_flags,
        "S_peak": S_peak,
        "t_peak": t_peak,
        "ice_onset_time": ice_onset_time,
        "ice_onset_T": ice_onset_T,
    }


def run():
    w = 1.0
    run_case("Case A (no ice)", w, include_ice=False, verbose=True)
    run_case("Case B (biological IN enabled)", w, include_ice=True, verbose=True)


if __name__ == "__main__":
    run()
