import numpy as np
import matplotlib.pyplot as plt

from solvers import time_evolution
from observables import expectation_x
from potentials import linear_potential
from initial_states import gaussian_wavepacket

# --- physics ---
m = 1.0
hbar = 1.0

g_values = np.array([1.0, 3.0])
probs = np.array([0.5, 0.5])
g_eff = np.sum(probs * g_values)

# --- numerics ---
Nx = 1024
x = np.linspace(-20, 20, Nx)
dx = x[1] - x[0]

dt = 0.01
Nt = 400
times = np.arange(Nt) * dt

# --- initial state ---
psi0 = gaussian_wavepacket(x, x0=0.0, p0=0.0)

# --- branch evolution ---
x_branch = np.zeros(Nt)

for p, g in zip(probs, g_values):
    V = linear_potential(x, m, g)
    psi_t = time_evolution(psi0, V, x, dt, Nt)
    x_branch += p * np.array([expectation_x(psi, x) for psi in psi_t])

# --- effective evolution ---
V_eff = linear_potential(x, m, g_eff)
psi_eff_t = time_evolution(psi0, V_eff, x, dt, Nt)
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

