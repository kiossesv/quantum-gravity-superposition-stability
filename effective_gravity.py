import numpy as np

def compute_geff(branch_probs, g_values):
    """
    Compute effective gravitational field per realization.

    Parameters
    ----------
    branch_probs : ndarray, shape (n_realizations, n_branches)
    g_values : array-like
        Gravitational field values for each branch.

    Returns
    -------
    geff : ndarray, shape (n_realizations,)
        Effective gravitational field per realization.
    """
    branch_probs = np.asarray(branch_probs)
    g_values = np.asarray(g_values)

    return np.sum(branch_probs * g_values, axis=1)
