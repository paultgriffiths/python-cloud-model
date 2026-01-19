from biological_in import BiologicalIN, check_ice_nucleation


def run_case(cooling_rate, label):
    dt = 1.0
    t_end = 1200.0  # run longer to reach colder temperatures
    T0 = 273.15     # start at 0 C

    bio = BiologicalIN(
        name="bioIN",
        N=50.0,
        T50=263.15,   # -10 C
        width=2.0
    )

    t = 0.0
    T = T0

    onset_time = None
    onset_T = None
    onset_Nactive = None

    while t <= t_end:
        nucleated, N_active = check_ice_nucleation(T, bio, N_threshold=1.0)
        if nucleated:
            onset_time = t
            onset_T = T
            onset_Nactive = N_active
            break

        # cool parcel
        T = T - cooling_rate * dt
        t += dt

    return onset_time, onset_T, onset_Nactive


def run():
    cases = {
        "w = 0.2 m/s": 0.002,
        "w = 0.5 m/s": 0.005,
        "w = 1.0 m/s": 0.010,
        "w = 2.0 m/s": 0.020,
    }

    print("Biological IN onset test (cooling parcel)")
    print("Case              Cooling rate (K/s)    onset_t (s)    onset_T (K)    N_active (m^-3)")
    print("------------------------------------------------------------------------------------")

    for label, rate in cases.items():
        onset_t, onset_T, Nact = run_case(rate, label)
        if onset_t is None:
            print(f"{label:16s} {rate:12.3f}     None          None         None")
        else:
            print(f"{label:16s} {rate:12.3f}   {onset_t:10.0f}    {onset_T:10.2f}    {Nact:12.3e}")


if __name__ == "__main__":
    run()
