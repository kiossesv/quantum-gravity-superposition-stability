import numpy as np
import matplotlib.pyplot as plt

from ensemble_runner import run_ensemble
from metrics import observable_deviation, rms_deviation, failure_probability
from analysis import summarize_geff

# --- import  project machinery ---
from utils import create_grids
from initial_states import gaussian_wavepacket, normalize
from potentials import linear_gravity_potential
from solvers import time_evolution
from observables import expectation_x


# --- user physics parameters ---
m = 1.0
hbar = 1.0
x0 = -10.0
p0 = 2.0
sigma = 1.0

g_values = np.array([1.0, 3.0])     # branch gravitational fields
mean_probs = np.array([0.5, 0.5])   # mean |c_i|^2

noise_strength = 0.05
n_realizations = 200

threshold_x = 0.2   # stability threshold for <x>

# --- numerical grids (example) ---
L = 40.0
N = 1024

dt = 0.01
n_steps = 400
times = np.arange(n_steps) * dt


# --- maximum safe simulation time ---
safe_f = 0.4                   # conservative safety factor
g_max = np.max(g_values)      # worst-case gravity

t_max_safe = safe_f * np.pi * hbar * N / (m * g_max * L)
if n_steps * dt > t_max_safe:
    print("WARNING: Simulation exceeds FFT spectral validity time")

# --- Create grids ---
x, p, dx = create_grids(N, L, hbar)

# --- initial state ---
psi0 = gaussian_wavepacket(x, x0, p0, sigma, hbar)
psi0 = normalize(psi0, dx)


# --- evolution wrappers ---
def evolve_effective(geff):
    V = linear_gravity_potential(x, m, geff)
    psi_t = time_evolution(psi0, V, x, p, dt, n_steps, hbar, m, store_wavefunction=True)
    psi_t = psi_t['psi']
    return np.array([expectation_x(psi, x) for psi in psi_t])


def evolve_branch(branch_probs):
    x_exp_total = np.zeros(n_steps)

    for prob, g in zip(branch_probs, g_values):
        V = linear_gravity_potential(x, m, g)
        psi_t = time_evolution(psi0, V, x, p, dt, n_steps, hbar, m, store_wavefunction=True)
        psi_t = psi_t['psi']

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
plt.title("Distribution of Effective Gravitational Acceleration")
plt.tight_layout()
plt.savefig("../figures/Figure_1b.png")
plt.close()

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
plt.tight_layout()
plt.savefig("../figures/Figure_mean_deviation.png")
plt.close()


plt.figure()
plt.scatter(
    np.arange(len(rms_dx)),
    rms_dx,
    s=20
)

plt.axhline(
    y=threshold_x,
    linestyle='--',
    linewidth=2
)

plt.xlabel("Monte Carlo realization")
plt.ylabel(r"$\Delta x_{\mathrm{RMS}}$")

plt.tight_layout()
plt.savefig("../figures/Figure_3b.png")
plt.close()


# choose a few representative realizations
indices = [0, 3, 7]   # or np.random.choice(N, 3, replace=False)
x_ref_all = results["obs_branch"]
x_eff_all = results["obs_eff"]

plt.figure()
for k in indices:
    plt.plot(times, x_ref_all[k], linewidth=2)
    plt.plot(times, x_eff_all[k], linestyle='--', linewidth=2)

plt.xlabel(r"$t$")
plt.ylabel(r"$\langle x(t) \rangle$")
plt.title("Branch-resolved vs effective trajectories")

plt.tight_layout()
plt.savefig("../figures/Figure_2b.png")
plt.close()
