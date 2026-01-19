from biological_in import BiologicalIN, check_ice_nucleation


def run():
    # Example biological IN class
    bio = BiologicalIN(
        name="bioIN",
        N=50.0,        # m^-3 (toy value for testing)
        T50=263.15,    # -10 C
        width=2.0
    )

    # Test temperatures (K)
    temperatures = [
        273.15,  # 0 C
        268.15,  # -5 C
        263.15,  # -10 C
        258.15   # -15 C
    ]

    print("Biological Ice Nucleation Test")
    print("T (K)     frac_active     N_active (m^-3)    nucleated")
    print("--------------------------------------------------------")

    for T in temperatures:
        frac = bio.ice_active_fraction(T)
        nucleated, N_active = check_ice_nucleation(T, bio, N_threshold=1.0)
        print(f"{T:6.2f}     {frac:8.3f}        {N_active:10.3e}        {nucleated}")


if __name__ == "__main__":
    run()
