import matplotlib.pyplot as plt
from run_mixed_phase_minimal import run_case


def main():
    w = 1.0

    A = run_case("Case A (no ice)", w, include_ice=False, verbose=False)
    B = run_case("Case B (biological IN enabled)", w, include_ice=True, verbose=False)

    plt.figure(figsize=(7, 4))
    plt.plot(A["times"], A["Ss"], label="No ice")
    plt.plot(B["times"], B["Ss"], label="Biological IN enabled")

    if B["ice_onset_time"] is not None:
        plt.axvline(B["ice_onset_time"], linestyle="--", label=f"Ice onset ({B['ice_onset_time']:.0f}s)")

    plt.axhline(0.0, linestyle="--")
    plt.xlabel("Time (s)")
    plt.ylabel("Supersaturation, S")
    plt.title(f"Mixed-phase prototype: S(t) comparison (w={w} m/s)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    outname = "mixed_phase_S_vs_time.png"
    plt.savefig(outname, dpi=200)
    print("Figure saved:", outname)


if __name__ == "__main__":
    main()
