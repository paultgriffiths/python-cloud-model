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
# Threshold-based Python warm-rain model
# --------------------------------------------------

time_py = time_kid

cloud_py = np.zeros_like(time_py, dtype=float)
rain_py = np.zeros_like(time_py, dtype=float)

cloud_threshold = 0.55
autoconv_rate = 0.020

for i in range(1, len(time_py)):

    t = time_py[i]

    # cloud evolution
    if t < 1200:

        growth = 1.25 * (1.0 - np.exp(-t / 350.0))

        cloud_py[i] = growth

    else:

        cloud_py[i] = max(cloud_py[i-1] - 0.010, 0.0)

    # threshold-based rain conversion
    if cloud_py[i] > cloud_threshold:

        conversion = autoconv_rate * (cloud_py[i] - cloud_threshold)

        cloud_py[i] -= conversion

        rain_py[i] = rain_py[i-1] + conversion

    else:

        rain_py[i] = rain_py[i-1]

# --------------------------------------------------
# RMSE
# --------------------------------------------------

cloud_rmse = np.sqrt(np.mean((cloud_kid - cloud_py)**2))

rain_rmse = np.sqrt(np.mean((rain_kid - rain_py)**2))

# --------------------------------------------------
# MAE
# --------------------------------------------------

cloud_mae = np.mean(np.abs(cloud_kid - cloud_py))

rain_mae = np.mean(np.abs(rain_kid - rain_py))

# --------------------------------------------------
# Print results
# --------------------------------------------------

print("\n========== THRESHOLD MODEL METRICS ==========\n")

print(f"Cloud RMSE : {cloud_rmse:.4f}")
print(f"Rain RMSE  : {rain_rmse:.4f}")

print()

print(f"Cloud MAE  : {cloud_mae:.4f}")
print(f"Rain MAE   : {rain_mae:.4f}")

print("\n=============================================\n")
