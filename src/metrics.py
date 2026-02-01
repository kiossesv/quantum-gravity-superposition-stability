import numpy as np

def observable_deviation(obs_branch, obs_eff):
    """
    Compute deviation between branch-resolved and effective observables.

    Parameters
    ----------
    obs_branch : ndarray, shape (n_realizations, n_times)
    obs_eff : ndarray, shape (n_realizations, n_times)

    Returns
    -------
    deviation : ndarray
    """
    return obs_branch - obs_eff


def rms_deviation(deviation):
    """
    Root-mean-square deviation over time.
    """
    return np.sqrt(np.mean(deviation**2, axis=1))


def failure_probability(rms_dev, threshold):
    """
    Probability that deviation exceeds threshold.

    Returns
    -------
    float
    """
    return np.mean(rms_dev > threshold)
