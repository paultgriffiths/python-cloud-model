import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv("mixed_phase_physics_timeseries.csv")

    t = df["t_s"]
    qcloud = df["qcloud"]
    qice = df["qice"]
    Ncloud = df["Ncloud"]
    Nice = df["Nice"]

    # Figure: qcloud & qice
    plt.figure()
    plt.plot(t, qcloud, label="qcloud (liquid)")
    plt.plot(t, qice, label="qice (ice)")
    plt.xlabel("Time (s)")
    plt.ylabel("Water mass proxy (arb. units)")
    plt.title("Mixed-phase parcel: liquid vs ice mass")
    plt.legend()
    plt.tight_layout()
    plt.savefig("mixed_phase_qcloud_qice_vs_time.png", dpi=200)
    print("Saved: mixed_phase_qcloud_qice_vs_time.png")

    # Figure: Ncloud & Nice
    plt.figure()
    plt.plot(t, Ncloud, label="Ncloud (droplets)")
    plt.plot(t, Nice, label="Nice (ice)")
    plt.xlabel("Time (s)")
    plt.ylabel("Number concentration (m^-3)")
    plt.title("Mixed-phase parcel: droplet vs ice number")
    plt.legend()
    plt.tight_layout()
    plt.savefig("mixed_phase_Ncloud_Nice_vs_time.png", dpi=200)
    print("Saved: mixed_phase_Ncloud_Nice_vs_time.png")

if __name__ == "__main__":
    main()
