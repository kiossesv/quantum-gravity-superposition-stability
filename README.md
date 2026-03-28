# Stability limits of effective gravitational models under quantum superposition
### Quantum Gravity Superposition Program -- Project 2
Numerical framework for investigating the **dynamical stability of effective gravitational descriptions** when gravitational fields are associated with **quantum superpositions of classical configurations**.

This repository contains the simulation code used in the study:

**V. I. Kiosses**

Stability limits of effective gravitational descriptions under quantum superposition (2026)

## Overview
In many semiclassical approaches to gravity, a **single effective gravitational field** is used to represent a system whose underlying gravitational configuration may involve multiple quantum branches.
In situations where gravity itself is associated with a quantum superposition of classical configurations, such effective descriptions may become unreliable.

This project investigates this question through direct numerical comparison between:
- **branch-resolved quantum dynamics**
- **effective gravitational evolution**
The central goal is to determine **when an effective gravitational description remains dynamically stable** under uncertainty in the underlying quantum superposition.

## Research Program Context
This repository is part of a **three-project research program** studying gravitational fields in quantum superposition.

### Project 1
**quantum-gravity-superposition-dynamics**
Numerically stable solver for branch-resolved quantum dynamics in superposed gravitational fields.

### Project 2 (this repository)
**quantum-gravity-superposition-stability**
Statistical stability analysis of effective gravitational models

### Project 3 (planned)
**quantum-gravity-superposition-sciml**
Physics-informed machine learning for predicting stability regimes of effective gravity

## Physical Model
We consider a non-relativistic quantum particle evolving under branch-dependent gravitational fields $V_i(x)=mg_i x$.

Each branch evolves independently under $\hat{H}_i = \frac{\hat{p}^2}{2m} + V_i(x)$.

The full quantum state is $\Psi(x,t) = \sum_i c_i \psi_i(x,t)$.

This branch-resolved formulation retains the full information about the superposed gravitational configuration.

### Effective Gravitational Approximation
A commonly used approximation replaces the superposed fields with a single effective acceleration $g_{\text{eff}}=\sum_i |c_i|^2 g_i$.

The particle then evolves under $V_{\text{eff}}=mg_{\text{eff}} x$.

The effective description therefore replaces a coherent multi-branch gravitational configuration with a single averaged field. The key question addressed in this project is: **Is this approximation dynamically stable?**

## Numerical Method
The simulations use a **spectral split-operator solver** for the time-dependent Schrödinger equation.
Features:
- FFT-based propagation
- second-order split-operator method
- periodic spatial domain
- branch-resolved evolution
- Monte-Carlo ensemble simulations
The solver is inherited from **Project 1**, where its unitarity and numerical stability were validated.

### Stability Test Framework
To probe robustness, controlled stochastic uncertainty is introduced in the branch weights $|c_i|^2 \righarrow |c_i|^2 + \delta_i$.

Each Monte-Carlo realization defines a perturbed effective acceleration $g_{\text{eff}}=\sum_i (c_i|^2 + \delta_i) g_i$.

The resulting effective evolution is compared with the branch-resolved reference dynamics.

###Stability Diagnostics
The primary observable used to compare the two descriptions is $\langle \hat{x}(t) \rangle$.

Trajectory disagreement is quantified using the RMS deviation $\Delta x_{RMS}} = \left( \frac{1}{T}\int_0^T (\langle x(t) \rangle_{eff}} - \langle x(t) \rangle_{ref})^2 dt \right)^{1/2}$.

An effective model is considered **unstable** when $\Delta x_{RMS} > \Delta x_{\text{crit}}$.

The ensemble failure probability is $P_{\text{fail}} = \frac{1}{N} \sum_{k=1}^N \Theta \left( \Delta x_{RMS}^{(k)} - \Delta x_{\text{crit}}^{(k)}\right)$.

## Scientific Results Preview
The numerical framework implemented in this repository was used to investigate the **stability of effective gravitational descriptions** when the underlying gravitational configuration is associated with a **quantum superposition of classical fields**.
The simulations compare:
- branch-resolved quantum dynamics (reference model)
- effective gravitational evolution using an averaged field
under controlled stochastic perturbations of the branch weights.

### Distribution of the Effective Gravitational Field
Monte Carlo sampling of stochastic branch weights produces a distribution of the effective gravitational acceleration $g_{\text{eff}}$.
Despite the introduced uncertainty, the distribution remains **narrow and well defined**, indicating that the effective gravitational parameter itself is statistically stable.

![Distribution of effective gravitational acceleration](figures/Figure_1b.png)

### Trajectory Deviations
Even when fluctuations in the effective gravitational acceleration are small, the resulting trajectories deviate progressively from the branch-resolved dynamics.
Because gravitational acceleration enters directly into the equations of motion, small mismatches accumulate in time.
![Trajectory deviations](figures/Figure_2b.png)
Solid lines represent the **branch-resolved reference dynamics**, while dashed lines correspond to **effective gravitational evolution**.
The deviations grow systematically during the evolution.

### Ensemble Stability Analysis
The stability of the effective description is evaluated using the RMS deviation $\Delta x_{RMS}}$.
Across the Monte Carlo ensemble, the RMS deviation exceeds the stability threshold in nearly all realizations.
![RMS deviation distribution](figures/Figure_3b.png)
This leads to a **failure probability approaching unity** in the investigated parameter regimes.

### Physical Interpretation
The instability arises from a structural difference between the two descriptions.
The branch-resolved dynamics preserves correlations between the probe motion and the underlying gravitational configuration, while the effective model replaces the superposed gravitational fields with a single averaged field.
Small fluctuations in the effective acceleration therefore accumulate deterministically during time evolution, producing trajectory deviations that grow approximately as $\Delta x \propto t^2$.

### Key Result
Although the effective gravitational acceleration remains statistically well defined, the corresponding dynamical trajectories become unstable under stochastic perturbations of the quantum superposition structure.
This reveals a **structural limitation of effective gravitational descriptions** in regimes involving **quantum superpositions of gravitational fields**.


## Repository Structure
```
quantum-gravity-superposition-stability/
│
├── src/
│        core solver (from Project 1)
│        ├── solvers.py
│        ├── observables.py
│        ├── potentials.py
│        ├── initial_states.py
│
│        stochastic stability framework
│        ├── samplers.py
│        ├── effective_gravity.py
│        ├── ensemble_runner.py
│
│        analysis utilities
│        ├── metrics.py
│        ├── analysis.py
│
│        numerical experiments
│        ├── deterministic_baseline.py
│        ├── stochastic_weights.py
│        └── monte_carlo_stability.py
│
├── figures/
│
│        documentation
└── README.md
```

## Reproducibility Instructions
### Running the Simulations

#### Deterministic benchmark
 `python deterministic_baseline.py`
Computes the deterministic baseline by evolving the system under branch-resolved gravitational fields and comparing it with the corresponding effective gravitational model.

![Deterministic baseline](figures/Figure_deterministic.png)

Comparison of the expectation value $\langle x(t) \rangle$ obtained from branch-resolved dynamics and the effective gravitational field, showing agreement in the noiseless reference case.


#### Stochastic branch perturbations
` python stochastic_weights.py`
Simulates Monte Carlo realizations of stochastic branch weights and compares branch-resolved dynamics with the corresponding effective gravitational model.

![Stochastic deviations](figures/Figure_stochastics_weights_deviations.png)

Each curve shows the deviation $\Delta \langle x(t) \rangle$ between branch-resolved and effective trajectories for one stochastic realization, illustrating the time-accumulation of small acceleration mismatches.

#### Full Monte-Carlo stability analysis
`python monte_carlo_stability.py`

Computes RMS deviations and failure probability across ensembles.



## Current Limitations
The present implementation focuses on a minimal controlled model:
- one spatial dimension
- uniform gravitational potentials
- coherent branch dynamics
- no decoherence
- no phase noise
These restrictions allow a clear investigation of stability properties of effective gravity.

## Future Directions
Possible extensions include:
- non-uniform gravitational fields
- multi-branch superpositions
- decoherence effects
- higher-dimensional dynamics
- machine-learning stability prediction (Project 3)

## Citation
If you use this code in research, please cite:

Kiosses, V. I.
Stability limits of effective gravitational descriptions under quantum superposition (2026)
===================================================================
## Research Context

This project is part of a three-repository research program on gravitational fields in quantum superposition:

- [Project 1: quantum-gravity-superposition-dynamics](https://github.com/kiossesv/quantum-gravity-superposition-dynamics)
- [Project 2: quantum-gravity-superposition-stability](https://github.com/kiossesv/quantum-gravity-superposition-stability)
- [Project 3: quantum-gravity-superposition-sciml](https://github.com/kiossesv/quantum-gravity-superposition-sciml)

## Relation to Project 1
This project directly builds on **Project 1: Numerical Time Evolution of Quantum States in Superposed Gravitational Fields.**
- **Project 1** establishes a clean, unitary, and numerically stable solver for branch-resolved quantum dynamics under superposed gravitational fields.
- **Project 2** uses that solver as a reference model and asks a deeper question:
*Under what conditions can branch-resolved quantum-gravitational dynamics be faithfully approximated by an effective gravitational field?*
In this sense, Project 1 provides the **numerical ground truth**, while Project 2 provides the **stability and robustness analysis**.

## Problem Statement - Overview
In classical physics, a gravitational field is characterized by a single acceleration parameter $g$.
In quantum scenarios, however, gravity itself may be associated with a system in superposition, leading to multiple, branch-dependent gravitational fields acting simultaneously on a quantum probe.

We consider a quantum particle evolving under superposed uniform gravitational fields, $V_1(x)=mg_1 x$ and $V_2(x)=mg_2 x$, where $g_1 \ne g_2$ correspond to distinct classical gravitational configurations.

While **Project 1** demonstrated that such branch-resolved dynamics can be simulated reliably, **the central question here is different**:
*Can this dynamics be replaced by a single effective gravitational model without losing physical validity?*
This project treats effective gravitational descriptions as testable approximations, not fundamental assumptions.

## Branch-Resolved vs Effective Descriptions
### Branch-Resolved Description (Reference Model)
The full quantum state is represented as a coherent superposition of branch-dependent wavefunctions:
![Superposed wavefunctions](docs/superposed_wavefunctions.svg)

Each branch evolves independently according to $\hat{H} \psi_i = (\hat{p}^2/2m + mg_i x) \psi_i$.

This description:
- retains full phase information,
- serves as the ground truth dynamics,
- is inherited directly from Project 1.

### Effective gravitational description
An effective model replaces the superposed fields with a single potential $V_{eff} = mg_{eff} x$, where $g_{eff}$ is constructed from branch data (e.g. expectation-based averaging).

The effective wavefunction evolves according to a single Schrödinger equation with a global time parameter.

Such models are common in semiclassical and phenomenological approaches — but their domain of validity under quantum superposition is not guaranteed.

## Conceptual Scope
This project does not assume that an effective gravitational model must exist.

Instead:
- effective descriptions are treated as hypotheses,
- breakdowns are interpreted as physical limitations, not numerical failures.

The objective is to determine when, how, and to what extent effective gravity provides a stable approximation to branch-resolved quantum dynamics.



## Design Constraint: Stability Under Uncertainty
### Conceptual Principle

Effective gravitational models should remain meaningful under controlled uncertainty.
Accordingly, stability is assessed statistically, not via single deterministic trajectories.

### Stochastic Branch Structure

Branch coefficients are modeled as stochastic variables to reflect:
- preparation uncertainty,
- environmental effects,
- incomplete information.
![Stochastic variables](docs/stochastic_variables.svg)
where each realization $k$ corresponds to one Monte Carlo sample.

As a result, effective quantities such as $g_{eff} = \sum_i |c_i|^2 g_i$, become random variables with associated distributions.


### Monte Carlo Stability Criterion

For each Monte Carlo realization:
1. Branch weights are sampled from a controlled noise distribution.
2. An effective gravitational field is constructed.
3. The system is evolved under:
    - branch-resolved dynamics,
    - effective single-field dynamics.
4. Deviations are quantified using observables and state-based metrics.

Stability is defined statistically, via ensemble-averaged behavior rather than individual realizations.

**Stability Criterion**
*An effective gravitational model is considered stable if the ensemble-averaged deviation of $\langle x(t)\rangle$from the effective prediction remains bounded within statistical uncertainty over the simulation time.*


## Computational implementation

### Deterministic Baseline

A noiseless reference case establishes:
- when effective gravity reproduces branch-resolved dynamics,
- the limits of agreement in ideal conditions.

This baseline is **necessary but not sufficient**.

Due to the use of FFT-based split-operator methods with periodic boundary conditions, uniform gravitational acceleration leads to linear momentum drift. All deterministic benchmarks are therefore restricted to times $t < t_{max} \sim \frac{\pi \hbar N}{m g_max L}$, ensuring spectral validity and preventing momentum aliasing.

### Stochastic Branch Weights

Controlled noise is introduced while preserving normalization.
This probes sensitivity to microscopic uncertainty in the quantum superposition structure.


### Monte Carlo Stability and Robustness

Large ensembles of noisy realizations are used to:
- quantify mean deviations,
- identify variance growth,
- detect breakdown thresholds.

This shifts the analysis from **trajectory-level agreement** to **statistical reliability**.


## Benchmarks and Validation
- deterministic_baseline.py
  Validates agreement in the noiseless limit.
- stochastic_weights.py
  Examines realization-dependent deviations under noisy branch weights.
- monte_carlo_stability.py
  Performs ensemble analysis to identify robustness regimes and instability thresholds.

Together, these benchmarks form a future-proof validation pipeline for effective gravitational models.



## Module-level design - Code Structure 
```
quantum-gravity-superposition-stability/
│
├── solvers.py                   # inherited from Project 1
├── observables.py.          # inherited from Project 1
├── potentials.py               # inherited from Project 1
├── initial_states.py.          # inherited from Project 1
│
├── samplers.py                # stochastic branch weights
├── effective_gravity.py     # mapping to effective fields
├── ensemble_runner.py      # Monte Carlo orchestration
├── metrics.py                   # stability diagnostics
├── analysis.py                  # statistical post-processing
│
│
├── deterministic_baseline.py       # benchmark 1
├── stochastic_weights.py           # benchmark 2
├── monte_carlo_stability.py        # benchmark 3
│
└── README.md

```

## Limitations (Current Version)
- 1D dynamics
- Uniform linear gravitational potentials
- No phase noise
- No decoherence

These are intentional constraints, allowing controlled interpretation of stability and breakdown.

## Outlook
This project establishes a statistically grounded framework for testing effective gravitational models under quantum superposition.
Natural extensions include:
phase noise and decoherence,
non-uniform fields,
higher-dimensional dynamics,
physics-informed machine learning for surrogate stability prediction (Project 3).
