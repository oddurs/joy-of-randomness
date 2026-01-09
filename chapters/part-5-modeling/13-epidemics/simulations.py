"""
Chapter 13: Epidemics
Stochastic SIR models, extinction probability, and the role of randomness in disease spread.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.special import comb


# ============================================================================
# Deterministic SIR Model (ODE)
# ============================================================================

def sir_deterministic(y, t, beta, gamma, N):
    """
    Deterministic SIR model using differential equations.
    
    Args:
        y: [S, I, R] state
        t: time (not used, for scipy.integrate.odeint)
        beta: transmission rate
        gamma: recovery rate
        N: population size
    
    Returns:
        [dS/dt, dI/dt, dR/dt]
    """
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]


def solve_sir_deterministic(N, beta, gamma, I0=1, t_max=100):
    """
    Solve deterministic SIR using ODE integration.
    
    Args:
        N: population size
        beta: transmission rate
        gamma: recovery rate
        I0: initial infections
        t_max: maximum time
    
    Returns:
        t, S, I, R
    """
    S0 = N - I0
    R0 = 0
    y0 = [S0, I0, R0]
    
    t = np.linspace(0, t_max, 1000)
    solution = odeint(sir_deterministic, y0, t, args=(beta, gamma, N))
    
    S = solution[:, 0]
    I = solution[:, 1]
    R = solution[:, 2]
    
    return t, S, I, R


# ============================================================================
# Stochastic SIR Model (Discrete Time)
# ============================================================================

def sir_stochastic_discrete(N, beta, gamma, I0=1, t_max=100, dt=0.1):
    """
    Stochastic SIR model using discrete-time Markov chain.
    
    Each time step:
    1. Transmissions: I individuals make contacts, some transmit
    2. Recoveries: I individuals recover with probability gamma*dt
    
    Args:
        N: population size
        beta: transmission rate (contacts per day)
        gamma: recovery rate (recovery probability per day)
        I0: initial infections
        t_max: maximum time
        dt: time step
    
    Returns:
        t, S, I, R arrays
    """
    S = N - I0
    I = I0
    R = 0
    
    t = []
    S_hist = []
    I_hist = []
    R_hist = []
    
    current_time = 0
    while current_time < t_max and I > 0:
        # Record state
        t.append(current_time)
        S_hist.append(S)
        I_hist.append(I)
        R_hist.append(R)
        
        # Transmission: each S-I pair transmits with probability beta*dt/N
        # Expected new infections: S * I * beta * dt / N
        # Actual new infections: random draw
        new_infections = np.random.binomial(S * I, beta * dt / N)
        new_infections = min(new_infections, S)  # Can't exceed S
        
        # Recoveries: each I recovers with probability gamma*dt
        recoveries = np.random.binomial(I, gamma * dt)
        
        # Update states
        S -= new_infections
        I = I + new_infections - recoveries
        R += recoveries
        
        current_time += dt
    
    # Final state
    if I > 0 or current_time < t_max:
        t.append(current_time)
        S_hist.append(S)
        I_hist.append(I)
        R_hist.append(R)
    
    return np.array(t), np.array(S_hist), np.array(I_hist), np.array(R_hist)


def sir_stochastic_many_runs(N, beta, gamma, I0=1, t_max=100, n_runs=100):
    """
    Run stochastic SIR many times.
    
    Args:
        N: population size
        beta: transmission rate
        gamma: recovery rate
        I0: initial infections
        t_max: maximum time
        n_runs: number of runs
    
    Returns:
        List of (t, S, I, R) tuples for each run
    """
    runs = []
    for _ in range(n_runs):
        result = sir_stochastic_discrete(N, beta, gamma, I0, t_max)
        runs.append(result)
    return runs


# ============================================================================
# Extinction Probability and R0
# ============================================================================

def compute_R0(beta, gamma):
    """
    Compute basic reproduction number R0 = beta / gamma.
    
    Args:
        beta: transmission rate
        gamma: recovery rate
    
    Returns:
        R0
    """
    return beta / gamma


def extinction_probability_branching(R0):
    """
    Extinction probability in branching process approximation.
    
    If R0 <= 1, extinction probability = 1.
    If R0 > 1, extinction probability = 1/R0.
    
    Args:
        R0: basic reproduction number
    
    Returns:
        Extinction probability
    """
    if R0 <= 1:
        return 1.0
    else:
        return 1.0 / R0


def major_outbreak_fraction(N, beta, gamma, I0=1, t_max=100, n_runs=100, threshold=0.1):
    """
    Estimate fraction of runs that result in "major" outbreaks.
    
    Major outbreak = infect > threshold fraction of population.
    
    Args:
        N: population size
        beta: transmission rate
        gamma: recovery rate
        I0: initial infections
        t_max: maximum time
        n_runs: number of stochastic runs
        threshold: fraction threshold (0.1 = 10%)
    
    Returns:
        Fraction of runs with major outbreak
    """
    runs = sir_stochastic_many_runs(N, beta, gamma, I0, t_max, n_runs)
    
    major_count = 0
    for t, S, I, R in runs:
        final_R = R[-1]
        if final_R / N > threshold:
            major_count += 1
    
    return major_count / n_runs


# ============================================================================
# Superspreaders
# ============================================================================

def sir_stochastic_superspreaders(N, beta, gamma, superspreader_fraction=0.1, 
                                   superspreader_mult=8, I0=1, t_max=100, dt=0.1):
    """
    Stochastic SIR with superspreaders.
    
    Fraction `superspreader_fraction` of infected people transmit with rate
    beta * superspreader_mult. Others transmit with rate beta / (1 - superspreader_fraction).
    
    (This keeps average transmission rate constant.)
    
    Args:
        N: population size
        beta: average transmission rate
        gamma: recovery rate
        superspreader_fraction: fraction that are superspreaders
        superspreader_mult: transmission multiplier for superspreaders
        I0: initial infections
        t_max: maximum time
        dt: time step
    
    Returns:
        t, S, I, R arrays
    """
    S = N - I0
    I_normal = I0
    I_super = 0
    R = 0
    
    t = []
    S_hist = []
    I_hist = []
    R_hist = []
    
    current_time = 0
    while current_time < t_max and (I_normal + I_super) > 0:
        t.append(current_time)
        S_hist.append(S)
        I_hist.append(I_normal + I_super)
        R_hist.append(R)
        
        # Transmissions from normal infected
        beta_normal = beta / (1 - superspreader_fraction)
        new_from_normal = np.random.binomial(S * I_normal, beta_normal * dt / N)
        new_from_normal = min(new_from_normal, S)
        
        # Transmissions from superspreaders
        beta_super = beta * superspreader_mult
        new_from_super = np.random.binomial(S * I_super, beta_super * dt / N)
        new_from_super = min(new_from_super, S)
        
        total_new = new_from_normal + new_from_super
        S -= total_new
        
        # Recoveries
        recoveries_normal = np.random.binomial(I_normal, gamma * dt)
        recoveries_super = np.random.binomial(I_super, gamma * dt)
        
        # Assign new infections to normal or superspreader status
        new_super = np.random.binomial(total_new, superspreader_fraction)
        new_normal = total_new - new_super
        
        I_normal = I_normal + new_normal - recoveries_normal
        I_super = I_super + new_super - recoveries_super
        R += recoveries_normal + recoveries_super
        
        current_time += dt
    
    return np.array(t), np.array(S_hist), np.array(I_hist), np.array(R_hist)


# ============================================================================
# Visualization
# ============================================================================

def plot_deterministic_vs_stochastic(N, beta, gamma, I0=1, t_max=100):
    """Plot deterministic SIR and multiple stochastic runs."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Deterministic
    t_det, S_det, I_det, R_det = solve_sir_deterministic(N, beta, gamma, I0, t_max)
    ax.plot(t_det, I_det, 'r-', linewidth=3, label='Deterministic', zorder=10)
    
    # Stochastic runs
    runs = sir_stochastic_many_runs(N, beta, gamma, I0, t_max, n_runs=100)
    for i, (t, S, I, R) in enumerate(runs):
        ax.plot(t, I, 'b-', alpha=0.1)
    
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Number Infected')
    ax.set_title(f'Deterministic vs. Stochastic SIR (N={N}, β={beta}, γ={gamma})')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(ymin=0)
    
    return fig


def plot_extinction_probability(N_range, beta, gamma):
    """Plot extinction probability vs. initial population size."""
    extinction_probs = []
    
    for N in N_range:
        major_fraction = major_outbreak_fraction(N, beta, gamma, n_runs=100)
        extinction_probs.append(1 - major_fraction)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.semilogy(N_range, extinction_probs, 'go-', linewidth=2, markersize=8)
    ax.set_xlabel('Initial Population Size (N)')
    ax.set_ylabel('Probability of Major Outbreak')
    ax.set_title(f'Extinction vs. Population Size (β={beta}, γ={gamma}, R₀={beta/gamma:.2f})')
    ax.grid(True, alpha=0.3, which='both')
    
    return fig


def plot_major_outbreak_vs_R0(R0_range, N=1000, gamma=0.1):
    """Plot fraction with major outbreak vs. R0."""
    major_fractions = []
    
    for R0 in R0_range:
        beta = R0 * gamma
        major_frac = major_outbreak_fraction(N, beta, gamma, n_runs=100)
        major_fractions.append(major_frac)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(R0_range, major_fractions, 'bs-', linewidth=2, markersize=8)
    ax.axvline(1.0, color='r', linestyle='--', linewidth=2, label='R₀ = 1')
    ax.set_xlabel('Basic Reproduction Number (R₀)')
    ax.set_ylabel('Fraction with Major Outbreak')
    ax.set_title(f'Outbreak Likelihood vs. R₀ (N={N})')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 1])
    
    return fig


def plot_superspreaders_effect(N, beta, gamma, I0=1, t_max=100):
    """Compare epidemics with and without superspreaders."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Normal
    runs_normal = sir_stochastic_many_runs(N, beta, gamma, I0, t_max, n_runs=50)
    ax = axes[0]
    for t, S, I, R in runs_normal:
        ax.plot(t, I, 'b-', alpha=0.2)
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Number Infected')
    ax.set_title('No Superspreaders')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(ymin=0)
    
    # Superspreaders
    ax = axes[1]
    for _ in range(50):
        t, S, I, R = sir_stochastic_superspreaders(N, beta, gamma, I0=I0, t_max=t_max)
        ax.plot(t, I, 'r-', alpha=0.2)
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Number Infected')
    ax.set_title('With Superspreaders (10% cause 80% of transmission)')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(ymin=0)
    
    return fig


# ============================================================================
# Demo / Main
# ============================================================================

if __name__ == '__main__':
    print("Chapter 13: Epidemics")
    print("=" * 60)
    
    N = 1000
    beta = 0.3
    gamma = 0.1
    R0 = beta / gamma
    
    print(f"\nParameters:")
    print(f"  Population: N = {N}")
    print(f"  Transmission rate: β = {beta}")
    print(f"  Recovery rate: γ = {gamma}")
    print(f"  R₀ = β/γ = {R0:.2f}")
    
    # Extinction probability
    print(f"\n--- Extinction Probability (Branching Process) ---")
    p_extinct = extinction_probability_branching(R0)
    print(f"  Probability of extinction from single infected: {p_extinct:.3f}")
    
    # Major outbreak probability
    print(f"\n--- Major Outbreak Probability (Simulation) ---")
    for N_test in [100, 500, 1000, 5000]:
        major_frac = major_outbreak_fraction(N_test, beta, gamma, n_runs=100)
        print(f"  N = {N_test:>5}: P(major outbreak) = {major_frac:.1%}")
    
    # R0 sensitivity
    print(f"\n--- Sensitivity to R₀ ---")
    print(f"R₀  | P(major outbreak)")
    print("-" * 30)
    for R0_test in [0.8, 1.0, 1.5, 2.0, 3.0]:
        beta_test = R0_test * gamma
        major_frac = major_outbreak_fraction(N, beta_test, gamma, n_runs=100)
        print(f"{R0_test:.1f} | {major_frac:>6.1%}")
    
    print("\nDone!")
