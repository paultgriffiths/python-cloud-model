# mixed_phase_state.py
from dataclasses import dataclass

@dataclass
class CloudState:
    # numbers (m^-3)
    Ncloud: float = 0.0
    Nice: float = 0.0

    # mass proxies (arbitrary units but consistent)
    qcloud: float = 0.0
    qice: float = 0.0
