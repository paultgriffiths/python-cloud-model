import numpy as np
import pandas as pd
from netCDF4 import Dataset

PYTHON_FILE = "data/mixed1_bioN_2500.csv"
KID_FILE = "/home/dryaktine/KiD-A/output/mixed1_out.nc"
OUTPUT_FILE = "data/publication_mixed_phase_table.csv"

P0 = 101325.0
Rd = 287.05
Z_TARGET = 400.0
T_END = 3600.0

# Python matched-number sensitivity
py = pd.read_csv(PYTHON_FILE)
py = py[py["t_s"] <= T_END].copy()

rho_air = P0 / (Rd * py["T_K"])
py["qice_kgkg"] = py["qice"] / rho_air

py_max_qice = py["qice_kgkg"].max()
py_t_max_qice = py.loc[py["qice_kgkg"].idxmax(), "t_s"]
py_max_Nice = py["Nice"].max()

# KiD / Thompson09
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

kid_max_ice = ice_kid.max()
kid_t_max_ice = time_kid[np.argmax(ice_kid)]

kid_max_frozen = frozen_kid.max()
kid_t_max_frozen = time_kid[np.argmax(frozen_kid)]

kid_max_Nice = Nice_kid.max()

ratio_qice_to_frozen = py_max_qice / kid_max_frozen

table = pd.DataFrame(
    [
        {
            "metric": "Maximum ice number concentration",
            "Python_parcel_model": py_max_Nice,
            "KiD_Thompson09": kid_max_Nice,
            "units": "m^-3",
            "notes": "Matched-number sensitivity; Python bio-IN input = 2500 m^-3",
        },
        {
            "metric": "Maximum cloud ice mixing ratio",
            "Python_parcel_model": py_max_qice,
            "KiD_Thompson09": kid_max_ice,
            "units": "kg kg^-1",
            "notes": (
                f"Python maximum at {py_t_max_qice:.0f} s; "
                f"KiD ice maximum at {kid_t_max_ice:.0f} s"
            ),
        },
        {
            "metric": "Maximum total frozen mixing ratio",
            "Python_parcel_model": np.nan,
            "KiD_Thompson09": kid_max_frozen,
            "units": "kg kg^-1",
            "notes": f"KiD ice + snow maximum at {kid_t_max_frozen:.0f} s",
        },
        {
            "metric": "Python max ice / KiD max total frozen",
            "Python_parcel_model": ratio_qice_to_frozen,
            "KiD_Thompson09": np.nan,
            "units": "ratio",
            "notes": "Maximum-to-maximum comparison, not same-time comparison",
        },
    ]
)

table.to_csv(OUTPUT_FILE, index=False)

print(table.to_string(index=False))
print()
print(f"Saved: {OUTPUT_FILE}")
