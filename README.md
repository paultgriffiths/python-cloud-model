# Python Cloud Parcel Model

## Project Overview
This repository contains a physically based Python parcel model developed to study
cloud droplet activation and condensational growth in mixed aerosol populations.

The model is designed as a **research-oriented framework**, with a strong emphasis on
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
- `make_table.py`: sensitivity analysis tables.
---
## How to Run the Model

This project is written in Python (>=3.9).
It is recommended to use a virtual environment.

### 1. Install dependencies
```bash
pip install numpy scipy matplotlib

