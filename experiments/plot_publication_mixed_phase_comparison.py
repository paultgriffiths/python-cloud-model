import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from netCDF4 import Dataset


# --------------------------------------------------
# Paths
# --------------------------------------------------

PYTHON_FILE = "data/mixed1_bioN_2500.csv"
KID_FILE = "/home/dryaktine/KiD-A/output/mixed1_out.nc"
OUTPUT_FILE = "figures/publication_mixed_phase_python_vs_kid.png"


# --------------------------------------------------
# Constants
# --------------------------------------------------

P0 = 101325.0       # Pa
Rd = 287.05         # J kg^-1 K^-1
Z_TARGET = 400.0    # m
T_END = 3600.0      # s


# --------------------------------------------------
# Read Python parcel-model output
# --------------------------------------------------

py = pd.read_csv(PYTHON_FILE)

py = py[py["t_s"] <= T_END].copy()

# qice in the simplified Python model is mass per unit volume
# [kg m^-3]. Convert to mixing ratio [kg kg^-1] for comparison
# with KiD/Thompson09.
rho_air = P0 / (Rd * py["T_K"])

py["qice_kgkg"] = py["qice"] / rho_air
py["Nice_m3"] = py["Nice"]


# --------------------------------------------------
# Read real KiD/Thompson09 output
# --------------------------------------------------

kid = Dataset(KID_FILE)

time_kid = np.asarray(kid.variables["time"][:])
z_kid = np.asarray(kid.variables["z"][:])

iz = int(np.argmin(np.abs(z_kid - Z_TARGET)))

if not np.isclose(z_kid[iz], Z_TARGET):
    raise ValueError(
        f"Requested z={Z_TARGET} m, nearest KiD level is {z_kid[iz]} m"
    )

mask = time_kid <= T_END

time_kid = time_kid[mask]

ice_kid = np.asarray(kid.variables["ice_mass"][iz, :])[mask]
snow_kid = np.asarray(kid.variables["snow_mass"][iz, :])[mask]
Nice_kid = np.asarray(kid.variables["ice_number"][iz, :])[mask]

kid.close()

frozen_kid = ice_kid + snow_kid


# --------------------------------------------------
# Diagnostics
# --------------------------------------------------

print(f"KiD comparison level: {z_kid[iz]:.1f} m")
print(f"Python final time: {py['t_s'].iloc[-1]:.1f} s")
print(f"KiD final time: {time_kid[-1]:.1f} s")

print(
    "Python max qice [kg/kg]:",
    f"{py['qice_kgkg'].max():.6e}",
)

print(
    "KiD max ice [kg/kg]:",
    f"{ice_kid.max():.6e}",
)

print(
    "KiD max total frozen (ice + snow) [kg/kg]:",
    f"{frozen_kid.max():.6e}",
)


# --------------------------------------------------
# Publication figure
# --------------------------------------------------

os.makedirs("figures", exist_ok=True)

fig, axes = plt.subplots(
    2,
    1,
    figsize=(7.0, 7.0),
    sharex=True,
)

# Panel (a): frozen condensate
axes[0].plot(
    py["t_s"],
    py["qice_kgkg"],
    linewidth=2.0,
    label="Python parcel model: ice",
)

axes[0].plot(
    time_kid,
    ice_kid,
    linewidth=2.0,
    label="KiD/Thompson09: ice",
)

axes[0].plot(
    time_kid,
    frozen_kid,
    linewidth=2.0,
    linestyle="--",
    label="KiD/Thompson09: ice + snow",
)

axes[0].set_ylabel("Frozen condensate (kg kg$^{-1}$)")
axes[0].set_yscale("log")
axes[0].set_title("(a) Frozen condensate at 400 m")
axes[0].grid(alpha=0.25)
axes[0].legend(frameon=False, loc="lower left", fontsize=8)


# Panel (b): ice number concentration
axes[1].plot(
    py["t_s"],
    py["Nice_m3"],
    linewidth=2.0,
    label="Python parcel model",
)

axes[1].plot(
    time_kid,
    Nice_kid,
    linewidth=2.0,
    label="KiD/Thompson09",
)

axes[1].set_xlabel("Time (s)")
axes[1].set_ylabel("Ice number concentration (m$^{-3}$)")
axes[1].set_yscale("log")
axes[1].set_title("(b) Ice number concentration at 400 m")
axes[1].grid(alpha=0.25)
axes[1].legend(frameon=False)

axes[1].set_xlim(0.0, T_END)

fig.tight_layout()

fig.savefig(
    OUTPUT_FILE,
    dpi=600,
    bbox_inches="tight",
)

plt.close(fig)

print(f"Saved: {OUTPUT_FILE}")
