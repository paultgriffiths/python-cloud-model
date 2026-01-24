import matplotlib.pyplot as plt

# ---- Data from mixed-phase sweep output ----
w = [0.2, 0.5, 1.0, 2.0]
S_noice = [5.915e-04, 1.520e-03, 3.188e-03, 7.031e-03]
S_ice   = [5.907e-04, 1.478e-03, 2.961e-03, 5.939e-03]

# ---- Plot ----
plt.figure(figsize=(7, 4.5))

plt.plot(w, S_noice, marker="o", linewidth=2, label="No ice (liquid-only)")
plt.plot(w, S_ice,   marker="o", linewidth=2, label="With biological IN (mixed-phase)")

plt.xlabel("Updraft velocity, $w$ (m s$^{-1}$)", fontsize=11)
plt.ylabel(r"Peak supersaturation, $S_{\mathrm{peak}}$", fontsize=11)
plt.title("Effect of updraft velocity on peak supersaturation", fontsize=12)

plt.grid(True, alpha=0.3)
plt.legend(frameon=False, fontsize=10)

plt.tight_layout()

outname = "mixed_phase_Speak_vs_updraft.png"
plt.savefig(outname, dpi=300)
print(f"Figure saved: {outname}")
