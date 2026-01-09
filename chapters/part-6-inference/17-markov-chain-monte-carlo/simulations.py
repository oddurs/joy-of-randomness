"""
Chapter 17: Markov Chain Monte Carlo
Sampling from intractable distributions using Metropolis-Hastings and related algorithms.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, multivariate_normal


# ============================================================================
# Metropolis-Hastings Algorithm
# ============================================================================

def metropolis_hastings(log_density, initial_state, proposal_scale, n_iterations):
    """
    Basic Metropolis-Hastings MCMC.
    
    Args:
        log_density: function that returns log π(θ)
        initial_state: starting point (scalar or array)
        proposal_scale: standard deviation of normal proposal
        n_iterations: number of iterations
    
    Returns:
        samples: array of shape (n_iterations, dim)
        acceptance_rate: fraction of proposed moves accepted
    """
    # Initialize
    current = np.asarray(initial_state)
    dim = current.ndim if current.ndim > 0 else 1
    samples = np.zeros((n_iterations, dim))
    accepted = 0
    
    # Evaluate density at initial state
    current_log_density = log_density(current)
    
    for i in range(n_iterations):
        # Propose new state (random walk)
        proposal = current + proposal_scale * np.random.randn(*current.shape)
        proposal_log_density = log_density(proposal)
        
        # Metropolis-Hastings acceptance probability
        log_acceptance_ratio = proposal_log_density - current_log_density
        
        # Accept or reject
        if np.log(np.random.rand()) < log_acceptance_ratio:
            current = proposal
            current_log_density = proposal_log_density
            accepted += 1
        
        samples[i] = current
    
    acceptance_rate = accepted / n_iterations
    return samples, acceptance_rate


def metropolis_hastings_2d(log_density, initial_state, proposal_scale, n_iterations):
    """2D version for visualization."""
    return metropolis_hastings(log_density, initial_state, proposal_scale, n_iterations)


# ============================================================================
# Target Distributions
# ============================================================================

def log_normal_density(x, mean=0, var=1):
    """Log of normal distribution."""
    return -0.5 * (x - mean)**2 / var - 0.5 * np.log(2 * np.pi * var)


def log_mixture_density(x):
    """Log of mixture of two normals (bimodal)."""
    # Mixture: 0.5 * N(-3, 1) + 0.5 * N(3, 1)
    component1 = 0.5 * norm.pdf(x, -3, 1)
    component2 = 0.5 * norm.pdf(x, 3, 1)
    density = component1 + component2
    return np.log(density + 1e-10)  # Add small constant to avoid log(0)


def log_rosenbrock_density(x):
    """
    Log of density on the Rosenbrock surface (challenging 2D target).
    
    Rosenbrock: f(x,y) = (1-x)^2 + 100(y-x^2)^2
    We use exp(-f/T) as the density.
    """
    if len(x) != 2:
        raise ValueError("Rosenbrock density is 2D only")
    x, y = x
    f = (1 - x)**2 + 100 * (y - x**2)**2
    return -f / 10  # Temperature scaling


# ============================================================================
# Gibbs Sampling
# ============================================================================

def gibbs_sampling_2d_gaussian(rho, n_iterations):
    """
    Gibbs sampling for 2D Gaussian with correlation.
    
    Target: bivariate normal with mean 0, variance 1, correlation rho.
    
    Args:
        rho: correlation coefficient
        n_iterations: number of iterations
    
    Returns:
        samples: array of shape (n_iterations, 2)
    """
    samples = np.zeros((n_iterations, 2))
    x, y = 0, 0  # Initial state
    
    for i in range(n_iterations):
        # Gibbs: sample each coordinate from conditional
        # x | y ~ N(rho * y, 1 - rho^2)
        x = np.random.normal(rho * y, np.sqrt(1 - rho**2))
        
        # y | x ~ N(rho * x, 1 - rho^2)
        y = np.random.normal(rho * x, np.sqrt(1 - rho**2))
        
        samples[i] = [x, y]
    
    return samples


# ============================================================================
# Convergence Diagnostics
# ============================================================================

def compute_autocorrelation(samples, max_lag=100):
    """
    Compute autocorrelation of samples.
    
    Args:
        samples: 1D array of samples
        max_lag: maximum lag to compute
    
    Returns:
        acf: autocorrelation as a function of lag
    """
    samples = samples.flatten()
    mean = np.mean(samples)
    c0 = np.var(samples)
    
    acf = np.zeros(max_lag)
    for lag in range(max_lag):
        c_lag = np.mean((samples[:-lag] - mean) * (samples[lag:] - mean)) if lag > 0 else c0
        acf[lag] = c_lag / c0
    
    return acf


def effective_sample_size(samples, max_lag=None):
    """
    Estimate effective sample size accounting for autocorrelation.
    
    ESS ≈ N / (1 + 2 * sum of autocorrelation)
    
    Args:
        samples: 1D array of samples
        max_lag: maximum lag to consider (default: first time ACF < 0.05)
    
    Returns:
        ess: effective sample size
    """
    samples = samples.flatten()
    n = len(samples)
    acf = compute_autocorrelation(samples, max_lag=min(n // 2, 500))
    
    # Sum autocorrelation until it becomes small
    if max_lag is None:
        cutoff = np.where(acf < 0.05)[0]
        max_lag = cutoff[0] if len(cutoff) > 0 else len(acf) // 2
    
    tau = 1 + 2 * np.sum(acf[1:max_lag])  # Integrated autocorrelation time
    ess = n / tau
    
    return ess


def gelman_rubin_diagnostic(chains_list):
    """
    Compute R-hat (Gelman-Rubin diagnostic).
    
    Requires multiple chains. R-hat ≈ 1 indicates convergence.
    
    Args:
        chains_list: list of arrays, each of shape (n_iterations, dim)
    
    Returns:
        r_hat: scalar diagnostic (ideally < 1.05)
    """
    m = len(chains_list)  # Number of chains
    n = chains_list[0].shape[0]  # Iterations per chain
    
    # Chain means
    chain_means = np.array([np.mean(chain, axis=0) for chain in chains_list])
    
    # Overall mean
    overall_mean = np.mean(chain_means, axis=0)
    
    # Between-chain variance
    B = n / (m - 1) * np.sum((chain_means - overall_mean)**2, axis=0)
    
    # Within-chain variance
    W = np.mean([np.var(chain, axis=0, ddof=1) for chain in chains_list], axis=0)
    
    # Estimated variance
    var_hat = ((n - 1) / n) * W + (1 / n) * B
    
    # R-hat
    r_hat = np.sqrt(var_hat / W)
    
    return r_hat


# ============================================================================
# Visualization
# ============================================================================

def plot_mcmc_trace_and_density(samples, burn_in=None, title="MCMC Results"):
    """Plot trace plot and posterior density."""
    if burn_in is None:
        burn_in = len(samples) // 4
    
    samples_post_burnin = samples[burn_in:]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Trace plot
    ax1.plot(samples, alpha=0.7, linewidth=0.5)
    ax1.axvline(burn_in, color='r', linestyle='--', linewidth=2, label=f'Burn-in')
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('θ')
    ax1.set_title(f'{title}: Trace Plot')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Posterior density
    ax2.hist(samples_post_burnin, bins=50, density=True, alpha=0.7, edgecolor='black', label='MCMC samples')
    ax2.set_xlabel('θ')
    ax2.set_ylabel('Density')
    ax2.set_title(f'{title}: Posterior (post burn-in)')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    return fig


def plot_mcmc_2d(samples, burn_in=None, target_name="Target"):
    """Plot 2D MCMC samples as scatter and trace."""
    if burn_in is None:
        burn_in = len(samples) // 4
    
    samples_post_burnin = samples[burn_in:]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Scatter plot
    ax = axes[0, 0]
    ax.scatter(samples_post_burnin[:, 0], samples_post_burnin[:, 1], 
              alpha=0.3, s=1)
    ax.set_xlabel('θ₁')
    ax.set_ylabel('θ₂')
    ax.set_title(f'{target_name}: Posterior Scatter')
    ax.grid(True, alpha=0.3)
    
    # Trace plots
    ax = axes[0, 1]
    ax.plot(samples[:, 0], alpha=0.7, linewidth=0.5)
    ax.axvline(burn_in, color='r', linestyle='--', linewidth=2)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('θ₁')
    ax.set_title('Trace: θ₁')
    ax.grid(True, alpha=0.3)
    
    ax = axes[1, 0]
    ax.plot(samples[:, 1], alpha=0.7, linewidth=0.5)
    ax.axvline(burn_in, color='r', linestyle='--', linewidth=2)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('θ₂')
    ax.set_title('Trace: θ₂')
    ax.grid(True, alpha=0.3)
    
    # Marginal densities
    ax = axes[1, 1]
    ax.hist(samples_post_burnin[:, 0], bins=30, density=True, alpha=0.5, label='θ₁', edgecolor='black')
    ax.hist(samples_post_burnin[:, 1], bins=30, density=True, alpha=0.5, label='θ₂', edgecolor='black')
    ax.set_xlabel('Value')
    ax.set_ylabel('Density')
    ax.set_title('Marginal Posteriors')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    return fig


def plot_proposal_effect(initial_state, log_density, proposal_scales, n_iterations=2000):
    """Compare effect of different proposal scales."""
    fig, axes = plt.subplots(len(proposal_scales), 2, figsize=(12, 3*len(proposal_scales)))
    
    if len(proposal_scales) == 1:
        axes = axes.reshape(1, -1)
    
    for idx, scale in enumerate(proposal_scales):
        samples, acc_rate = metropolis_hastings(log_density, initial_state, scale, n_iterations)
        
        # Trace plot
        ax = axes[idx, 0]
        ax.plot(samples, alpha=0.7, linewidth=0.5)
        ax.set_ylabel('θ')
        ax.set_title(f'Scale={scale:.3f}, Acceptance={acc_rate:.1%}')
        ax.grid(True, alpha=0.3)
        
        # Histogram
        ax = axes[idx, 1]
        ax.hist(samples[500:], bins=40, density=True, alpha=0.7, edgecolor='black')
        ax.set_ylabel('Density')
        ax.set_title(f'Posterior (post burn-in)')
        ax.grid(True, alpha=0.3, axis='y')
    
    axes[-1, 0].set_xlabel('Iteration')
    axes[-1, 1].set_xlabel('θ')
    
    return fig


def plot_autocorrelation(samples, max_lag=100):
    """Plot autocorrelation function."""
    acf = compute_autocorrelation(samples.flatten(), max_lag)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.stem(range(len(acf)), acf, basefmt=' ')
    ax.axhline(0, color='k', linewidth=0.5)
    ax.axhline(0.05, color='r', linestyle='--', alpha=0.5, label='Significance threshold')
    ax.set_xlabel('Lag')
    ax.set_ylabel('Autocorrelation')
    ax.set_title('Autocorrelation Function')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig


# ============================================================================
# Demo / Main
# ============================================================================

if __name__ == '__main__':
    print("Chapter 17: Markov Chain Monte Carlo")
    print("=" * 60)
    
    # Example 1: Simple normal distribution
    print("\n--- Example 1: Standard Normal ---")
    
    def log_density_normal(x):
        return log_normal_density(x, mean=0, var=1)
    
    samples, acc_rate = metropolis_hastings(log_density_normal, 0, proposal_scale=0.5, n_iterations=5000)
    
    print(f"  Acceptance rate: {acc_rate:.1%}")
    print(f"  Mean: {np.mean(samples[1000:]):.3f} (expected 0)")
    print(f"  Std dev: {np.std(samples[1000:]):.3f} (expected 1)")
    print(f"  Effective sample size: {effective_sample_size(samples[1000:]):.0f}")
    
    # Example 2: Bimodal distribution
    print("\n--- Example 2: Bimodal Mixture ---")
    
    samples_bimodal, acc_rate_bimodal = metropolis_hastings(
        log_mixture_density, 0, proposal_scale=1.0, n_iterations=10000
    )
    
    print(f"  Acceptance rate: {acc_rate_bimodal:.1%}")
    print(f"  ESS: {effective_sample_size(samples_bimodal[1000:]):.0f}")
    
    # Example 3: Gibbs sampling
    print("\n--- Example 3: Gibbs Sampling (2D Gaussian) ---")
    
    samples_gibbs = gibbs_sampling_2d_gaussian(rho=0.8, n_iterations=5000)
    
    print(f"  Correlation (true): 0.8")
    print(f"  Correlation (samples): {np.corrcoef(samples_gibbs[1000:].T)[0, 1]:.3f}")
    
    print("\nDone!")
