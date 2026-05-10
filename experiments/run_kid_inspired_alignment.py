import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pandas as pd

from cases.kid_inspired_forcing import kid_inspired_updraft


# Simulation settings
dt = 1.0
t_end = 1200.0

times = np.arange(0, t_end + dt, dt)

results = []

for t in times:

    # Time-dependent updraft
    w = kid_inspired_updraft(t)

    results.append({
        "time_s": t,
        "w_mps": w
    })

# Save results
df = pd.DataFrame(results)

df.to_csv("data/kid_inspired_alignment.csv", index=False)

print("KiD-inspired forcing test completed.")
print("Saved: data/kid_inspired_alignment.csv")