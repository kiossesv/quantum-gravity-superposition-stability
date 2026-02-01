import numpy as np
import matplotlib.pyplot as plt

from samplers import sample_branch_weights
from solvers import time_evolution
from observables import expectation_x
from potentials import linear_potential
from initial_states import gaussian_wavepacket

# --- physics ---
m = 1.0

g_values = np.array([1.0, 3.0])
mean_probs = np.array([0.5, 0.5])

noise_strength = 0.05
n_realizations = 20

# --- numerics ---
Nx = 1024
x = np.linspace(-20, 20, Nx)

dt = 0.01
Nt = 400
times = np.arange(Nt) * dt

psi0 = gaussian_wavepacket(x, x0=0.0, p0=0.0)

# --- sample weights ---
branch_probs = sample_branch_weights(
    mean_probs,
    noise_strength,
    n_realizations,
    seed=1
)

# --- plot ---
plt.figure()

for probs in branch_probs:
    # branch-resolved
    x_branch = np.zeros(Nt)
    for p, g in zip(probs, g_values):
        V = linear_potential(x, m, g)
        psi_t = time_evolution(psi0, V, x, dt, Nt)
        x_branch += p * np.array([expectation_x(psi, x) for psi in psi_t])

    # effective
    g_eff = np.sum(probs * g_values)
    V_eff = linear_potential(x, m, g_eff)
    psi_eff_t = time_evolution(psi0, V_eff, x, dt, Nt)
    x_eff = np.array([expectation_x(psi, x) for psi in psi_eff_t])

    plt.plot(times, x_branch - x_eff, alpha=0.5)

plt.xlabel("Time")
plt.ylabel(r"$\Delta\langle x \rangle$")
plt.title("Stochastic Branch Weights: Realization-wise Deviations")
plt.show()

