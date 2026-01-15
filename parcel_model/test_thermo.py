from thermodynamics import saturation_vapor_pressure

T = 288.0  # Representative temperature (Kelvin)
es = saturation_vapor_pressure(T)

print("Saturation vapor pressure =", es, "Pa")
