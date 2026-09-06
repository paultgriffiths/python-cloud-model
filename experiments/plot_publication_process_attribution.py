import os

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# Paths
# --------------------------------------------------

DEPOSITION_FILE = "data/mixed1_integrated_deposition_summary.csv"
SEDIMENTATION_FILE = "data/mixed1_sedimentation_sensitivity_summary.csv"

OUTPUT_FILE = "figures/publication_mixed_phase_process_attribution.png"


# --------------------------------------------------
# Read committed diagnostic summaries
# --------------------------------------------------

dep = pd.read_csv(DEPOSITION_FILE)
sed = pd.read_csv(SEDIMENTATION_FILE)


# --------------------------------------------------
# Extract deposition diagnostics
# --------------------------------------------------

python_dep = dep.loc[
    dep["model"] == "Python",
    "integrated_positive_deposition_kgkg",
].iloc[0]

kid_dep = dep.loc[
    dep["model"] == "KiD_Thompson09_z400m",
    "integrated_positive_deposition_kgkg",
].iloc[0]

deposition_ratio = python_dep / kid_dep


# --------------------------------------------------
# Extract sedimentation diagnostics
# --------------------------------------------------

sed_on = sed.loc[
    sed["sedimentation"] == "ON",
    "frozen_400m_kgkg",
].iloc[0]

sed_off = sed.loc[
    sed["sedimentation"] == "OFF",
    "frozen_400m_kgkg",
].iloc[0]

sedimentation_ratio = sed_off / sed_on


# --------------------------------------------------
# Print quantitative diagnostics
# --------------------------------------------------

print(
    "Python integrated positive deposition [kg/kg]:",
    f"{python_dep:.6e}",
)

print(
    "KiD integrated positive deposition [kg/kg]:",
    f"{kid_dep:.6e}",
)

print(
    "Python / KiD deposition ratio:",
    f"{deposition_ratio:.3f}",
)

print(
    "KiD frozen condensate at 400 m, sedimentation ON [kg/kg]:",
    f"{sed_on:.6e}",
)

print(
    "KiD frozen condensate at 400 m, sedimentation OFF [kg/kg]:",
    f"{sed_off:.6e}",
)

print(
    "KiD OFF / ON frozen-condensate ratio:",
    f"{sedimentation_ratio:.3f}",
)


# --------------------------------------------------
# Publication figure
# --------------------------------------------------

os.makedirs("figures", exist_ok=True)

fig, axes = plt.subplots(
    1,
    2,
    figsize=(9.0, 4.2),
)


# Panel (a): integrated depositional growth
axes[0].bar(
    ["Python parcel\nmodel\n(bio-IN = 2500 m^-3)", "KiD/\nThompson09"],
    [python_dep, kid_dep],
)

axes[0].set_yscale("log")
axes[0].set_ylabel("Integrated positive deposition (kg kg$^{-1}$)")
axes[0].set_title("(a) Depositional growth, 0–3600 s")
axes[0].grid(axis="y", alpha=0.25)

axes[0].text(
    0.5,
    0.94,
    f"Python / KiD = {deposition_ratio:.2f}×",
    transform=axes[0].transAxes,
    ha="center",
    va="top",
)


# Panel (b): KiD sedimentation sensitivity
axes[1].bar(
    ["Sedimentation\nON", "Sedimentation\nOFF"],
    [sed_on, sed_off],
)

axes[1].set_yscale("log")
axes[1].set_ylabel("Frozen condensate at 400 m (kg kg$^{-1}$)")
axes[1].set_title("(b) KiD sedimentation sensitivity")
axes[1].grid(axis="y", alpha=0.25)

axes[1].text(
    0.5,
    0.94,
    f"OFF / ON = {sedimentation_ratio:.2f}×",
    transform=axes[1].transAxes,
    ha="center",
    va="top",
)


fig.tight_layout()

fig.savefig(
    OUTPUT_FILE,
    dpi=600,
    bbox_inches="tight",
)

plt.close(fig)

print(f"Saved: {OUTPUT_FILE}")
