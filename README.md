[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
![Research Code](https://img.shields.io/badge/code-research-blueviolet.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-research--prototype-orange.svg)

# Python Cloud Parcel Model

A physically based **cloud parcel model** implemented in Python to investigate aerosol activation, vapour competition, and mixed-phase cloud microphysics.

The model is designed as a **transparent research framework** to explore how aerosol populations, liquid droplets, and ice crystals interact during the ascent of an air parcel.

---

# Scientific Context

Mixed-phase clouds remain a major source of uncertainty in atmospheric science and climate modelling.

Key unresolved processes include:

- aerosol–cloud interactions  
- biological ice nucleation  
- vapour competition between droplets and ice  
- sensitivity to updraft velocity  

Parcel models provide a controlled framework to isolate these processes while maintaining physically consistent thermodynamics.

This repository implements a **minimal but physically interpretable parcel model** that allows these interactions to emerge naturally.

---

# Physical Framework

The parcel model simulates the ascent of an air parcel with prescribed updraft velocity.

Key physical components include:

---

## Aerosol Activation

Cloud droplet formation follows **Köhler theory**, allowing aerosols to activate when supersaturation exceeds the critical value.

---

## Supersaturation Formulation

Supersaturation is calculated separately for liquid water and ice:
```
 Sw = (e − esat_water) / esat_water
 Si = (e − esat_ice) / esat_ice
```

This separation allows droplets and ice crystals to interact with the vapour field through distinct thermodynamic constraints.

---

## Maxwell-Type Growth

Droplet and ice growth follow Maxwell-type diffusion-limited growth equations:
```
 dr/dt = (G / r) S
```

where **G(T)** represents the combined effects of vapour diffusion and latent heat transport.

---

## Latent Heat Feedback

Condensation and deposition release latent heat, modifying parcel temperature through:
```
dT/dt = − cooling_rate + latent_heating
```

This ensures thermodynamic consistency between microphysics and parcel evolution.

---

## Biological Ice Nucleation

Ice nucleation is represented through a temperature-dependent biological IN parameterisation based on a logistic activation curve.

---

# Bergeron–Findeisen Diagnostic

To quantify the transition from liquid-dominated to ice-dominated vapour depletion, we define a diagnostic ratio:
```
 R = |dep_rate| / |cond_rate|


Interpretation:

| Regime | Condition |
|------|------|
| Liquid dominated | R < 1 |
| Ice dominated | R ≥ 1 |

This provides a quantitative diagnostic for the onset of the **Bergeron–Findeisen process**.

Under baseline aerosol and IN conditions, condensation remains the dominant vapour sink (**R < 1**).

Sensitivity experiments demonstrate that:

- increasing IN number  
- decreasing CCN concentration  
- increasing updraft velocity  

can significantly increase **R**, strengthening vapour competition between droplets and ice.

---

# Example Diagnostics

## Supersaturation evolution

![Supersaturation](figures/maxwell_S_vs_T.png)

---

## Liquid and ice mass evolution

![Mass evolution](figures/maxwell_q_vs_T.png)

---

## Ice-dominance diagnostic

![Dominance ratio](figures/R_vs_time.png)

---

# Repository Structure

All model components are located in the `parcel_model/` directory.

Key files include:

- `aerosol.py` – aerosol population definitions
- `activation.py` – Köhler-based aerosol activation
- `thermodynamics.py` – saturation and supersaturation calculations
- `biological_in.py` – biological ice nucleation scheme

- `run_parcel_competition.py` – liquid-phase vapour competition
- `run_bioIN_onset.py` – ice nucleation onset experiments
- `run_mixed_phase_minimal.py` – minimal mixed-phase parcel model
- `run_mixed_phase_physics.py` – separated liquid/ice vapour physics

- `plot_*.py` – plotting and diagnostic scripts
   plot_R_ratio.py
   plot_mixed_phase_growth.py
   plot_mixed_phase_updraft_sweep.py

Figures used in this README are located in:

---

# Installation

## How to Run the Model

### Requirements

- Python >= 3.9
- Recommended: virtual environment

---

### 0. Create and activate a virtual environment
Create:
```bash
python -m venv venv

```
### Activate on Linux / macOS:
```bash
source venv/bin/activate

```
### Activate on Windows (PowerShell / CMD):
```bash
venv\Scripts\activate

```
### 1. Install dependencies
```bash
pip install numpy scipy matplotlib pandas

```
### 2.Run simulations

Liquid-only parcel:
```bash
python run_parcel_competition.py

```
Biological ice nucleation onset:
```bash
python run_bioIN_onset.py

```

Minimal mixed-phase parcel (liquid + ice growth):
```bash
python run_mixed_phase_minimal.py

```

Mixed-phase updraft sweep:
```bash
python run_mixed_phase_updraft_sweep.py

```


### 3. Generate figures
```bash

python plot_results_polished.py
python plot_bioIN_onset.py
python plot_mixed_phase_compare.py
python plot_mixed_phase_growth.py
python plot_mixed_phase_updraft_sweep.py


```

### Output Figures
```bash

---

# Running the Model

### Liquid-phase aerosol activation
python run_parcel_competition.py

### Ice nucleation onset experiment
python run_bioIN_onset.py


### Minimal mixed-phase parcel model
python run_mixed_phase_minimal.py


### Physically based mixed-phase parcel model
python run_mixed_phase_maxwell.py


---

# Generating Diagnostics
```
python plot_R_ratio.py
python plot_mixed_phase_growth.py
python plot_mixed_phase_updraft_sweep.py

```

These scripts generate diagnostic figures illustrating:

- supersaturation evolution
- droplet and ice growth
- vapour competition
- sensitivity to updraft velocity

---

# Planned Developments

Future extensions of the model include:

- fully coupled buoyancy–updraft feedback
- pressure evolution along parcel ascent
- multi-bin droplet and ice size distributions
- sensitivity studies across aerosol populations
- comparison with laboratory and field observations

---

# Status

This repository contains a **research prototype** developed for physical process exploration and hypothesis generation.

It is not intended for operational forecasting or climate prediction applications.

---

# Citation

If you use this code in research, please cite the repository once the Zenodo DOI is activated.

```

























