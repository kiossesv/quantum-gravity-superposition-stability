import numpy as np

def summarize_geff(geff):
    return {
        "mean": np.mean(geff),
        "std": np.std(geff),
        "min": np.min(geff),
        "max": np.max(geff),
    }


def summarize_deviation(deviation):
    return {
        "mean": np.mean(deviation),
        "std": np.std(deviation),
    }
