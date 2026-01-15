import matplotlib.pyplot as plt

# Results from parcel model
pollen_N = [0, 100, 300, 1000, 3000, 10000]
S_peak = [6.818e-4, 6.743e-4, 6.594e-4, 6.100e-4, 4.869e-4, 1.947e-4]

# Replace zero with small value for log scale plotting
pollen_N_plot = [1 if p == 0 else p for p in pollen_N]

plt.figure()
plt.plot(pollen_N_plot, S_peak, marker='o', linestyle='-')

plt.xscale('log')
plt.xlabel('Pollen number concentration (m$^{-3}$)')
plt.ylabel('Peak supersaturation')
plt.title('Effect of pollen concentration on peak supersaturation')

plt.grid(True)
plt.tight_layout()
plt.show()
