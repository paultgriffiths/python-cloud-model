import matplotlib.pyplot as plt

# Results from parcel model
pollen_N = [0, 100, 300, 1000, 3000, 10000]
S_peak = [6.818e-4, 6.743e-4, 6.594e-4, 6.100e-4, 4.869e-4, 1.947e-4]

# Replace zero with small value for log-scale plotting
pollen_N_plot = [1 if p == 0 else p for p in pollen_N]

# ---- Figure setup (paper-friendly) ----
plt.figure(figsize=(6.5, 4.2), dpi=120)

plt.plot(
    pollen_N_plot,
    S_peak,
    marker="o",
    markersize=5,
    linewidth=1.5
)

plt.xscale("log")

plt.xlabel(r"Pollen number concentration (m$^{-3}$)")
plt.ylabel(r"Peak supersaturation, $S_{\mathrm{peak}}$")

plt.title("Dependence of peak supersaturation on pollen concentration")

# Optional: indicate transition region (adjust if needed)
plt.axvline(1e3, linestyle="--", linewidth=1.0)
plt.text(1.05e3, max(S_peak)*0.98, "onset of strong\ncompetition", fontsize=9, va="top")

# Grid (light, readable)
plt.grid(True, which="both", linestyle=":", linewidth=0.8)

# Tight layout for clean margins
plt.tight_layout()

# Save high-resolution figure
plt.savefig("peak_supersaturation_vs_pollen.png", dpi=300)

# Show on screen
plt.show()
