from dataclasses import dataclass

@dataclass
class KiDCase1Config:
    dt: float = 1.0
    t_end: float = 3600.0

    z_top: float = 3000.0
    w1: float = 2.0
    t1: float = 3600.0
    t2: float = 600.0

    temperature_fixed: bool = True
    initial_temperature: float = 297.9
    initial_pressure: float = 100000.0
    initial_qv: float = 0.015

    ccn_concentration: float = 50e6
    enable_ice: bool = False
    enable_rain: bool = True

    initial_height: float = 0.0
