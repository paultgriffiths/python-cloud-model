# aerosol.py

class AerosolPopulation:
    def __init__(self, name, N, radius, kappa, rho_p):
        self.name = name        # population name
        self.N = N              # number concentration (m^-3)
        self.radius = radius    # particle radius (m)
        self.kappa = kappa      # hygroscopicity parameter
        self.rho_p = rho_p      # particle density (kg/m^3)
        self.activated = False # activation flag
