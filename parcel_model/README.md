\# Parcel Model for Mixed Aerosol Activation



This repository contains a simplified parcel model implemented in Python to investigate

cloud droplet activation and vapour competition between mixed aerosol populations,

with a particular focus on large biological particles (e.g. pollen).



The work is inspired by Borlace et al., but developed independently with an emphasis on

physical interpretation and numerical stability.



---



\## Model Overview



The model simulates an ascending air parcel that cools at a prescribed rate.

Supersaturation is generated through cooling and reduced through condensation onto

activated aerosol particles.



Two aerosol populations are represented:

\- Sulfate aerosol (small, hygroscopic, high number concentration)

\- Pollen (large, weakly hygroscopic, low number concentration)



Activation is treated using a κ-Köhler framework.



---



\## Code Structure



\- `constants.py`  

&nbsp; Physical constants used throughout the model.



\- `thermodynamics.py`  

&nbsp; Saturation vapour pressure and supersaturation calculations.



\- `aerosol.py`  

&nbsp; Definition of aerosol population objects.



\- `activation.py`  

&nbsp; Activation check based on κ-Köhler theory.



\- `run\_parcel\_simple.py`  

&nbsp; Basic parcel model without explicit competition tuning.



\- `run\_parcel\_competition.py`  

&nbsp; Parcel model including a simplified condensation sink to represent vapour competition.



\- `plot\_results.py` / `plot\_results\_polished.py`  

&nbsp; Scripts to generate figures of peak supersaturation versus pollen concentration.



---



\## How to Run



1\. Ensure Python 3 is installed.

2\. Clone the repository.

3\. Run the main parcel model:

&nbsp;  ```bash

&nbsp;  python run\_parcel\_competition.py



