# Convergence Analysis

A simple plane acoustic wave traveling in a 2D duct is used as a first level to confirm the validity of the simulations.
We use the scattered field formulation with an incident wave
$$ p_i=\hat{p}_i \exp(i kx +\phi), $$
travelling from left to right.
The duct consists of the simulation domain $\Omega_d$, two spacing domains $\Omega_s$ of thickness $d_s$, and two
absorbers with thickness $d_a$ in the PML domain $\Omega_{absorber}$.
All boundaries $\Gamma$ of the overall domain $\Omega=\Omega_{absorber}\cup \Omega_d\cup \Omega_s$ are sound hard.

To eliminate the influence of the absorbers, they are oversized massively.
