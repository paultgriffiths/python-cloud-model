import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_kid_case1_results(df):
    os.makedirs("figures", exist_ok=True)

    plt.figure()
    plt.plot(df["time"], df["cloud_mass"])
    plt.xlabel("Time (s)")
    plt.ylabel("Cloud mass (kg/kg)")
    plt.title("KiD Case 1 - Cloud Mass")
    plt.savefig("figures/kid_case1_cloud_mass.png", dpi=200, bbox_inches="tight")
    plt.close()

    plt.figure()
    plt.plot(df["time"], df["rain_mass"])
    plt.xlabel("Time (s)")
    plt.ylabel("Rain mass (kg/kg)")
    plt.title("KiD Case 1 - Rain Mass")
    plt.savefig("figures/kid_case1_rain_mass.png", dpi=200, bbox_inches="tight")
    plt.close()

    plt.figure()
    plt.plot(df["time"], df["surface_rain_rate"])
    plt.xlabel("Time (s)")
    plt.ylabel("Surface rain rate")
    plt.title("KiD Case 1 - Surface Rain Rate")
    plt.savefig("figures/kid_case1_surface_rain_rate.png", dpi=200, bbox_inches="tight")
    plt.close()

    plt.figure()
    plt.plot(df["time"], df["liquid_water_path"])
    plt.xlabel("Time (s)")
    plt.ylabel("Liquid water path (proxy)")
    plt.title("KiD Case 1 - Liquid Water Path")
    plt.savefig("figures/kid_case1_lwp.png", dpi=200, bbox_inches="tight")
    plt.close()


def main():
    df = pd.read_csv("data/kid_case1_results.csv")
    plot_kid_case1_results(df)
    print("Figures saved in figures/")


if __name__ == "__main__":
    main()