import numpy as np
import matplotlib.pyplot as plt

from ensemble_runner import run_ensemble
from metrics import observable_deviation, rms_deviation, failure_probability
from analysis import summarize_geff

# --- user physics parameters ---
m = 1.0
hbar = 1.0

g_values = np.array([1.0, 3.0])     # branch gravitational fields
mean_probs = np.array([0.5, 0.5])   # mean |c_i|^2

noise_strength = 0.05
n_realizations = 200

threshold_x = 0.2   # stability threshold for <x>

# --- numerical grids (example) ---
Nx = 1024
x = np.linspace(-20, 20, Nx)
dx = x[1] - x[0]

dt = 0.01
Nt = 400
times = np.arange(Nt) * dt

# --- import your own project machinery ---
from initial_states import gaussian_wavepacket
from potentials import linear_potential
from solvers import time_evolution
from observables import expectation_x


# --- evolution wrappers ---
def evolve_effective(geff):
    V = linear_potential(x, m, geff)
    psi0 = gaussian_wavepacket(x, x0=0.0, p0=0.0)
    psi_t = time_evolution(psi0, V, x, dt, Nt)
    return np.array([expectation_x(psi, x) for psi in psi_t])


def evolve_branch(branch_probs):
    x_exp_total = np.zeros(Nt)

    for prob, g in zip(branch_probs, g_values):
        V = linear_potential(x, m, g)
        psi0 = gaussian_wavepacket(x, x0=0.0, p0=0.0)
        psi_t = time_evolution(psi0, V, x, dt, Nt)

        x_exp = np.array([expectation_x(psi, x) for psi in psi_t])
        x_exp_total += prob * x_exp

    return x_exp_total


# --- Monte Carlo run ---
results = run_ensemble(
    mean_probs=mean_probs,
    g_values=g_values,
    noise_strength=noise_strength,
    n_realizations=n_realizations,
    evolve_branch=evolve_branch,
    evolve_effective=evolve_effective,
    seed=42
)

# --- diagnostics ---
dx_t = observable_deviation(results["obs_branch"], results["obs_eff"])
rms_dx = rms_deviation(dx_t)

fail_prob = failure_probability(rms_dx, threshold_x)
geff_stats = summarize_geff(results["geff"])

# --- reporting ---
print("Effective gravity statistics:")
for k, v in geff_stats.items():
    print(f"{k:>6}: {v:.4f}")

print(f"\nFailure probability (Δ<x> RMS > {threshold_x}): {fail_prob:.3f}")

# --- plots ---
plt.figure()
plt.hist(results["geff"], bins=30)
plt.xlabel(r"$g_{\mathrm{eff}}$")
plt.ylabel("Counts")
plt.title("Distribution of Effective Gravitational Field")
plt.show()

plt.figure()
plt.plot(times, np.mean(dx_t, axis=0))
plt.fill_between(
    times,
    np.mean(dx_t, axis=0) - np.std(dx_t, axis=0),
    np.mean(dx_t, axis=0) + np.std(dx_t, axis=0),
    alpha=0.3
)
plt.xlabel("Time")
plt.ylabel(r"$\langle x \rangle_{\mathrm{branch}} - \langle x \rangle_{\mathrm{eff}}$")
plt.title("Mean Deviation with Ensemble Spread")
plt.show()
