![Research Code](https://img.shields.io/badge/code-research-blueviolet.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-research--prototype-orange.svg)

# 🌥️ Python Cloud Parcel Model

## Overview

This project explores warm cloud parcel microphysics using the KiD-A cloud parcel model.

The simulations investigate the temporal evolution of cloud water and rain water during warm cloud development.

The model was compiled and executed on Ubuntu WSL using Fortran and NetCDF libraries.

<p align="center">
  <img src="cloud_parcel_animation.gif" width="700">
</p>

## Technologies

- Python
- Fortran
- NetCDF4
- Matplotlib
- Ubuntu WSL
- Git/GitHub

## Future Work

- Mixed-phase cloud simulations
- Comparison with laboratory observations
- Sensitivity analysis of microphysics schemes
- Automated visualization workflows

  
⚠️ Research-grade prototype for physical insight, not operational forecasting.


## 🚀 What this project does
This model simulates the ascent of an air parcel and shows how:

- **cloud droplets form (Köhler activation)**
- **ice crystals nucleate (biological IN)**
- **vapour is shared between liquid and ice**
- **mixed-phase clouds emerge naturally**

---

## 🧠 Key Insight

Ice does not dominate automatically.

👉 Ice-dominated behaviour **(R ≥ 1)** only appears when:
- ice nucleation is strong enough
- vapour competition becomes significant
  
This provides a physical explanation of the Bergeron–Findeisen process.

---

## 📖 Scientific Context

Mixed-phase clouds remain a major source of uncertainty in atmospheric science and climate modelling.
Key unresolved processes include:

- aerosol–cloud interactions  
- biological ice nucleation  
- vapour competition between droplets and ice  
- sensitivity to updraft velocity  

Parcel models provide a controlled framework to isolate these processes while maintaining physically consistent thermodynamics.
This repository implements a **minimal but physically interpretable parcel model** that allows these interactions to emerge naturally.

---

## ⚙️ Physical Framework

These processes are represented mathematically in the governing equations below.
The parcel model simulates the ascent of an air parcel with prescribed updraft velocity.
Key physical components include:

- **Aerosol Activation**
Cloud droplet formation follows **Köhler theory**, allowing aerosols to activate when supersaturation exceeds the critical value.

- **Biological Ice Nucleation**
Ice nucleation is represented through a temperature-dependent biological IN parameterisation based on a logistic activation curve.

---

## ⚙️ Governing Equations

The parcel model is based on a physically consistent representation of vapour, liquid, and ice interactions in a rising air parcel.

- **Supersaturation**

Supersaturation is defined separately with respect to liquid water and ice:
```
Sw = (e − esat_water) / esat_water  
Si = (e − esat_ice) / esat_ice
```

This separation allows liquid droplets and ice crystals to interact with the vapour field under distinct thermodynamic constraints.

- **Vapour Budget**

The total vapour tendency is decomposed into contributions from liquid condensation and ice deposition:
```
dqv/dt = (dqv/dt)_liq + (dqv/dt)_ice
``` 

where:

(dqv/dt)_liq = − cond_rate  
(dqv/dt)_ice = − dep_rate  

This formulation enables explicit competition between liquid droplets and ice particles for available water vapour.

- **Temperature Evolution**

Temperature evolves due to adiabatic cooling and latent heat release:
```
dT/dt = − cooling_rate + (Lv / cp) · (dql/dt) + (Ls / cp) · (dqi/dt)
```
This coupling ensures thermodynamic consistency between microphysical growth and parcel evolution.

- **Ice-Dominance Diagnostic**

To quantify vapour competition, a diagnostic ratio is defined:
```
R = |dep_rate| / |cond_rate|
```
R < 1 → liquid-dominated regime  
R ≥ 1 → ice-dominated regime  

This diagnostic provides a quantitative measure of the transition to ice-dominated vapour depletion, consistent with the Bergeron–Findeisen process.

- **Maxwell-Type Growth**

Droplet and ice growth follow Maxwell-type diffusion-limited growth equations:
```
 dr/dt = (G / r) S
```

where **G(T)** represents the combined effects of vapour diffusion and latent heat transport.

- **Latent Heat Feedback**

Condensation and deposition release latent heat, modifying parcel temperature through:
```
dT/dt = − cooling_rate + latent_heating
```

This ensures thermodynamic consistency between microphysics and parcel evolution.

---

## 📊 Core Diagnostic

The key quantity is:
```
 R = |dep_rate| / |cond_rate|
```
Interpretation:

| Regime | Meaning |
|--------|-----------|
| R < 1 | Liquid dominates |
| R ≥ 1| Ice dominates |

This provides a quantitative diagnostic for the onset of the **Bergeron–Findeisen process**.
Under baseline aerosol and IN conditions, condensation remains the dominant vapour sink (**R < 1**).
Sensitivity experiments demonstrate that:

- increasing IN number  
- decreasing CCN concentration  
- increasing updraft velocity  

can significantly increase **R**, strengthening vapour competition between droplets and ice.

---

## Model Diagnostics

These diagnostics illustrate vapour competition between liquid droplets and ice crystals in the parcel.

The transition toward an ice-dominated regime is captured by the diagnostic ratio \(R = |dep\_rate| / |cond\_rate|\).

---

### Supersaturation evolution

![Supersaturation](figures/maxwell_S_vs_T.png)

Supersaturation over water (Sw) stabilises after droplet activation, while supersaturation over ice (Si) continues to increase as temperature decreases.

---

### Thermodynamic driver (Si − Sw)

![Si minus Sw](figures/Si_minus_Sw_vs_T.png)

As temperature decreases, Si exceeds Sw, creating a thermodynamic preference for vapour deposition onto ice.

---

### Liquid and ice mass evolution

![Mass evolution](figures/maxwell_q_vs_T.png)

Liquid water increases rapidly after activation, while ice grows more gradually through vapour deposition.

---

### Vapour competition (R vs time)

![R ratio](figures/R_vs_time.png)

The ratio \(R\) shows the transition from liquid-dominated (\(R < 1\)) to ice-dominated (\(R \geq 1\)) behaviour.

---

### Sensitivity of the ice-dominated transition

![Rmax heatmap](figures/Rmax_heatmap_CCN_IN.png)

The maximum value of \(R\) depends on CCN and IN concentrations. Ice-dominated behaviour occurs only when IN concentration is sufficiently high.

---

### Sensitivity of the ice-dominated regime

![Rmax heatmap](figures/Rmax_heatmap_CCN_IN_boundary.png)

The transition boundary (\(R = 1\)) separates liquid-dominated and ice-dominated regimes across the CCN–IN parameter space.

---

# 🎬 Model Validation Results

## Case 1 — Warm-Rain Benchmark (KiD-inspired)

To evaluate the physical consistency of the parcel model, a warm-rain benchmark inspired by KiD Case 1 has been implemented.

This configuration includes:

- prescribed sinusoidal updraught forcing  
- fixed temperature  
- Köhler-based aerosol activation  
- supersaturation over water from thermodynamic calculations  
- Maxwell-type droplet growth  
- warm-rain autoconversion and accretion  

### Results

![Cloud water mass](figures/kid_case1_cloud_mass.png)  
*Cloud water mass evolution.*

![Rain water mass](figures/kid_case1_rain_mass.png)  
*Rain water mass evolution.*

![Surface rain rate](figures/kid_case1_surface_rain_rate.png)  
*Surface rain-rate evolution.*

![Liquid water path](figures/kid_case1_lwp.png)  
*Liquid water path evolution.*

The model reproduces the expected qualitative behaviour of a warm-rain cloud system:

- rapid cloud water growth during ascent  
- peak cloud water followed by decay  
- delayed rain formation  
- gradual increase in surface rain rate
  

### Validation Metrics

| Metric | Value |
|--------|------|
| Max cloud mass | 1.35 × 10⁻³ |
| Time of max cloud | 296 s |
| Max rain mass | 1.40 × 10⁻³ |
| Rain onset time | 42 s |
| Max rain rate | 6.99 × 10⁻³ |
| Final cloud mass | ~0 |
| Final rain mass | 1.40 × 10⁻³ |

### Interpretation

The model captures the essential warm-rain evolution:

- rapid cloud development followed by depletion  
- conversion of cloud water into rain  
- rain dominance at late times  

These results are consistent with KiD intercomparison behaviour.

---

### Qualitative comparison with KiD-inspired benchmark

| Diagnostic | Present model | Expected qualitative KiD behaviour |
|---|---:|---|
| Cloud water evolution | rises then decays | rises during ascent then decays |
| Rain formation | ~42 s in this configuration | delayed rain formation |
| Peak cloud mass | 1.35 × 10⁻³ kg/kg | comparable warm-rain peak behaviour |
| Final cloud mass | ~0 | cloud water depleted by rain conversion |
| Surface rain rate | increases gradually | rain rate increases after rain onset |

The comparison confirms that the model captures the expected sequence of warm-rain processes observed in KiD intercomparison studies. While the agreement is primarily qualitative, the results provide confidence that the model reproduces the key physical behaviour of cloud water growth, delayed rain formation, and subsequent rain development.

A fully quantitative comparison would require using the exact KiD reference setup and comparing against published KiD model outputs.

---

## ❄️ Case 2 — Mixed-Phase Cloud (Maxwell Growth)

A mixed-phase parcel experiment was performed using the Maxwell-growth framework, including:

- coupled vapour evolution  
- latent heating  
- biological ice nucleation  

This setup represents a system where liquid droplets and ice crystals compete for water vapour.

### Results

![Liquid and ice mass](figures/case2_from_maxwell_liquid_ice.png)  
*Evolution of liquid water and ice mass.*

![Supersaturation](figures/case2_from_maxwell_S.png)  
*Supersaturation over water (Sw) and ice (Si).*

![Vapour sinks](figures/case2_from_maxwell_sinks.png)  
*Condensation vs deposition sinks.*

![BF ratio](figures/case2_from_maxwell_R.png)  
*Bergeron–Findeisen ratio.*

---

### Physical Interpretation

The simulation shows coexistence of liquid and ice:

- supersaturation over ice (Si) > supersaturation over water (Sw)  
- liquid grows rapidly after activation  
- ice increases steadily via deposition  
- condensation and deposition occur simultaneously  

Ice growth is favoured because saturation vapour pressure over ice is lower than over liquid water.

---

### Bergeron–Findeisen Transition

The model captures a transition from:

- liquid-dominated regime (R < 1)  
- to ice-dominated regime (R ≥ 1)  

This transition emerges naturally without parameter tuning.

- transition time ≈ 1800 s  
- final ratio R ≈ 11.57  

As temperature decreases:

- saturation over ice becomes lower  
- vapour deposits onto ice  
- droplet growth reduces Sw  

---

### Validation Metrics

| Metric | Value |
|--------|-------|
| Max liquid mass (qcloud) | 1.95 × 10⁻³ |
| Max ice mass (qice) | 1.18 × 10⁻³ |
| Ice onset time | 0 s |
| Max Sw | 1.14 × 10⁻² |
| Max Si | 3.83 × 10⁻¹ |
| Max condensation sink | 1.72 × 10⁻⁶ |
| Max deposition sink | 4.29 × 10⁻⁷ |
| Final R | 11.57 |

---

### Note

An initial spike in the ratio R may occur due to very small condensation rates.  
This is a numerical artefact and does not affect interpretation.

---

### Key Insights

- mixed-phase behaviour emerges naturally from thermodynamics  
- vapour competition depends on Si vs Sw  
- ice growth can occur even when condensation dominates  

---

## 📌 Comparison between Case 1 and Case 2


| Feature | Case 1: Warm-rain benchmark | Case 2: Mixed-phase Maxwell case |
|---|---|---|
| Main process | Liquid cloud growth and rain formation | Competition between liquid droplets and ice crystals |
| Phase included | Liquid only | Liquid + ice |
| Key behaviour | Cloud water increases, then decreases as rain forms | Liquid and ice coexist, then ice growth becomes increasingly important |
| Vapour sink | Condensation dominates | Condensation initially dominates, then deposition becomes stronger |
| Main diagnostic | Cloud mass, rain mass, rain rate | Supersaturation, vapour sinks, Bergeron–Findeisen ratio |
| Scientific meaning | Reproduces warm-rain qualitative behaviour | Captures mixed-phase transition and vapour competition |

This comparison shows that the model can reproduce two distinct cloud regimes. Case 1 captures the expected warm-rain evolution, while Case 2 extends the framework to mixed-phase conditions where liquid droplets and ice crystals compete for water vapour. The transition from condensation-dominated to deposition-dominated behaviour demonstrates that the model can represent the emergence of Bergeron–Findeisen-type behaviour without additional tuning.

---

## Comparison with KiD-inspired setup

| Component | Formal KiD / KiD-inspired setup | Current model | Next action |
|---|---|---|---|
| Model type | 1D kinematic cloud model used for microphysics intercomparison | 0D parcel model | State clearly that this is a simplified parcel analogue |
| Updraft forcing | Prescribed kinematic forcing, often sinusoidal or time-dependent | Prescribed parcel updraft / cooling rate | Add a KiD-inspired time-dependent updraft option |
| Warm-rain focus | Cloud water, rain water, rain rate, LWP | Warm-rain benchmark already included | Compare the same diagnostics |
| Aerosol / droplet number | Fixed or prescribed aerosol/droplet number, e.g. warm-rain intercomparison cases | CCN activation and prescribed CCN sensitivity | Document CCN values clearly |
| Microphysics | Warm-rain microphysics schemes compared under same forcing | Köhler activation, Maxwell growth, warm-rain process, mixed-phase extension | Separate warm-rain validation from mixed-phase extension |
| Outputs | Cloud water, rain water, precipitation/rain rate, LWP | qcloud, qrain, rain rate, LWP, qice, R | Use common output names and figures |

---


## 🔬 Final Scientific Conclusion

- Warm-rain behaviour is correctly reproduced
- Mixed-phase coexistence emerges naturally
- Vapour competition is governed by Si vs Sw
- Ice growth is thermodynamically favoured
- No explicit parameter tuning is required for BF transition

This model provides a consistent bridge between:

warm-rain → mixed-phase → ice-dominated regimes
---

## Numerical Stability Analysis

### Stability Test Summary
The model was tested across:

- Updraft velocities: 1, 5, 10 m/s  
- Timesteps: 0.1, 0.5, 1.0 s  
- Initial ice radii: 1e-6, 5e-7, 1e-7 m  

A total of 27 combinations were evaluated.
All cases remained numerically stable. No NaN values, infinite values, negative radii, or supersaturation blow-up were observed.

---

### Representative Cases

| w (m/s) | dt (s) | r_init (m) | Status | Notes                  |
|--------|--------|-----------|--------|------------------------|
| 1      | 1.0    | 1e-6      | Stable | No onset               |
| 5      | 0.5    | 5e-7      | Stable | Normal growth          |
| 10     | 0.1    | 1e-7      | Stable | Extreme but stable     |

---

### Detailed Analysis

To further investigate the effect of timestep size, additional simulations were performed using larger timestep values (dt = 2, 5, and 10 s).
All simulations remained numerically stable, with no evidence of divergence, oscillations, or instability.

---

### Stability Behaviour

- No oscillations or numerical blow-up were detected.  
- Ice growth remained physically consistent across all simulations.  
- The onset of ice formation occurred at similar times for different timestep values.  

---

### Accuracy Considerations

While the model remains stable for large timesteps, small differences in the final ice radius were observed:

- Smaller timesteps (dt ≤ 0.1) produce nearly identical results.  
- Larger timesteps (dt ≥ 1.0) introduce slight deviations.  

This indicates that:

- The model is numerically stable across a wide range of dt.  
- The solution is converging as dt → 0.  
- Larger timesteps slightly reduce accuracy but do not affect overall behaviour.  

---

### Practical Implications

These results suggest that:

- The model can be run with relatively large timesteps to reduce computational cost.  
- A timestep of dt ≈ 0.1–1.0 s provides a good balance between accuracy and efficiency.  

### Sensitivity to Timestep (dt)

  ![Timestep sensitivity](figures/figure_dt_sensitivity.png)
The figure below shows the variation of the final ice radius as a function of timestep size.

This plot confirms that:

- The solution converges as dt decreases.
- The variation in final ice radius remains small.
- The model remains stable across the tested timestep range.
  
### Interpretation

The results show that the final ice radius converges as the timestep decreases.

For timesteps larger than 1 s, the solution becomes nearly constant, indicating numerical stability and low sensitivity to further increases in timestep.

This suggests that using dt ≈ 1 s provides a good compromise between computational efficiency and accuracy.

---

### Breakdown at large timesteps

To further investigate the robustness of the model, larger timestep values were tested (dt = 20, 50, and 100 s).

The simulations failed for these cases:

- dt = 20 s → Overflow error
- dt = 50 s → Division by zero
- dt = 100 s → Division by zero

This indicates that the numerical scheme becomes unstable for sufficiently large timesteps. The failure is likely due to large temperature changes within a single timestep, leading to non-physical values and numerical breakdown.

Therefore, while the model is stable for dt ≤ 10 s, there is a clear upper limit beyond which the results are no longer reliable.

---

### Reproducibility

All results can be reproduced by running:

```bash
python run_stability_test.py

```
The output summary is saved in:

```bash
data/stability_results.csv

```
---
## ⚠️ Limitations

- Zero-dimensional parcel (no spatial variability)
- No turbulence or entrainment
- Simplified ice nucleation parameterisation
- Single-moment microphysics

---

## 📁 Repository Structure

The project is organised to clearly separate model physics, experiments, diagnostics, and outputs.

```text
python-cloud-model/
├── parcel_model/                    # core parcel microphysics modules
│   ├── aerosol.py                   # aerosol population definitions
│   ├── activation.py                # Köhler-based droplet activation
│   ├── thermodynamics.py            # saturation and supersaturation calculations
│   ├── biological_in.py             # biological ice nucleation parameterisation
│   └── run_mixed_phase_maxwell.py   # mixed-phase parcel model driver
│
├── cases/         # configuration files for different cases
│    ├── case1_config.py
│    ├──  kid_forcing.py
│    └──  kid_inspired_forcing.py
│ 
├── experiments/         # experiment scripts
│   ├── run_stability_test.py
│   ├── run_kid_case1.py   # KiD Case 1 warm-rain benchmark experiment
│   ├── run_case2_from_maxwell.py
│   ├── extract_validation_metrics.py
│   └── run_kid_inspired_alignment.py
│
│
├── plotting/            # plotting and diagnostics
│   ├── plot_R_ratio.py
│   ├── plot_mixed_phase_growth.py
│   ├── plot_Si_minus_Sw.py
│   ├── plot_kid_case1.py            # plots for KiD Case 1 benchmark
│   ├── plot_case2_from_maxwell.py   #  plots Case 2 Bergeron-Findeisen transition reproduced
│   └── plot_kid_inspired_alignment.py
│
│
├── data/                # simulation outputs and stability results
│   └── stability_results.csv
│
├── data/                # simulation outputs (CSV files)
├── figures/            # generated figures
│   ├── maxwell_S_vs_T.png
│   ├── maxwell_q_vs_T.png
│   ├── R_vs_time.png
│   ├── Si_minus_Sw_vs_T.png
│   ├── Rmax_heatmap_CCN_IN_boundary.png
│   ├── kid_case1_cloud_mass.png
│   ├── kid_case1_rain_mass.png
│   ├── kid_case1_surface_rain_rate.png
│   ├── kid_case1_lwp.png
│   ├── case2_from_maxwell_liquid_ice.png
│   ├── case2_from_maxwell_S.png
│   ├── case2_from_maxwell_sinks.png
│   ├── case2_from_maxwell_R.png
│   └── kid_warm1_comparison.png
│
│
├── KiD-A/                           # official KiD benchmark model (Fortran)
│
├── README.md
├── requirements.txt
└── .gitignore

```


##  Key Files

---

### Core model (parcel physics)

- **parcel_model/aerosol.py** — aerosol population definitions  

- **parcel_model/activation.py** — Köhler-based aerosol activation  

- **parcel_model/thermodynamics.py** — saturation vapour pressure and supersaturation calculations (Sw, Si)  

- **parcel_model/biological_in.py** — temperature-dependent biological ice nucleation scheme  

- **parcel_model/run_mixed_phase_maxwell.py** — physically based mixed-phase parcel model with Maxwell growth and latent heat feedback
  
---

### Experiments

- **experiments/run_R_sweep.py** — sensitivity of vapour competition across parameter space  

- **experiments/run_R_w_sweep.py** — sensitivity of vapour competition to updraft velocity  

- **experiments/run_mixed_phase_updraft_sweep.py** — mixed-phase evolution under varying dynamical forcing

- **experiments/run_kid_case1.py** — warm-rain benchmark inspired by KiD Case 1
  
---

### Diagnostics and plotting

- **plotting/plot_R_ratio.py** — Bergeron–Findeisen diagnostic \(R = |dep\_rate| / |cond\_rate|\)  

- **plotting/plot_Si_minus_Sw.py** — thermodynamic driver of vapour transfer (Si − Sw)  

- **plotting/plot_mixed_phase_growth.py** — evolution of liquid and ice mass

- **plotting/plot_kid_case1.py** — diagnostic plots for KiD Case 1 benchmark  


---

### Outputs

- **data/** — simulation outputs (CSV time series)  

- **figures/** — generated figures for diagnostics and analysis  

---  

## Workflow

The overall workflow of the model is illustrated below:
  ![Workflow](figures/workflow_diagram.png)
*Figure: Workflow of the parcel model from simulation to diagnostics and visualisation.*

Model → Simulation Output → Diagnostics → Figures

- **Model**: core parcel model computes thermodynamic and microphysical evolution  
- **Simulation Output**: results are saved as time series (CSV files)  
- **Diagnostics**: derived quantities (e.g. R ratio, Si − Sw) are computed  
- **Figures**: visualisations are generated to interpret physical behaviour
  
## 🧭 Scientific Workflow Summary

![Scientific workflow](figures/scientific_workflow_summary.png)

*Figure: Scientific workflow of the mixed-phase parcel model. The simulations connect parcel dynamics, supersaturation evolution, vapour competition, phase partitioning, and the emergence of Bergeron–Findeisen conditions in mixed-phase clouds.*

---

## ✅ Scientific Workflow

The modelling framework follows a physically connected workflow linking parcel dynamics, thermodynamics, and mixed-phase cloud microphysics:

Parcel ascent and dynamical forcing  
→ supersaturation evolution (`Sw`, `Si`)  
→ vapour competition diagnostics (`R_BF`)  
→ liquid and ice phase partitioning  
→ Bergeron–Findeisen transition analysis

This framework enables investigation of how transient parcel dynamics influence vapour competition, phase evolution, and ice dominance in mixed-phase cloud systems.

---

## 🌊 KiD-Inspired Dynamical Forcing

To improve consistency with parcel-model intercomparison frameworks, a time-dependent KiD-inspired updraft forcing has been implemented.

The prescribed vertical velocity follows a sinusoidal evolution:

```math
w(t) = w_{max} \sin\left(\frac{\pi t}{t_{forcing}}\right)
```

where:

- \(w_{max}\) is the maximum updraft velocity
- \(t_{forcing}\) is the forcing duration

This configuration provides a more realistic transient parcel ascent compared with constant updraft forcing.

### Example forcing evolution

![KiD-inspired forcing](figures/kid_inspired_updraft.png)

*Figure: Time-dependent KiD-inspired prescribed updraft forcing used for parcel simulations.*

---

## 🧪 Effect of KiD-Inspired Forcing

A first alignment experiment using a KiD-inspired effective updraft forcing (`w_effective = 2.0 m/s`) was performed.

Compared with constant updraft simulations:

- vapour competition was reduced
- the Bergeron–Findeisen transition weakened
- liquid water remained dominant for a longer period
- ice growth became less aggressive

These results demonstrate that transient dynamical forcing can significantly modify mixed-phase cloud evolution and vapour competition.

This behaviour is physically consistent with the shorter ascent duration associated with transient forcing.

  ![Constant vs KiD forcing](figures/constant_vs_kid_R.png)

*Figure: Comparison of the Bergeron–Findeisen ratio \(R\) under constant updraft forcing and KiD-inspired effective forcing. Under constant forcing, the parcel transitions toward an ice-dominated regime \((R \geq 1)\). In contrast, the transient KiD-inspired forcing suppresses the transition and maintains a liquid-dominated regime.*

### Physical Interpretation

The comparison demonstrates that parcel dynamics strongly influence mixed-phase cloud evolution.

Under constant forcing, continuous ascent sustains supersaturation and strengthens vapour deposition onto ice crystals. As a result, the Bergeron–Findeisen ratio increases rapidly and eventually exceeds the ice-dominance threshold:

```math
R \geq 1

```

In contrast, the transient KiD-inspired forcing limits the duration of sustained ascent. This weakens vapour competition, reduces ice growth efficiency, and delays or suppresses the transition toward an ice-dominated regime.

These results show that the emergence of Bergeron–Findeisen conditions depends not only on thermodynamics and aerosol properties, but also on the temporal structure of dynamical forcing.

![Constant vs KiD liquid and ice](figures/constant_vs_kid_liquid_ice.png)

*Figure: Comparison of liquid water and ice water evolution under constant updraft forcing and KiD-inspired effective forcing. Under transient forcing, liquid water remains dominant for a longer period while ice growth is significantly reduced. This demonstrates that the temporal structure of dynamical forcing strongly influences phase partitioning in mixed-phase clouds.*

![Constant vs KiD supersaturation](figures/constant_vs_kid_supersaturation.png)

*Figure: Comparison of supersaturation evolution under constant updraft forcing and KiD-inspired effective forcing. The simulations show distinct evolution of supersaturation with respect to water (\(Sw\)) and ice (\(Si\)). Although \(Si\) increases substantially under transient forcing, the reduced duration of sustained ascent weakens vapour competition and limits the transition toward an ice-dominated regime.*

![BF transition timing](figures/BF_transition_timing.png)

*Figure: Timing of the Bergeron–Findeisen transition under different forcing configurations. Under constant forcing, the parcel transitions toward an ice-dominated vapour sink after approximately 1782 s. Under transient KiD-inspired forcing, no transition occurs within the simulation period, indicating suppressed vapour competition and reduced ice dominance.*

Overall, these forcing experiments show that the temporal structure of parcel ascent controls supersaturation evolution, vapour competition, phase partitioning, and the timing of the Bergeron–Findeisen transition.

### Comparison of forcing configurations

| Case | Forcing type | BF transition | Ice dominance | Main behaviour |
|---|---|---|---|---|
| Constant forcing | Constant updraft (`w = 1.0 m/s`) | Yes | Strong | Sustained vapour competition and strong ice growth |
| KiD-inspired forcing | Transient prescribed forcing | No | Weak | Reduced vapour competition and delayed ice growth |

---

## 🥇 Literature-Inspired Benchmark Starter Case

A literature-inspired mixed-phase benchmark starter case was performed as an initial step toward model validation and future KiD-style comparisons.

This case uses mixed-phase conditions representative of parcel-model intercomparison studies, including transient ascent, supersaturation evolution, vapour competition, and liquid–ice phase partitioning.

The simulation shows:

- persistent supersaturation with respect to ice (`Si`)
- liquid cloud water remaining dominant during the simulation
- gradual ice growth by deposition
- weak Bergeron–Findeisen vapour competition during short transient ascent
- no strong ice-dominated transition within the simulated period

The benchmark-style experiments demonstrate that the model is capable of reproducing physically consistent mixed-phase cloud behaviour, including supersaturation evolution, vapour competition, delayed ice growth, and persistent liquid water under transient ascent conditions.

These results provide an initial step toward literature-inspired model validation and future KiD-style benchmark comparisons.

![Case 3 supersaturation](figures/case3_literature_benchmark_supersaturation.png)

*Figure: Supersaturation evolution in the literature-inspired benchmark starter case.*

![Case 3 liquid and ice](figures/case3_literature_benchmark_liquid_ice.png)

*Figure: Liquid and ice mass evolution in the benchmark starter case.*

![Case 3 Bergeron–Findeisen ratio](figures/case3_literature_benchmark_R.png)

*Figure: Bergeron–Findeisen vapour competition diagnostic for the benchmark starter case.*

### Comparison with Mixed-Phase Literature Behaviour

The simulated benchmark behaviour is qualitatively consistent with mixed-phase parcel-model studies reported in the literature.

In particular, the simulations reproduce several physically expected behaviours commonly reported in transient mixed-phase cloud studies:

- persistent liquid water during transient ascent
- gradual ice growth by vapour deposition
- delayed Bergeron–Findeisen transition
- weak vapour competition during short forcing periods
- supersaturation with respect to ice remaining larger than supersaturation with respect to liquid water

These trends are physically consistent with previous mixed-phase parcel-model and KiD-style intercomparison studies, where transient dynamical forcing suppresses rapid ice dominance and prolongs liquid persistence.

---

## 🧪 Case 4: KiD Mixed1 Alignment Experiment

This experiment represents an initial direct-alignment test with the KiD mixed-phase benchmark framework.

The setup was configured using parameters inspired by the official KiD `mixed1.nml` case, including:

- `dt = 1 s`
- aerosol concentration ≈ `50 × 10^6 m^-3`
- weak mixed-phase ascent forcing

The simulation reproduces physically consistent mixed-phase behaviour:

- gradual ice growth
- persistent liquid water during early ascent
- rapid liquid depletion during the Bergeron–Findeisen transition
- strong vapour competition at later times

These results demonstrate that the parcel model can reproduce benchmark-aligned mixed-phase cloud evolution and provide a foundation for future direct intercomparison studies with KiD.

### Liquid and Ice Evolution

![Case 4 Liquid and Ice](figures/case4_kid_mixed1_alignment_liquid_ice.png)

### Supersaturation Evolution

![Case 4 Supersaturation](figures/case4_kid_mixed1_alignment_supersaturation.png)

---

### Quantitative Comparison Summary

| Metric | KiD Benchmark | Python Parcel Model |
|---|---|---|
| Cloud-water peak | 1.4334 | 1.1829 |
| Rain-water peak | 0.4519 | 0.8320 |
| Cloud peak time (s) | 570 | 1170 |
| Rain peak time (s) | 930 | 3600 |

The simplified Python parcel model reproduces the general warm-cloud evolution observed in the KiD benchmark, but important quantitative differences remain.

In particular:
- rain formation is delayed in the simplified model
- rain-water production is overestimated
- cloud evolution is temporally smoother than in the KiD simulation

These differences are expected because the Python framework currently uses simplified warm-rain parameterisations compared with the full KiD microphysics scheme.

---

### Error Metrics

| Metric | Value |
|---|---|
| Cloud RMSE | 0.3303 |
| Rain RMSE | 0.5378 |
| Cloud MAE | 0.2844 |
| Rain MAE | 0.4531 |

The quantitative comparison indicates that the simplified Python parcel model captures the general warm-cloud evolution observed in the KiD benchmark, although significant differences remain in rain formation timing and precipitation intensity.

The larger rain-related errors are expected because the simplified framework currently lacks detailed collision–coalescence and sedimentation physics.

---

## Threshold-Based Autoconversion Improvement

A physically motivated threshold-based rain autoconversion scheme was introduced to improve alignment between the simplified Python parcel model and the KiD warm-cloud benchmark.

The updated framework delays rain formation until cloud water exceeds a critical threshold, producing more realistic warm-rain evolution.

### Error Reduction

| Metric | Previous Model | Threshold-Based Model |
|---|---|---|
| Cloud RMSE | 0.3303 | 0.2399 |
| Rain RMSE | 0.5378 | 0.3579 |
| Cloud MAE | 0.2844 | 0.2058 |
| Rain MAE | 0.4531 | 0.3031 |

The introduction of threshold-based autoconversion significantly improves the agreement with the KiD benchmark, particularly for rain-water timing and overall cloud evolution.

![Threshold Autoconversion](figures/case10_threshold_autoconversion.png)

---

## Threshold Sensitivity Study

A sensitivity analysis was performed to investigate how the rain autoconversion threshold influences warm-cloud evolution and agreement with the KiD benchmark.

Three threshold values were tested:

- 0.35
- 0.55
- 0.75

The results demonstrate that the autoconversion threshold strongly controls:

- cloud-water persistence
- timing of rain formation
- post-peak cloud decay
- overall benchmark agreement

Lower thresholds trigger earlier rain conversion and more rapid cloud depletion, while larger thresholds delay rain formation and preserve cloud water for longer periods.

The intermediate threshold (`0.55`) produced the closest qualitative agreement with the KiD warm-cloud benchmark.

![Threshold Sensitivity](figures/case12_threshold_sensitivity.png)

---

## Updraft Sensitivity Study

A sensitivity analysis was performed to investigate how vertical velocity (`w`) influences warm-cloud evolution and benchmark agreement.

Three updraft velocities were tested:

- 1.0 m/s
- 2.0 m/s
- 4.0 m/s

The simulations show that cloud-water growth is strongly controlled by parcel ascent rate.

Stronger updrafts produce:

- faster supersaturation generation
- enhanced cloud-water growth
- larger cloud-water peaks
- delayed cloud depletion

The intermediate forcing (`w = 2.0 m/s`) produced the closest agreement with the KiD warm-cloud benchmark.

![Updraft Sensitivity](figures/case13_updraft_sensitivity.png)

---

## Aerosol Sensitivity Study

A sensitivity analysis was performed to investigate how aerosol loading influences warm-cloud development and benchmark agreement.

Three aerosol scaling factors were tested:

- 0.5
- 1.0
- 2.0

The simulations show that aerosol concentration strongly affects cloud-water evolution.

Larger aerosol loading produces:

- enhanced cloud-water growth
- larger cloud-water peaks
- delayed cloud depletion
- stronger persistence of condensate

The intermediate aerosol factor (`1.0`) produced the closest agreement with the KiD warm-cloud benchmark.

![Aerosol Sensitivity](figures/case14_aerosol_sensitivity.png)

---

## 🔬 Key Scientific Findings

- Ice dominance does not emerge automatically.
- Vapour competition depends strongly on forcing structure.
- Transient KiD-inspired forcing suppresses the Bergeron–Findeisen transition.
- Supersaturation evolution alone does not determine ice dominance.
- Phase partitioning depends on both thermodynamics and parcel dynamics.
- Mixed-phase cloud behaviour emerges naturally from physically based thermodynamics and diffusion-limited growth.


## 📚 References

- Pruppacher, H. R., and Klett, J. D. (1997). *Microphysics of Clouds and Precipitation*. Springer.

- Morrison, H., Curry, J. A., and Khvorostyanov, V. I. (2005). *A New Double-Moment Microphysics Parameterization for Application in Cloud and Climate Models. Part I: Description*. Journal of the Atmospheric Sciences, 62(6), 1665–1677.

- Grabowski, W. W. (2015). *Untangling microphysical impacts on deep convection applying a novel modeling methodology*. Journal of the Atmospheric Sciences, 72(6), 2446–2467.

- Rogers, R. R., and Yau, M. K. (1989). *A Short Course in Cloud Physics*. Pergamon Press.

- Köhler, H. (1936). *The nucleus in and the growth of hygroscopic droplets*. Transactions of the Faraday Society, 32, 1152–1161.

- KiD (Kinematic Driver) intercomparison framework for cloud microphysics studies: https://github.com/Adehill/KiD-A.
  
---


## 📏 Units

All variables in this model use **SI units** to ensure physical consistency.

### Thermodynamic variables
- Temperature: **Kelvin (K)**
- Pressure: **Pascal (Pa)**
- Water vapour mixing ratio: **kg/kg**

### Microphysical variables
- Droplet / ice radius: **meters (m)**
- Liquid water content: **kg/kg**
- Ice water content: **kg/kg**

### Dynamical variables
- Vertical velocity (updraft): **m/s**
- Time: **seconds (s)**

### Aerosol properties
- CCN concentration: **m⁻³**
- IN concentration: **m⁻³**

### Diagnostic quantities
- Supersaturation (Sw, Si): **dimensionless**
- Vapour competition ratio (R): **dimensionless**
        

## ⚙️ Numerical Method

- Time integration: explicit time stepping
- Fixed timestep (dt)
- Coupled evolution of temperature, vapour, liquid, and ice
- Latent heat feedback included
- Numerical stability controlled via timestep selection

---

## ⚙️ Installation

### ⚡ Quick Start

Clone the repository and run a simulation in minutes:

```bash
git clone https://github.com/paultgriffiths/python-cloud-model.git
cd python-cloud-model

```

### Requirements

- Python >= 3.9
- Recommended: virtual environment

---

### 1. Create and activate a virtual environment
Create the environment:
```bash
python -m venv venv

```
Activate on Linux / macOS:
```bash
source venv/bin/activate

```
Activate on Windows (PowerShell / CMD):
```bash
venv\Scripts\activate

```
### 2. Install dependencies
```bash
pip install -r requirements.txt

```
If needed, you can also install manually:
```bash
pip install numpy scipy matplotlib pandas

```

### 3. Run simulations

Run the main validated experiments:

#### Warm-rain benchmark (KiD-inspired)
```bash
python experiments/run_kid_case1.py

```

#### Mixed-phase cloud (Maxwell growth)
```bash
python experiments/run_case2_from_maxwell.py

```
---

## 🔬 KiD-A Warm Cloud Benchmark (Fortran)

The official KiD-A warm cloud benchmark was compiled and executed under Ubuntu WSL using Fortran and NetCDF libraries.

### Compile the KiD-A model

```bash
make COMPILER=gfortran CASE=1D all

```

### Run the warm cloud benchmark

```bash
./bin/KiD_1D.exe namelists/warm1.nml output/warm1_output.nc

```

The simulation generates:

```text
output/warm1_output.nc

```

which can be analysed using Python and NetCDF4.

---

## 🌧️ Official KiD Warm Benchmark Test

The official KiD 1-D warm-cloud benchmark case (`warm1.nml`) was successfully compiled and executed under Ubuntu/WSL using `gfortran`, `build-essential`, and NetCDF libraries.

The simulation produced an official KiD NetCDF output file:

`output/warm1_output.nc`

The benchmark output shows realistic warm-cloud evolution, with rapid cloud-water growth followed by rain-water formation and gradual decay.

This provides the first official KiD benchmark reference output for future direct comparison with the Python cloud parcel model.

![KiD Warm Benchmark](figures/kid_warm1_comparison.png)

*Figure: Official KiD warm-cloud benchmark showing cloud-water and rain-water evolution over time.*

---

## Direct KiD Benchmark Alignment

An improved warm-cloud alignment experiment was developed to directly compare the simplified Python parcel model against the official KiD warm-cloud benchmark.

The alignment reproduces several key qualitative behaviours observed in the KiD reference simulation, including:

- rapid cloud-water growth
- delayed rain-water onset
- gradual post-peak decay
- realistic timing differences between cloud and rain evolution

The comparison demonstrates that simplified parcel-model physics can qualitatively reproduce important warm-cloud microphysical behaviour under KiD-inspired forcing conditions.

This provides an initial framework for future quantitative benchmarking between simplified parcel models and established cloud microphysics schemes.

![Improved KiD Alignment](figures/case7_improved_warm_alignment.png)

---

### Additional scripts

Additional exploratory and sensitivity experiments are available:

```bash
python parcel_model/run_parcel_competition.py
python parcel_model/run_bioIN_onset.py
python parcel_model/run_mixed_phase_maxwell.py
python run_mixed_phase_minimal.py
python run_mixed_phase_updraft_sweep.py

```

These scripts investigate:

- vapour competition between liquid and ice
- biological ice nucleation onset
- mixed-phase cloud evolution
- sensitivity to updraft velocity
- Maxwellian condensational growth
  
---

## Generating Diagnostics

Generate diagnostic figures using:

```bash
python plotting/plot_kid_case1.py
python plotting/plot_case2_from_maxwell.py
python plotting/plot_R_ratio.py
python plotting/plot_Si_minus_Sw.py

```

These diagnostics illustrate:

- supersaturation evolution (`Sw` and `Si`)
- liquid and ice condensational growth
- vapour competition between condensation and deposition
- warm-rain and mixed-phase cloud evolution
- thermodynamic phase transitions

---

## Planned Developments

Future extensions of the model include:

- fully coupled buoyancy–updraft feedback
- pressure evolution along parcel ascent
- multi-bin droplet and ice size distributions
- sensitivity studies across aerosol populations
- comparison with laboratory and field observations

---

## Status

This repository contains a research-oriented prototype developed for physical process exploration, conceptual modelling, and hypothesis generation.

It is not intended for operational weather forecasting or climate prediction applications.

---

## Citation

If you use this repository in research or educational work, please cite the project appropriately.

A DOI and formal citation entry will be provided following a future Zenodo release.

























