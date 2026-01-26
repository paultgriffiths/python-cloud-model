import matplotlib.pyplot as plt
from run_mixed_phase_minimal import run_case

def main():
    w = 1.0

    t_no, S_no, qi_no, _, _ = run_case("No ice", w=w, include_ice=False, verbose=False)
    t_ice, S_ice, qi_ice, onset_t, onset_T = run_case("With bio IN + growth", w=w, include_ice=True, verbose=False)

    # --- Figure 1: Supersaturation vs time ---
    plt.figure()
    plt.plot(t_no, S_no, label="No ice")
    plt.plot(t_ice, S_ice, label="Bio IN + ice growth")
    if onset_t is not None:
        plt.axvline(onset_t, linestyle="--", label=f"Ice onset (t={onset_t:.0f}s)")
    plt.xlabel("Time (s)")
    plt.ylabel("Supersaturation S")
    plt.title("Mixed-phase parcel: S(t) with/without ice growth")
    plt.legend()
    plt.tight_layout()
    plt.savefig("mixed_phase_S_vs_time_growth.png", dpi=200)
    print("Saved: mixed_phase_S_vs_time_growth.png")

    # --- Figure 2: Ice mass proxy qi vs time ---
    plt.figure()
    plt.plot(t_ice, qi_ice, label="qi (ice mass proxy)")
    if onset_t is not None:
        plt.axvline(onset_t, linestyle="--", label="Ice onset")
    plt.xlabel("Time (s)")
    plt.ylabel("qi (arb. units)")
    plt.title("Mixed-phase parcel: ice growth proxy qi(t)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("mixed_phase_qi_vs_time.png", dpi=200)
    print("Saved: mixed_phase_qi_vs_time.png")

if __name__ == "__main__":
    main()
