from thermodynamics import saturation_vapor_pressure, supersaturation
from aerosol import AerosolPopulation
from activation import check_activation


def parcel_run(cooling_rate, label):
    # --- Aerosol population (keep it simple for stability test) ---
    sulfate = AerosolPopulation(
        name="sulfate",
        N=500e6,        # m^-3  (500 cm^-3)
        radius=30e-9,
        kappa=1.0,
        rho_p=1770.0
    )

    # --- Parcel setup ---
    dt = 1.0
    t_end = 600.0

    T = 288.0
    RH0 = 0.95
    es0 = saturation_vapor_pressure(T)
    e = RH0 * es0

    # Track peak supersaturation
    S_peak = -999.0
    t_peak = None

    t = 0.0
    while t <= t_end:
        es = saturation_vapor_pressure(T)
        S = supersaturation(e, es)

        # Activation check (not strictly required for this test, but informative)
        act, Sc = check_activation(S, sulfate, T=T)

        # --- Simple explicit condensation sink (stability-focused) ---
        if S > 0.0:
            e = e - (0.5 * S * es * dt)
            if e < 0.0:
                e = 0.0
            S = supersaturation(e, es)

        # Track peak S
        if S > S_peak:
            S_peak = S
            t_peak = t

        # Update temperature (cooling)
        T = T - cooling_rate * dt
        t = t + dt

    return S_peak, t_peak


def run():
    # Map updraft cases to representative cooling rates (K/s)
    cooling_cases = {
        "w = 0.2 m/s": 0.002,
        "w = 0.5 m/s": 0.005,
        "w = 1.0 m/s": 0.010,
        "w = 2.0 m/s": 0.020,
    }

    print("Updraft / cooling-rate sensitivity test")
    print("Case              Cooling rate (K/s)      Peak S        t_peak (s)")
    print("-------------------------------------------------------------------")

    for label, rate in cooling_cases.items():
        S_peak, t_peak = parcel_run(rate, label)
        print(f"{label:16s} {rate:12.3f}        {S_peak: .3e}     {t_peak:8.0f}")


if __name__ == "__main__":
    run()
