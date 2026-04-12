from dataclasses import dataclass

@dataclass
class ParcelConfig:
    w: float = 1.0        # updraft (m/s)
    dt: float = 0.1       # timestep (s)
    t_end: float = 2000   # total time

    T0: float = 273.15    # temperature (K)
    p0: float = 85000     # pressure (Pa)

    ccn_conc: float = 1e8 # CCN
    in_conc: float = 1e3  # IN
