# NOTE:
# This benchmark is valid only before wavepacket wrap-around
# due to periodic FFT boundary conditions.


import numpy as np
import matplotlib.pyplot as plt


from utils import create_grids
from initial_states import gaussian_wavepacket, normalize
from potentials import linear_gravity_potential
from solvers import time_evolution
from observables import expectation_x


# --- physics ---
m = 1.0
hbar = 1.0
x0 = -10.0
p0 = 2.0
sigma = 1.0

g_values = np.array([1.0, 3.0])
probs = np.array([0.5, 0.5])
g_eff = np.sum(probs * g_values)

# --- numerics ---
L = 100.0
N = 2048

dt = 0.01
n_steps = 400
times = np.arange(n_steps) * dt


# --- maximum safe simulation time ---
alpha = 0.4                   # conservative safety factor
g_max = np.max(g_values)      # worst-case gravity

t_max_safe = alpha * np.pi * hbar * N / (m * g_max * L)
if n_steps * dt > t_max_safe:
    print("WARNING: Simulation exceeds FFT spectral validity time")


# --- Create grids ---
x, p, dx = create_grids(N, L, hbar)




# --- initial state ---
psi0 = gaussian_wavepacket(x, x0, p0, sigma, hbar)
psi0 = normalize(psi0, dx)

# --- branch evolution ---
x_branch = np.zeros(n_steps)

for pr_v, g in zip(probs, g_values):
    V = linear_gravity_potential(x, m, g)
    psi_t = time_evolution(psi0, V, x, p, dt, n_steps, hbar, m, store_wavefunction=True)
    psi_t = psi_t['psi']
    x_branch += pr_v * np.array([expectation_x(psi, x) for psi in psi_t])

# --- effective evolution ---
V_eff = linear_gravity_potential(x, m, g_eff)
psi_eff_t = time_evolution(psi0, V_eff, x, p, dt, n_steps, hbar, m, store_wavefunction=True)
psi_eff_t = psi_eff_t['psi']
x_eff = np.array([expectation_x(psi, x) for psi in psi_eff_t])

# --- plot ---
plt.figure()
plt.plot(times, x_branch, label="Branch-resolved")
plt.plot(times, x_eff, "--", label="Effective")
plt.xlabel("Time")
plt.ylabel(r"$\langle x \rangle$")
plt.legend()
plt.title("Deterministic Baseline: Branch vs Effective Gravity")
plt.show()

