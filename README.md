[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
![Research Code](https://img.shields.io/badge/code-research-blueviolet.svg)
![Citation](https://img.shields.io/badge/citation-available-brightgreen.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-research--prototype-orange.svg)

# Python Cloud Parcel Model

A research-oriented Python parcel model to study cloud microphysics, with a focus on aerosol activation, vapour competition, and mixed-phase (liquid–ice) cloud processes.

---

## Project Overview

This repository contains a physically based cloud parcel model designed to explore how aerosols, cloud droplets, and ice particles interact during the ascent of an air parcel.

The model emphasises:
- Physical transparency
- Simple but meaningful parameterisations
- Time-evolution diagnostics that help explain cloud processes step by step

---

## Scientific Motivation

Aerosol–cloud interactions and mixed-phase cloud processes remain major sources of uncertainty in climate science. Parcel models provide a controlled framework to isolate key microphysical mechanisms while retaining realistic thermodynamics.

This project investigates:
- Köhler-based aerosol activation
- Vapour competition between aerosol populations
- Sensitivity to updraft velocity
- Biological ice nucleation (e.g. pollen-like INPs)
- Vapour transfer between liquid droplets and ice crystals

---

## Mixed-Phase Physics (Liquid + Ice)

A mixed-phase extension has been implemented that explicitly separates vapour exchange with liquid droplets and ice crystals.

Key features include:
- Supersaturation with respect to liquid water (Sw)
- Supersaturation with respect to ice (Si)
- Separate vapour sink/source terms for liquid and ice
- Temperature-dependent biological ice nucleation
- Diagnostic tracking of:
  - Cloud liquid water (qcloud)
  - Ice mass proxy (qice)
  - Cloud droplet number (Ncloud)
  - Ice crystal number (Nice)

This framework allows the transition from liquid-dominated growth to ice-dominated vapour depletion to emerge naturally.

---

## Key Results

### Liquid-Only Regime
- Supersaturation increases with updraft velocity
- Cloud droplets activate and grow via condensation
- Vapour competition occurs primarily between droplets

### Mixed-Phase Regime
- Ice nucleation occurs at a nearly fixed temperature
- Ice growth rapidly becomes the dominant vapour sink
- Liquid water growth stalls after ice onset
- Vapour is preferentially transferred to ice crystals, consistent with the Bergeron–Findeisen mechanism

## Sensitivity of Ice Growth to IN Number

A sensitivity analysis was performed to investigate the impact of ice-nucleating particle (IN) number on mixed-phase ice growth.

The results show that increasing the IN number leads to:

- Earlier onset of ice growth due to enhanced ice nucleation
- Faster ice mass growth rates once ice is activated
- Stronger vapour depletion by ice crystals, consistent with the Bergeron–Findeisen mechanism
- A reduced role of liquid water growth at high IN concentrations

These findings highlight the strong control exerted by IN number on mixed-phase cloud evolution and vapour partitioning.

**Figure:** Sensitivity of ice mass proxy (qice) to varying IN number (Nice = 5, 50, 500).

---

## Repository Structure

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

---


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

Outputs

The model generates:

Time series of temperature, supersaturation, and vapour tendencies

Evolution of qcloud, qice, Ncloud, and Nice

Figures illustrating:

Temperature vs time

Supersaturation vs time

Liquid and ice growth

Number concentration evolution

### Next Steps

Planned developments include:

Physically based Maxwell-type growth equations

Latent heat feedback on temperature and buoyancy

Sensitivity studies with respect to IN efficiency and number

Comparison with published mixed-phase cloud studies

```

### Status
```bash

This code is a research prototype intended for process understanding and hypothesis generation rather than operational forecasting.

```
