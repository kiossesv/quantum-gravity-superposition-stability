import numpy as np

def sample_branch_weights(
    mean_probs,
    noise_strength=0.0,
    n_realizations=1,
    seed=None
):
    """
    Sample stochastic branch weights with normalization enforced.

    Parameters
    ----------
    mean_probs : array-like
        Mean probabilities |c_i|^2 (must sum to 1).
    noise_strength : float
        Standard deviation of Gaussian noise.
    n_realizations : int
        Number of Monte Carlo samples.
    seed : int or None
        Random seed for reproducibility.

    Returns
    -------
    probs : ndarray, shape (n_realizations, n_branches)
        Normalized branch probabilities per realization.
    """
    rng = np.random.default_rng(seed)
    mean_probs = np.array(mean_probs)

    probs = []
    for _ in range(n_realizations):
        noisy = mean_probs + rng.normal(0.0, noise_strength, size=len(mean_probs))
        noisy = np.clip(noisy, 0.0, None)
        noisy /= np.sum(noisy)
        probs.append(noisy)

    return np.array(probs)
