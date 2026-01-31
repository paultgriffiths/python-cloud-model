import matplotlib.pyplot as plt
import numpy as np

def main():
    # Time setup
    dt = 1.0          # seconds
    t_end = 1200.0    # seconds
    t = np.arange(0, t_end + dt, dt)

    # Initial temperature
    T0 = 273.15       # K
    w = 1.0           # m/s
    cooling_rate = 0.01 * w  # K/s

    # Temperature evolution
    T = T0 - cooling_rate * t

    # Plot
    plt.figure()
    plt.plot(t, T)
    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (K)")
    plt.title("Parcel temperature evolution T(t)")
    plt.tight_layout()
    plt.savefig("temperature_vs_time.png", dpi=200)

    print("Saved: temperature_vs_time.png")

if __name__ == "__main__":
    main()
