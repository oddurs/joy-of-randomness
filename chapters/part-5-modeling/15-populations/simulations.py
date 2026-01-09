"""
Chapter 15: Populations
Birth-death processes, extinction probability, and stochastic population models.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


# ============================================================================
# Birth-Death Process
# ============================================================================

def simulate_birth_death(n0, lambda_birth, mu_death, t_max):
    """
    Simulate a discrete-time birth-death process.
    
    Args:
        n0: initial population size
        lambda_birth: birth rate per individual per time unit
        mu_death: death rate per individual per time unit
        t_max: maximum time
    
    Returns:
        times, populations: arrays of (time, population size)
    """
    n = n0
    time = 0
    times = [0]
    pops = [n]
    
    while time < t_max and n > 0:
        # Each individual may reproduce
        births = np.random.binomial(n, lambda_birth)
        
        # Each individual may die
        deaths = np.random.binomial(n, mu_death)
        
        # Update population
        n = n + births - deaths
        
        # Advance time
        time += 1
        times.append(time)
        pops.append(n)
    
    return np.array(times), np.array(pops)


def simulate_birth_death_many_runs(n0, lambda_birth, mu_death, t_max, n_runs=100):
    """
    Run birth-death process many times.
    
    Args:
        n0: initial population size
        lambda_birth: birth rate
        mu_death: death rate
        t_max: maximum time
        n_runs: number of simulations
    
    Returns:
        List of (times, pops) for each run
    """
    runs = []
    for _ in range(n_runs):
        result = simulate_birth_death(n0, lambda_birth, mu_death, t_max)
        runs.append(result)
    return runs


# ============================================================================
# Extinction Probability
# ============================================================================

def compute_extinction_probability(n0, lambda_birth, mu_death, t_max, n_runs=100):
    """
    Estimate extinction probability by simulation.
    
    Args:
        n0: initial population size
        lambda_birth: birth rate
        mu_death: death rate
        t_max: maximum time
        n_runs: number of simulations
    
    Returns:
        Fraction of runs that go extinct
    """
    runs = simulate_birth_death_many_runs(n0, lambda_birth, mu_death, t_max, n_runs)
    
    extinct = 0
    for times, pops in runs:
        if pops[-1] == 0:
            extinct += 1
    
    return extinct / n_runs


def theoretical_extinction_probability(n0, lambda_birth, mu_death):
    """
    Theoretical extinction probability for branching process.
    
    If lambda > mu, extinction probability = (mu / lambda)^n0
    
    Args:
        n0: initial population size
        lambda_birth: birth rate per individual
        mu_death: death rate per individual
    
    Returns:
        Extinction probability
    """
    if lambda_birth <= mu_death:
        return 1.0
    else:
        rho = mu_death / lambda_birth
        return rho ** n0


# ============================================================================
# Density-Dependent Population Model
# ============================================================================

def simulate_logistic_birth_death(n0, r, K, env_noise=0, t_max=100):
    """
    Simulate population with density dependence and logistic growth.
    
    Birth rate decreases, death rate increases as population approaches carrying capacity K.
    
    Args:
        n0: initial population size
        r: intrinsic growth rate
        K: carrying capacity
        env_noise: environmental noise (std dev of per-capita growth)
        t_max: maximum time
    
    Returns:
        times, populations
    """
    n = n0
    times = [0]
    pops = [n]
    
    for t in range(1, t_max + 1):
        if n <= 0:
            break
        
        # Logistic growth: per-capita growth rate decreases as n approaches K
        growth_rate = r * (1 - n / K)
        
        # Add environmental noise
        if env_noise > 0:
            growth_rate += np.random.normal(0, env_noise)
        
        # Births
        lambda_t = max(0, growth_rate / 2)  # Half of growth is births
        births = np.random.binomial(n, lambda_t)
        
        # Deaths
        mu_t = max(0, -growth_rate / 2) if growth_rate < 0 else 0
        deaths = np.random.binomial(n, mu_t)
        
        # Update population
        n = n + births - deaths
        
        times.append(t)
        pops.append(max(0, n))
    
    return np.array(times), np.array(pops)


# ============================================================================
# Allee Effect
# ============================================================================

def simulate_allee_effect(n0, lambda_max, mu_min, n_critical, t_max=100):
    """
    Simulate population with Allee effect.
    
    When population is very small (< n_critical), birth rate drops and death rate rises.
    
    Args:
        n0: initial population size
        lambda_max: maximum birth rate (when n >> n_critical)
        mu_min: minimum death rate (when n >> n_critical)
        n_critical: critical population size for Allee effect
        t_max: maximum time
    
    Returns:
        times, populations
    """
    n = n0
    times = [0]
    pops = [n]
    
    for t in range(1, t_max + 1):
        if n <= 0:
            break
        
        # Birth rate decreases when n < n_critical
        if n < n_critical:
            lambda_t = lambda_max * (n / n_critical)  # Linearly decrease
        else:
            lambda_t = lambda_max
        
        # Death rate increases when n < n_critical
        if n < n_critical:
            mu_t = mu_min + (0.5 - mu_min) * (1 - n / n_critical)
        else:
            mu_t = mu_min
        
        # Births and deaths
        births = np.random.binomial(n, lambda_t)
        deaths = np.random.binomial(n, mu_t)
        
        # Update
        n = n + births - deaths
        
        times.append(t)
        pops.append(max(0, n))
    
    return np.array(times), np.array(pops)


# ============================================================================
# Metapopulation Model
# ============================================================================

def simulate_metapopulation(n_patches, n0_per_patch, lambda_birth, mu_death, 
                            migration_rate, t_max=100):
    """
    Simulate a metapopulation: multiple patches with local dynamics and migration.
    
    Args:
        n_patches: number of patches
        n0_per_patch: initial population per patch
        lambda_birth: birth rate per individual
        mu_death: death rate per individual
        migration_rate: probability of migrating to another patch
        t_max: maximum time
    
    Returns:
        times, populations (n_patches populations over time)
    """
    populations = np.ones((n_patches,)) * n0_per_patch
    times = [0]
    history = [populations.copy()]
    
    for t in range(1, t_max + 1):
        # Local dynamics in each patch
        for i in range(n_patches):
            if populations[i] > 0:
                births = np.random.binomial(int(populations[i]), lambda_birth)
                deaths = np.random.binomial(int(populations[i]), mu_death)
                populations[i] = populations[i] + births - deaths
        
        # Migration: individuals move between patches
        for i in range(n_patches):
            migrants = np.random.binomial(int(populations[i]), migration_rate)
            if migrants > 0:
                populations[i] -= migrants
                # Distribute to random other patches
                dest_patch = np.random.randint(0, n_patches)
                populations[dest_patch] += migrants
        
        # Ensure non-negative
        populations = np.maximum(populations, 0)
        
        times.append(t)
        history.append(populations.copy())
    
    history = np.array(history)
    return np.array(times), history


# ============================================================================
# Visualization
# ============================================================================

def plot_population_trajectories(n0, lambda_birth, mu_death, t_max=100, n_runs=50):
    """Plot many population trajectories."""
    runs = simulate_birth_death_many_runs(n0, lambda_birth, mu_death, t_max, n_runs)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for times, pops in runs:
        ax.plot(times, pops, 'b-', alpha=0.2, linewidth=0.8)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Population Size')
    ax.set_title(f'Population Trajectories (λ={lambda_birth}, μ={mu_death}, n₀={n0})')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(ymin=0)
    
    return fig


def plot_extinction_probability_vs_initial_population(lambda_birth, mu_death, t_max=100):
    """Plot extinction probability as a function of initial population size."""
    n0_values = [1, 2, 5, 10, 20, 50, 100]
    extinction_probs = []
    
    for n0 in n0_values:
        p_extinct = compute_extinction_probability(n0, lambda_birth, mu_death, t_max, n_runs=100)
        extinction_probs.append(p_extinct)
    
    # Theoretical
    theory_probs = [theoretical_extinction_probability(n0, lambda_birth, mu_death) for n0 in n0_values]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.semilogy(n0_values, extinction_probs, 'bo-', label='Simulation', markersize=8, linewidth=2)
    ax.semilogy(n0_values, theory_probs, 'r^--', label='Theory (μ/λ)^n', markersize=8, linewidth=2)
    
    ax.set_xlabel('Initial Population Size (n₀)')
    ax.set_ylabel('Extinction Probability')
    ax.set_title(f'Extinction vs. Initial Population (λ={lambda_birth}, μ={mu_death})')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')
    
    return fig


def plot_density_dependent_vs_independent(n0, r, K, t_max=100):
    """Compare density-independent and density-dependent models."""
    # Density-independent (exponential)
    times_ind, pops_ind = simulate_birth_death(n0, r/2, (r/2 - r/10), t_max)
    
    # Density-dependent (logistic)
    times_dep, pops_dep = simulate_logistic_birth_death(n0, r, K, t_max=t_max)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Run multiple times for density-dependent
    for _ in range(20):
        times, pops = simulate_logistic_birth_death(n0, r, K, t_max=t_max)
        ax1.plot(times, pops, 'g-', alpha=0.2)
    
    ax1.axhline(K, color='r', linestyle='--', linewidth=2, label=f'Carrying capacity K={K}')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Population Size')
    ax1.set_title('Density-Dependent Growth (with carrying capacity)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(ymin=0)
    
    # Compare final populations
    runs_ind = simulate_birth_death_many_runs(n0, r/2, (r/2 - r/10), t_max, n_runs=50)
    runs_dep = [simulate_logistic_birth_death(n0, r, K, t_max=t_max) for _ in range(50)]
    
    final_ind = [pops[-1] for _, pops in runs_ind if len(pops) > 0]
    final_dep = [pops[-1] for _, pops in runs_dep if len(pops) > 0]
    
    ax2.hist(final_ind, bins=20, alpha=0.6, label='Density-independent (exponential)', edgecolor='black')
    ax2.hist(final_dep, bins=20, alpha=0.6, label='Density-dependent (logistic)', edgecolor='black')
    ax2.set_xlabel('Final Population Size')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Final Population Distribution')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    return fig


def plot_allee_effect(n0, t_max=100):
    """Compare populations with and without Allee effect."""
    # Without Allee effect
    times_no, pops_no = simulate_birth_death(n0, 0.6, 0.4, t_max)
    
    # With Allee effect
    times_allee, pops_allee = simulate_allee_effect(n0, 0.6, 0.4, n_critical=10, t_max=t_max)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Multiple trajectories without Allee
    for _ in range(30):
        times, pops = simulate_birth_death(n0, 0.6, 0.4, t_max)
        ax1.plot(times, pops, 'b-', alpha=0.2, linewidth=0.8)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Population Size')
    ax1.set_title('Without Allee Effect')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(ymin=0)
    
    # Multiple trajectories with Allee
    for _ in range(30):
        times, pops = simulate_allee_effect(n0, 0.6, 0.4, n_critical=10, t_max=t_max)
        ax2.plot(times, pops, 'r-', alpha=0.2, linewidth=0.8)
    ax2.axvline(10, color='k', linestyle='--', alpha=0.5, label='Critical size = 10')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Population Size')
    ax2.set_title('With Allee Effect')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(ymin=0)
    
    return fig


def plot_metapopulation_dynamics(n_patches=5, t_max=100):
    """Plot metapopulation dynamics."""
    times, history = simulate_metapopulation(n_patches, 20, 0.6, 0.4, 
                                            migration_rate=0.05, t_max=t_max)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot each patch
    for i in range(n_patches):
        ax1.plot(times, history[:, i], label=f'Patch {i+1}', linewidth=2)
    
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Population Size')
    ax1.set_title('Metapopulation: Individual Patches')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(ymin=0)
    
    # Total metapopulation
    total_pop = history.sum(axis=1)
    ax2.plot(times, total_pop, 'k-', linewidth=2)
    ax2.fill_between(times, 0, total_pop, alpha=0.3)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Total Population (all patches)')
    ax2.set_title('Metapopulation: Total Abundance')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(ymin=0)
    
    return fig


# ============================================================================
# Demo / Main
# ============================================================================

if __name__ == '__main__':
    print("Chapter 15: Populations")
    print("=" * 60)
    
    n0 = 5
    lambda_birth = 1.2
    mu_death = 1.0
    t_max = 100
    
    print(f"\nParameters:")
    print(f"  Initial population: n₀ = {n0}")
    print(f"  Birth rate: λ = {lambda_birth}")
    print(f"  Death rate: μ = {mu_death}")
    print(f"  Net growth rate: λ - μ = {lambda_birth - mu_death}")
    
    # Extinction probability
    print(f"\n--- Extinction Probability ---")
    p_extinct_theory = theoretical_extinction_probability(n0, lambda_birth, mu_death)
    p_extinct_sim = compute_extinction_probability(n0, lambda_birth, mu_death, t_max, n_runs=100)
    
    print(f"  Theory: p(extinction) = (μ/λ)^n = {p_extinct_theory:.3f}")
    print(f"  Simulation (100 runs): {p_extinct_sim:.1%}")
    
    # Vary initial population
    print(f"\n--- Extinction vs. Initial Population Size ---")
    print(f"n₀ | p(extinction) | Interpretation")
    print("-" * 50)
    for n in [1, 5, 10, 20, 50]:
        p = theoretical_extinction_probability(n, lambda_birth, mu_death)
        print(f"{n:>2} | {p:>13.1%} | {'Likely' if p > 0.5 else 'Unlikely'}")
    
    # Density dependence
    print(f"\n--- Density-Dependent Model (Logistic) ---")
    r = 0.5
    K = 100
    print(f"  Intrinsic growth rate: r = {r}")
    print(f"  Carrying capacity: K = {K}")
    
    # Run several times
    extinctions = 0
    for _ in range(100):
        times, pops = simulate_logistic_birth_death(n0, r, K, t_max=t_max)
        if pops[-1] == 0:
            extinctions += 1
    
    print(f"  Extinction probability: {extinctions / 100:.1%}")
    
    print("\nDone!")
