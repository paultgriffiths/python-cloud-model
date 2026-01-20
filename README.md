# Python Cloud Parcel Model

## Project Overview
This repository contains a physically based Python parcel model developed to study
cloud droplet activation and condensational growth in mixed aerosol populations.

The model is designed as a research-oriented framework, with a strong emphasis on
physical interpretability, numerical stability, and transparent implementation.

## Scientific Motivation
Aerosol–cloud interactions remain a major source of uncertainty in climate modelling.
Parcel models offer a controlled environment to isolate key microphysical processes
while retaining detailed thermodynamic descriptions.

This project focuses in particular on:
- Köhler-based aerosol activation
- Vapour competition between aerosol modes
- Sensitivity to aerosol size and hygroscopicity
- The role of large biological particles (e.g. pollen)

## Repository Structure
The core model implementation is located in the `parcel_model/` directory.

Key components include:
- `activation.py`: aerosol activation and Köhler-based calculations
- `aerosol.py`: aerosol population definitions
- `constants.py`: physical and thermodynamic constants
- `kohler.py`: Köhler theory implementation
- `run_parcel_simple.py`: basic parcel model simulation
- `run_parcel_competition.py`: vapour competition experiments
- `plot_results.py`: visualisation of model outputs
- `make_table.py`: sensitivity analysis tables

---

## Results and Key Findings

### 1. Supersaturation sensitivity to updraft velocity
A series of parcel simulations were performed to examine the sensitivity of peak
supersaturation to changes in updraft velocity (cooling rate).

Across the tested range (w = 0.2–2.0 m s⁻¹), the model remains numerically stable and
exhibits a monotonic increase in peak supersaturation with increasing updraft velocity.
This behaviour is physically expected, as stronger updrafts generate supersaturation
more rapidly through enhanced cooling.

These results confirm that the model captures the fundamental dynamical control on
liquid-phase cloud droplet activation.

### 2. Minimal biological ice-nucleation parameterisation
A minimal biological ice-nucleation (IN) class was introduced to represent the
temperature-dependent activation of biological particles (e.g. pollen-like IN).

Ice activity is parameterised using a logistic dependence on temperature, characterised
by a midpoint temperature (T₅₀) and activation width. Diagnostic tests show that the
fraction of ice-active particles increases rapidly with decreasing temperature,
consistent with established laboratory and field observations of biological IN.

### 3. Ice onset in a cooling parcel
The biological IN class was coupled to the cooling parcel framework to diagnose the
onset of ice nucleation under different updraft velocities.

For a fixed biological IN population, the onset temperature of ice nucleation remains
nearly invariant across updraft velocities, indicating that ice initiation is primarily
thermodynamically controlled. In contrast, the onset time decreases systematically with
increasing updraft velocity, as stronger updrafts reach the critical temperature more
rapidly.

### 4. Comparison of liquid- and ice-phase sensitivities
Taken together, these experiments highlight contrasting roles of updraft velocity in
cloud microphysical processes:

- Updraft velocity strongly controls the magnitude of peak supersaturation and therefore
  liquid droplet activation.
- Biological ice nucleation is comparatively insensitive to updraft velocity in
  temperature space, but sensitive in time, with faster updrafts leading to earlier ice
  onset.

This comparison demonstrates how the same dynamical forcing can exert distinct controls
on liquid- and ice-phase cloud formation.

---

## How to Run the Model

This project is written in Python (>=3.9).
It is recommended to use a virtual environment.

### 1. Install dependencies
```bash
pip install numpy scipy matplotlib

### 1. Install dependencies
```bash
pip install numpy scipy matplotlib

### 2. Run parcel simulations

python run_parcel_competition.py

### 3. Run biological ice-nucleation experiments

python run_bioIN_onset.py

### 4. Generate figures

python plot_results_polished.py

python plot_bioIN_onset.py

```
