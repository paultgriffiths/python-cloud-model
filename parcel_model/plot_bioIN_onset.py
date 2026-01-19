import matplotlib.pyplot as plt

# Data from run_bioIN_onset.py output
updraft_velocity = [0.2, 0.5, 1.0, 2.0]   # m/s
onset_time = [1109, 444, 222, 111]        # seconds

plt.figure(figsize=(6, 4))
plt.plot(updraft_velocity, onset_time, marker='o', linewidth=2)

plt.xlabel("Updraft velocity (m s$^{-1}$)")
plt.ylabel("Ice onset time (s)")
plt.title("Biological IN: Ice onset time vs updraft velocity")

plt.grid(True)
plt.tight_layout()

plt.savefig("bioIN_onset_vs_updraft.png", dpi=300)
plt.show()
