import csv
import matplotlib.pyplot as plt

def read_csv(fname):
    cols = {}
    with open(fname, "r", newline="") as f:
        reader = csv.DictReader(f)
        for k in reader.fieldnames:
            cols[k] = []
        for row in reader:
            for k in reader.fieldnames:
                cols[k].append(float(row[k]))
    return cols

def main():
    data = read_csv("mixed_phase_physics_timeseries.csv")
    t = data["t_s"]
    qice = data["qice"]
    Nice = data["Nice"]
    qcloud = data["qcloud"]
    Ncloud = data["Ncloud"]

    plt.figure(figsize=(8, 7))

    # 1) qcloud
    plt.subplot(2,2,1)
    plt.plot(t, qcloud)
    plt.xlabel("Time (s)")
    plt.ylabel("qcloud (proxy)")
    plt.title("Liquid water (qcloud)")

    # 2) Ncloud
    plt.subplot(2,2,2)
    plt.plot(t, Ncloud)
    plt.xlabel("Time (s)")
    plt.ylabel("Ncloud (m^-3)")
    plt.title("Activated droplets (Ncloud)")

    # 3) qice
    plt.subplot(2,2,3)
    plt.plot(t, qice)
    plt.xlabel("Time (s)")
    plt.ylabel("qice (proxy)")
    plt.title("Ice water (qice)")

    # 4) Nice
    plt.subplot(2,2,4)
    plt.plot(t, Nice)
    plt.xlabel("Time (s)")
    plt.ylabel("Nice (m^-3)")
    plt.title("Ice crystals (Nice)")

    plt.tight_layout()
    plt.savefig("mixed_phase_qN_summary.png", dpi=200)
    print("Saved: mixed_phase_qN_summary.png")

if __name__ == "__main__":
    main()
