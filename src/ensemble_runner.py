import numpy as np
from samplers import sample_branch_weights
from effective_gravity import compute_geff

def run_ensemble(
    mean_probs,
    g_values,
    noise_strength,
    n_realizations,
    evolve_branch,
    evolve_effective,
    seed=None
):
    """
    Run ensemble of stochastic realizations.

    evolve_branch(probs) -> observables
    evolve_effective(geff) -> observables
    """

    branch_probs = sample_branch_weights(
        mean_probs,
        noise_strength,
        n_realizations,
        seed
    )

    geff = compute_geff(branch_probs, g_values)

    obs_branch = []
    obs_eff = []

    for k in range(n_realizations):
        obs_branch.append(evolve_branch(branch_probs[k]))
        obs_eff.append(evolve_effective(geff[k]))

    return {
        "branch_probs": branch_probs,
        "geff": geff,
        "obs_branch": np.array(obs_branch),
        "obs_eff": np.array(obs_eff),
    }
