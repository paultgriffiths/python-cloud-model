import os

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# Input / output files
# --------------------------------------------------

NUMBER_FILE = "data/clean_aerosol_number_sensitivity.csv"
RADIUS_FILE = "data/clean_aerosol_radius_sensitivity.csv"
KAPPA_FILE = "data/clean_kappa_sensitivity.csv"
TIMESTEP_FILE = "data/clean_timestep_sensitivity.csv"

OUTPUT_FILE = "figures/publication_warm_cloud_sensitivity.png"


# --------------------------------------------------
# Read reproducible clean-baseline experiments
# --------------------------------------------------

number = pd.read_csv(NUMBER_FILE)
radius = pd.read_csv(RADIUS_FILE)
kappa = pd.read_csv(KAPPA_FILE)
timestep = pd.read_csv(TIMESTEP_FILE)


# --------------------------------------------------
# Print diagnostics used in the figure
# --------------------------------------------------

print(
    "Aerosol-number SSmax range [%]:",
    f"{number['SSmax_percent'].max():.6f}",
    "to",
    f"{number['SSmax_percent'].min():.6f}",
)

print(
    "Dry-radius t50 range [s]:",
    f"{radius['t_50pct_s'].max():.1f}",
    "to",
    f"{radius['t_50pct_s'].min():.1f}",
)

print(
    "Kappa t50 range [s]:",
    f"{kappa['t_50pct_s'].max():.1f}",
    "to",
    f"{kappa['t_50pct_s'].min():.1f}",
)

print(
    "Timestep SSmax range [%]:",
    f"{timestep['SSmax_percent'].max():.6f}",
    "to",
    f"{timestep['SSmax_percent'].min():.6f}",
)


# --------------------------------------------------
# Publication figure
# --------------------------------------------------

os.makedirs("figures", exist_ok=True)

fig, axes = plt.subplots(
    2,
    2,
    figsize=(9.0, 7.2),
)


# (a) Aerosol number concentration
axes[0, 0].plot(
    number["aerosol_N_m3"] / 1.0e6,
    number["SSmax_percent"],
    marker="o",
)

axes[0, 0].set_xlabel("Aerosol number concentration (cm$^{-3}$)")
axes[0, 0].set_ylabel("Maximum supersaturation (%)")
axes[0, 0].set_title("(a) Aerosol-number sensitivity")
axes[0, 0].grid(alpha=0.25)


# (b) Dry aerosol radius
axes[0, 1].plot(
    radius["aerosol_radius_um"],
    radius["t_50pct_s"],
    marker="o",
)

axes[0, 1].set_xlabel("Dry aerosol radius ($\\mu$m)")
axes[0, 1].set_ylabel("50% activation time (s)")
axes[0, 1].set_title("(b) Dry-radius sensitivity")
axes[0, 1].grid(alpha=0.25)


# (c) Hygroscopicity
axes[1, 0].plot(
    kappa["kappa"],
    kappa["t_50pct_s"],
    marker="o",
)

axes[1, 0].set_xlabel("Hygroscopicity, $\\kappa$")
axes[1, 0].set_ylabel("50% activation time (s)")
axes[1, 0].set_title("(c) Hygroscopicity sensitivity")
axes[1, 0].grid(alpha=0.25)


# (d) Timestep convergence
axes[1, 1].plot(
    timestep["dt_s"],
    timestep["SSmax_percent"],
    marker="o",
)

axes[1, 1].set_xlabel("Timestep (s)")
axes[1, 1].set_ylabel("Maximum supersaturation (%)")
axes[1, 1].set_title("(d) Timestep convergence")
axes[1, 1].grid(alpha=0.25)


fig.tight_layout()

fig.savefig(
    OUTPUT_FILE,
    dpi=600,
    bbox_inches="tight",
)

plt.close(fig)

print(f"Saved: {OUTPUT_FILE}")
