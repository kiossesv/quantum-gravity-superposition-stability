import numpy as np
import matplotlib.pyplot as plt


from utils import create_grids
from samplers import sample_branch_weights
from solvers import time_evolution
from observables import expectation_x
from potentials import linear_gravity_potential
from initial_states import gaussian_wavepacket, normalize

# --- physics ---
m = 1.0
hbar = 1.0
x0 = -10.0
p0 = 3.0
sigma = 1.0

g_values = np.array([1.0, 3.0])
probs = np.array([0.5, 0.5])

noise_strength = 0.05
n_realizations = 20

# --- numerics ---
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


# --- sample weights ---
branch_probs = sample_branch_weights(
    probs,
    noise_strength,
    n_realizations,
    seed=1
)

# --- plot ---
plt.figure()

for probals in branch_probs:
    # branch-resolved
    x_branch = np.zeros(n_steps)
    for pr_v, g in zip(probals, g_values):
        V = linear_gravity_potential(x, m, g)
        psi_t = time_evolution(psi0, V, x, p, dt, n_steps, hbar, m, store_wavefunction=True)
        psi_t = psi_t['psi']
        x_branch += pr_v * np.array([expectation_x(psi, x) for psi in psi_t])

    # effective
    g_eff = np.sum(probals * g_values)
    V_eff = linear_gravity_potential(x, m, g_eff)
    psi_eff_t = time_evolution(psi0, V_eff, x, p, dt, n_steps, hbar, m, store_wavefunction=True)
    psi_eff_t = psi_eff_t['psi']
    x_eff = np.array([expectation_x(psi, x) for psi in psi_eff_t])

    plt.plot(times, x_branch - x_eff, alpha=0.5)

plt.xlabel("Time")
plt.ylabel(r"$\Delta\langle x \rangle$")
plt.title("Stochastic Branch Weights: Realization-wise Deviations")
plt.tight_layout()
plt.savefig("../figures/Figure_stochastics_weights_deviations.png")
plt.close()
