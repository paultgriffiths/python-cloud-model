import matplotlib.pyplot as plt
from run_mixed_phase_physics import run  # لازم run() ترجع timeseries

def main():
    out = run(return_series=True)  # غادي نصلحوها فـ run_mixed_phase_physics.py
    t = out["t"]
    qcloud = out["qcloud"]
    qice = out["qice"]
    Ncloud = out["Ncloud"]
    Nice = out["Nice"]
    onset_t = out["ice_onset_t"]

    # Figure: qcloud & qice
    plt.figure()
    plt.plot(t, qcloud, label="qcloud (liquid)")
    plt.plot(t, qice, label="qice (ice)")
    if onset_t is not None:
        plt.axvline(onset_t, linestyle="--", label="ice onset")
    plt.xlabel("Time (s)")
    plt.ylabel("Mass proxy (arb.)")
    plt.title("Water substance partition: liquid vs ice")
    plt.legend()
    plt.tight_layout()
    plt.savefig("mixed_phase_qice_qcloud_vs_time.png", dpi=200)
    print("Saved: mixed_phase_qice_qcloud_vs_time.png")

    # Figure: Ncloud & Nice
    plt.figure()
    plt.plot(t, Ncloud, label="Ncloud")
    plt.plot(t, Nice, label="Nice")
    if onset_t is not None:
        plt.axvline(onset_t, linestyle="--", label="ice onset")
    plt.xlabel("Time (s)")
    plt.ylabel("Number concentration (m^-3)")
    plt.title("Number evolution: droplets vs ice")
    plt.legend()
    plt.tight_layout()
    plt.savefig("mixed_phase_Nice_Ncloud_vs_time.png", dpi=200)
    print("Saved: mixed_phase_Nice_Ncloud_vs_time.png")

if __name__ == "__main__":
    main()
