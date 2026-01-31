[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
![Research Code](https://img.shields.io/badge/code-research-blueviolet.svg)
![Citation](https://img.shields.io/badge/citation-available-brightgreen.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-research--prototype-orange.svg)

# Python Cloud Parcel Model

## Project Overview

This repository contains a physically based Python parcel model developed to study cloud droplet activation, condensational growth, and mixed-phase cloud processes in idealised rising air parcels.

The model is designed as a **research-oriented framework**, with emphasis on:
- physical interpretability  
- numerical stability  
- transparent and modular implementation  

---

## Scientific Motivation

Aerosol–cloud interactions remain a major source of uncertainty in climate modelling. Parcel models provide a controlled framework to isolate key microphysical processes while retaining detailed thermodynamic descriptions.

This project focuses on:

- Köhler-based aerosol activation  
- Vapour competition between aerosol modes  
- Sensitivity to aerosol size and hygroscopicity  
- The role of large biological particles (e.g. pollen)  
- A minimal mixed-phase (liquid + ice) cloud prototype  

---

## Model Description

The model simulates an ascending air parcel subject to prescribed cooling (updraft velocity). As the parcel cools:

1. Supersaturation develops  
2. Liquid droplets activate on aerosol particles  
3. Biological ice nucleation may occur once temperatures are sufficiently low  
4. Ice particles grow by vapour deposition, depleting supersaturation  

This simple framework allows direct comparison between liquid-only and mixed-phase cloud evolution.

---

## Repository Structure

The core implementation is located in the `parcel_model/` directory.

Key files include:

- `activation.py` – aerosol activation (κ-Köhler theory)  
- `aerosol.py` – aerosol population definitions  
- `constants.py` – physical and thermodynamic constants  
- `kohler.py` – Köhler theory implementation  
- `run_parcel_simple.py` – basic liquid-only parcel simulation  
- `run_parcel_competition.py` – vapour competition experiments  
- `run_bioIN_onset.py` – biological ice-nucleation onset diagnostics  
- `run_mixed_phase_minimal.py` – minimal mixed-phase (liquid + ice growth) model  
- `run_mixed_phase_updraft_sweep.py` – updraft sensitivity experiments  
- `plot_*.py` – plotting and visualisation scripts  

---

## Results Summary

### 1. Supersaturation Sensitivity to Updraft Velocity

Peak supersaturation increases monotonically with updraft velocity (cooling rate) over the range  
**w = 0.2–2.0 m s⁻¹**.

This confirms the expected dynamical control of updraft velocity on liquid droplet activation.

---

### 2. Biological Ice Nucleation

A minimal biological ice-nucleation parameterisation is implemented using a logistic temperature dependence defined by a midpoint temperature (T₅₀) and activation width.

The fraction of ice-active particles increases rapidly with decreasing temperature, consistent with laboratory and field observations of biological ice nucleation.

---

### 3. Ice Onset in a Cooling Parcel

Coupling biological ice nucleation to the parcel model shows that:

- Ice onset temperature is nearly invariant with respect to updraft velocity  
- Ice onset time decreases systematically with increasing updraft velocity  

This indicates that ice initiation is primarily **thermodynamically controlled**, while parcel dynamics determine the **timing** of ice formation.

---

### 4. Mixed-Phase Effects and Ice Growth

A minimal ice growth (vapour deposition) term is included after ice onset. Ice growth is tracked using an ice mass proxy (`qi`).

Key behaviours observed:

- Supersaturation is rapidly depleted once ice growth begins  
- Ice mass (`qi`) increases monotonically with time  
- Mixed-phase parcels reach lower peak supersaturation than liquid-only parcels  

These results highlight the strong vapour sink associated with ice growth in mixed-phase clouds.

---

### 5. Mixed-Phase Updraft Sweep

Updraft sensitivity experiments comparing liquid-only and mixed-phase cases show that:

- Peak supersaturation increases with updraft velocity in both cases  
- Ice formation reduces peak supersaturation relative to the liquid-only case  
- Ice onset temperature remains fixed, while onset time decreases with increasing updraft  

---

## How to Run the Model

python run_mixed_phase_minimal.py
python run_mixed_phase_updraft_sweep.py
python plot_mixed_phase_compare.py
python plot_mixed_phase_growth.py
python plot_mixed_phase_updraft_sweep.py


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
python plot_mixed_phase_growth.py
python plot_mixed_phase_updraft_sweep.py


```

### 6. Output Figures
```bash
Running the plotting scripts generates the following figures:

- peak_supersaturation_vs_pollen.png – Peak supersaturation as a function of pollen concentration

- updraft_sensitivity_Speak_vs_w.png – Peak supersaturation versus updraft velocity

- bioIN_onset_vs_updraft.png – Ice nucleation onset time versus updraft velocity

- mixed_phase_S_vs_time.png – Supersaturation evolution with and without biological ice nucleation

```
In the most recent update, the model was extended with a minimal mixed-phase framework including ice growth.

New additions include:

- A mixed-phase parcel prototype combining liquid droplets and biological ice nucleation

- A simple ice growth (vapour deposition) term, tracked using an ice mass proxy (qi)

- Updraft sensitivity experiments comparing cases with and without ice

- New scripts to sweep updraft velocity and diagnose ice onset timing

New figures showing:

- Supersaturation evolution with and without ice

- Ice growth (qi) as a function of time

- Peak supersaturation versus updraft velocity in mixed-phase conditions

These updates demonstrate how ice formation rapidly depletes supersaturation and how ice onset is thermodynamically controlled, while its timing depends on updraft speed