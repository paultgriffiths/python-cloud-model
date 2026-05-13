import numpy as np
from netCDF4 import Dataset

# --------------------------------------------------
# Read KiD benchmark data
# --------------------------------------------------

kid = Dataset("/home/dryaktine/KiD-A/output/warm1_output.nc")

time_kid = kid.variables["time"][:]
cloud_kid = kid.variables["cloud_mass_path"][:]
rain_kid = kid.variables["rain_mass_path"][:]

# --------------------------------------------------
# Simplified Python alignment model
# --------------------------------------------------

dt = 30.0
t_end = 3600

time_py = np.arange(0, t_end + dt, dt)

cloud_py = np.zeros_like(time_py, dtype=float)
rain_py = np.zeros_like(time_py, dtype=float)

for i in range(1, len(time_py)):

    t = time_py[i]

    # improved cloud growth
    if t < 1200:
        cloud_py[i] = 1.25 * (1.0 - np.exp(-t / 400.0))

    else:
        cloud_py[i] = max(cloud_py[i-1] - 0.018, 0.0)

    # delayed rain onset
    if t > 900:
        rain_py[i] = 0.85 * (1.0 - np.exp(-(t - 900) / 700.0))

# --------------------------------------------------
# Quantitative metrics
# --------------------------------------------------

kid_cloud_peak = np.max(cloud_kid)
py_cloud_peak = np.max(cloud_py)

kid_rain_peak = np.max(rain_kid)
py_rain_peak = np.max(rain_py)

kid_cloud_peak_time = time_kid[np.argmax(cloud_kid)]
py_cloud_peak_time = time_py[np.argmax(cloud_py)]

kid_rain_peak_time = time_kid[np.argmax(rain_kid)]
py_rain_peak_time = time_py[np.argmax(rain_py)]

# --------------------------------------------------
# Print results
# --------------------------------------------------

print("\n========== QUANTITATIVE COMPARISON ==========\n")

print(f"KiD cloud peak       : {kid_cloud_peak:.4f}")
print(f"Python cloud peak    : {py_cloud_peak:.4f}")

print()

print(f"KiD rain peak        : {kid_rain_peak:.4f}")
print(f"Python rain peak     : {py_rain_peak:.4f}")

print()

print(f"KiD cloud peak time  : {kid_cloud_peak_time:.1f} s")
print(f"Python cloud peak    : {py_cloud_peak_time:.1f} s")

print()

print(f"KiD rain peak time   : {kid_rain_peak_time:.1f} s")
print(f"Python rain peak     : {py_rain_peak_time:.1f} s")

print("\n=============================================\n")
