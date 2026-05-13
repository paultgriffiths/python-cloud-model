import numpy as np
from netCDF4 import Dataset

# --------------------------------------------------
# Read KiD benchmark output
# --------------------------------------------------

kid = Dataset("/home/dryaktine/KiD-A/output/warm1_output.nc")

time_kid = kid.variables["time"][:]
cloud_kid = kid.variables["cloud_mass_path"][:]
rain_kid = kid.variables["rain_mass_path"][:]

# --------------------------------------------------
# Improved Python alignment model
# --------------------------------------------------

dt = 30.0
t_end = 3600

time_py = time_kid

cloud_py = np.zeros_like(time_py, dtype=float)
rain_py = np.zeros_like(time_py, dtype=float)

for i in range(1, len(time_py)):

    t = time_py[i]

    # cloud evolution
    if t < 1200:
        cloud_py[i] = 1.25 * (1.0 - np.exp(-t / 400.0))

    else:
        cloud_py[i] = max(cloud_py[i-1] - 0.018, 0.0)

    # rain evolution
    if t > 900:
        rain_py[i] = 0.85 * (1.0 - np.exp(-(t - 900) / 700.0))

# --------------------------------------------------
# RMSE calculations
# --------------------------------------------------

cloud_rmse = np.sqrt(np.mean((cloud_kid - cloud_py)**2))

rain_rmse = np.sqrt(np.mean((rain_kid - rain_py)**2))

# --------------------------------------------------
# Mean absolute error
# --------------------------------------------------

cloud_mae = np.mean(np.abs(cloud_kid - cloud_py))

rain_mae = np.mean(np.abs(rain_kid - rain_py))

# --------------------------------------------------
# Print results
# --------------------------------------------------

print("\n========== ERROR METRICS ==========\n")

print(f"Cloud RMSE : {cloud_rmse:.4f}")
print(f"Rain RMSE  : {rain_rmse:.4f}")

print()

print(f"Cloud MAE  : {cloud_mae:.4f}")
print(f"Rain MAE   : {rain_mae:.4f}")

print("\n===================================\n")
