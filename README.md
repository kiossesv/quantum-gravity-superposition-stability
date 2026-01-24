# Stability and robustness of effective gravitational models in quantum superposition
### Project 2 -- v1.0

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
├── benchmarks/
│   ├── deterministic_baseline.py
│   ├── stochastic_weights.py
│   └── monte_carlo_stability.py
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
