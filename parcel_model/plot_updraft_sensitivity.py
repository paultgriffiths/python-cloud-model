import matplotlib.pyplot as plt


def main():
    # Updraft velocity (m/s) and corresponding peak supersaturation
    w = [0.2, 0.5, 1.0, 2.0]
    S_peak = [1.317e-04, 3.336e-04, 6.818e-04, 1.425e-03]

    plt.figure()
    plt.plot(w, S_peak, marker="o")
    plt.xlabel("Updraft velocity, w (m/s)")
    plt.ylabel(r"Peak supersaturation, $S_{\mathrm{peak}}$")
    plt.title("Updraft sensitivity: peak supersaturation vs updraft velocity")
    plt.grid(True)

    plt.savefig("updraft_sensitivity_Speak_vs_w.png", dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
