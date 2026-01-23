# Python Cloud Parcel Model

## Project Overview
This repository contains a physically based Python parcel model developed to study
cloud droplet activation and condensational growth in mixed aerosol populations.

The model is designed as a **research-oriented framework**, with a strong emphasis on
physical interpretability, numerical stability, and transparent implementation.

---

## Scientific Motivation
Aerosol–cloud interactions remain a major source of uncertainty in climate modelling.
Parcel models offer a controlled environment to isolate key microphysical processes
while retaining detailed thermodynamic descriptions.

This project focuses in particular on:
- Köhler-based aerosol activation
- Vapour competition between aerosol modes
- Sensitivity to aerosol size and hygroscopicity
- The role of large biological particles (e.g. pollen)

---

## Repository Structure
The core model implementation is located in the `parcel_model/` directory.

Key components include:
- `activation.py` – aerosol activation and Köhler-based calculations
- `aerosol.py` – aerosol population definitions
- `constants.py` – physical and thermodynamic constants
- `kohler.py` – Köhler theory implementation
- `run_parcel_simple.py` – basic parcel model simulation
- `run_parcel_competition.py` – vapour competition experiments
- `run_bioIN_onset.py` – biological ice-nucleation onset experiments
- `run_mixed_phase_minimal.py` – minimal mixed-phase (liquid + ice) prototype
- `plot_results.py` – visualisation of model outputs
- `make_table.py` – sensitivity analysis tables

---

## Results and Key Findings

### 1. Supersaturation sensitivity to updraft velocity
Parcel simulations show that peak supersaturation increases monotonically with
updraft velocity (cooling rate) over the range **w = 0.2–2.0 m s⁻¹**.

The model remains numerically stable and reproduces the physically expected
dynamical control of updraft velocity on liquid droplet activation.

### 2. Minimal biological ice-nucleation parameterisation
A minimal biological ice-nucleation (IN) class was implemented using a logistic
temperature dependence defined by a midpoint temperature (T₅₀) and activation width.

Diagnostic tests show a rapid increase in the fraction of ice-active particles with
decreasing temperature, consistent with laboratory and field observations of
biological IN.

### 3. Ice onset in a cooling parcel
Coupling the biological IN scheme to the parcel model shows that:
- Ice onset temperature is nearly invariant with respect to updraft velocity
- Ice onset time decreases systematically with increasing updraft velocity

This indicates that ice initiation is primarily thermodynamically controlled, while
dynamics determine the timing of ice formation.

### 4. Comparison of liquid- and ice-phase sensitivities
These experiments highlight contrasting roles of updraft velocity:
- **Liquid phase:** updraft velocity strongly controls peak supersaturation and CCN activation
- **Ice phase:** biological ice nucleation is comparatively insensitive to updraft velocity in temperature space,
  but sensitive in time, with faster updrafts leading to earlier ice onset

This demonstrates how the same dynamical forcing can exert distinct controls on
liquid- and ice-phase cloud formation.

---

## How to Run the Model
This project is written in **Python (>=3.9)**.
It is recommended to use a virtual environment.

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
pip install numpy scipy matplotlib

```
### 2. Run parcel simulations (liquid phase)
```bash
python run_parcel_competition.py

```
### 3. Run biological ice-nucleation experiments
```bash
python run_bioIN_onset.py

```

### 4. Run minimal mixed-phase prototype (liquid + biological ice)
```bash
python run_mixed_phase_minimal.py

```
### 5. Generate figures
```bash
python plot_results_polished.py
python plot_bioIN_onset.py
python plot_mixed_phase_compare.py


```
### Output Figures
Running the plotting scripts generates the following figures:
- `peak_supersaturation_vs_pollen.png` – Peak supersaturation as a function of pollen concentration
- `updraft_sensitivity_Speak_vs_w.png` – Peak supersaturation versus updraft velocity
- `bioIN_onset_vs_updraft.png` – Ice nucleation onset time versus updraft velocity
- `mixed_phase_S_vs_time.png` – Supersaturation evolution with and without biological ice nucleation


```




