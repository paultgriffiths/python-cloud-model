from thermodynamics import saturation_vapor_pressure, supersaturation
from aerosol import AerosolPopulation
from activation import check_activation


def parcel_run(pollen_N, label, dt=1.0):
    # --- Aerosol populations ---
    sulfate = AerosolPopulation(
        name="sulfate",
        N=500e6,        # m^-3  (500 cm^-3)
        radius=30e-9,
        kappa=1.0,
        rho_p=1770.0
    )

    pollen = AerosolPopulation(
        name="pollen",
        N=pollen_N,     # m^-3
        radius=5e-6,
        kappa=0.1,
        rho_p=1000.0
    )

    # --- Parcel setup ---
    t_end = 600.0

    T = 288.0
    cooling_rate = 0.01  # K/s

    RH0 = 0.95
    es0 = saturation_vapor_pressure(T)
    e = RH0 * es0

    # --- Condensation tuning ---
    k_base = 0.5

    # Reference sink scale based on sulfate (used to normalize sink_strength)
    sink_ref = sulfate.N * (sulfate.radius ** 2)

    # Track peak supersaturation
    S_peak = -999.0
    t_peak = None

    print("\n=== Case:", label, f"(dt={dt})", " | pollen_N =", pollen_N, "m^-3 ===")
    print("t(s)   T(K)        S         e(Pa)   sink_norm      sulfate_act  pollen_act")

    t = 0.0
    while t <= t_end:
        es = saturation_vapor_pressure(T)
        S = supersaturation(e, es)

        # Check activation status at current S
        act_s, Sc_s = check_activation(S, sulfate, T=T)
        act_p, Sc_p = check_activation(S, pollen, T=T)

        # --- Use a surface-area-like proxy: sum(N * r^2) ---
        sink_strength = 0.0
        if sulfate.activated:
            sink_strength += sulfate.N * (sulfate.radius ** 2)
        if pollen.activated:
            sink_strength += pollen.N * (pollen.radius ** 2)

        # Normalize to make it dimensionless-ish
        sink_norm = sink_strength / sink_ref if sink_ref > 0 else 0.0

        # Apply condensation only when supersaturated
        if S > 0.0:
            e = e - (k_base * sink_norm * S * es * dt)
            if e < 0.0:
                e = 0.0
            S = supersaturation(e, es)

        # Track peak S
        if S > S_peak:
            S_peak = S
            t_peak = t

        # Print every 60 seconds (approximately, depending on dt)
        if int(t) % 60 == 0:
            print(
                f"{int(t):4d}  {T:6.2f}  {S: .3e}  {e:8.2f}   {sink_norm: .3e}"
                f"      {str(sulfate.activated):>5}       {str(pollen.activated):>5}"
            )

        # Update temperature and time
        T = T - cooling_rate * dt
        t = t + dt

    print(f"Peak S for {label} (dt={dt}): {S_peak:.3e} at t = {t_peak:.0f} s")
    return S_peak, t_peak


def run():
    pollen_cases = [0.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0]
    dt_cases = [0.5, 1.0, 2.0]

    all_results = {}

    for dt in dt_cases:
        print("\n" + "=" * 70)
        print(f"TIME-STEP SENSITIVITY RUN: dt = {dt} s")
        print("=" * 70)

        results = []
        for pN in pollen_cases:
            S_peak, t_peak = parcel_run(pollen_N=pN, label=f"pollen_N={pN}", dt=dt)
            results.append((pN, S_peak, t_peak))

        all_results[dt] = results

        print("\n=== SUMMARY (dt = {:.1f} s): Peak supersaturation vs pollen concentration ===".format(dt))
        print("pollen_N (m^-3)     Peak S        t_peak (s)")
        for pN, S_peak, t_peak in results:
            print(f"{pN:12.1f}    {S_peak: .3e}     {t_peak:8.0f}")

    key_cases = [0.0, 3000.0, 10000.0]
    print("\n" + "=" * 70)
    print("COMPACT COMPARISON (Peak S) FOR KEY POLLEN CASES")
    print("=" * 70)
    header = "dt(s) " + " ".join([f"{int(k):>12d}" for k in key_cases])
    print(header)

    for dt in dt_cases:
        dt_map = {pN: S_peak for (pN, S_peak, _) in all_results[dt]}
        row = [f"{dt:4.1f}"]
        for k in key_cases:
            row.append(f"{dt_map[k]:12.3e}")
        print(" ".join(row))


if __name__ == "__main__":
    run()
