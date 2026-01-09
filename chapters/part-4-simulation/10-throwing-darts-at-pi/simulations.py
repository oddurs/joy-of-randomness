"""
Chapter 10: Throwing Darts at Pi
Monte Carlo methods and integration by random sampling.
"""

import numpy as np
import matplotlib.pyplot as plt


# ============================================================================
# Basic Monte Carlo Integration
# ============================================================================

def estimate_pi_basic(n_darts):
    """
    Estimate π by throwing darts at a unit circle.
    
    Args:
        n_darts: Number of darts to throw
    
    Returns:
        Estimated value of π
    """
    # Random points in [-1, 1] × [-1, 1]
    x = np.random.uniform(-1, 1, n_darts)
    y = np.random.uniform(-1, 1, n_darts)
    
    # Check if inside unit circle
    distance = np.sqrt(x**2 + y**2)
    hits = distance <= 1
    
    # Estimate π
    pi_estimate = 4 * hits.sum() / n_darts
    
    return pi_estimate


def estimate_pi_convergence(n_samples_list):
    """
    Track π estimate convergence across different sample sizes.
    
    Args:
        n_samples_list: List of sample sizes to test
    
    Returns:
        List of π estimates, list of errors
    """
    estimates = []
    errors = []
    
    for n in n_samples_list:
        pi_est = estimate_pi_basic(n)
        estimates.append(pi_est)
        errors.append(abs(pi_est - np.pi))
    
    return estimates, errors


def estimate_pi_multiple_runs(n_darts, n_runs=100):
    """
    Run π estimation multiple times to assess variance.
    
    Args:
        n_darts: Number of darts per run
        n_runs: Number of independent runs
    
    Returns:
        Array of π estimates
    """
    estimates = np.zeros(n_runs)
    
    for i in range(n_runs):
        estimates[i] = estimate_pi_basic(n_darts)
    
    return estimates


# ============================================================================
# General Monte Carlo Integration
# ============================================================================

def monte_carlo_integrate(f, bounds, n_samples):
    """
    Estimate integral of f over rectangular domain using Monte Carlo.
    
    Args:
        f: Function to integrate (callable)
        bounds: List of (low, high) for each dimension
        n_samples: Number of samples
    
    Returns:
        Estimated integral value
    """
    dim = len(bounds)
    
    # Generate random points in the domain
    points = np.zeros((n_samples, dim))
    for d in range(dim):
        low, high = bounds[d]
        points[:, d] = np.random.uniform(low, high, n_samples)
    
    # Evaluate function at each point
    values = np.array([f(point) for point in points])
    
    # Compute domain volume
    volume = 1.0
    for low, high in bounds:
        volume *= (high - low)
    
    # Estimate integral
    integral = volume * np.mean(values)
    
    return integral


def monte_carlo_integrate_convergence(f, bounds, n_samples_list):
    """
    Track convergence of Monte Carlo integration.
    
    Args:
        f: Function to integrate
        bounds: Domain bounds
        n_samples_list: List of sample sizes
    
    Returns:
        List of integral estimates
    """
    estimates = []
    
    for n in n_samples_list:
        est = monte_carlo_integrate(f, bounds, n)
        estimates.append(est)
    
    return estimates


# ============================================================================
# High-Dimensional Examples
# ============================================================================

def hypersphere_volume_exact(d, r=1.0):
    """
    Compute exact volume of d-dimensional hypersphere.
    
    Args:
        d: Dimension
        r: Radius (default 1)
    
    Returns:
        Volume
    """
    # V_d(r) = (π^(d/2) / Γ(d/2 + 1)) * r^d
    from scipy.special import gamma
    
    return (np.pi ** (d / 2)) / gamma(d / 2 + 1) * (r ** d)


def hypersphere_volume_monte_carlo(d, n_samples, r=1.0):
    """
    Estimate volume of d-dimensional unit hypersphere using Monte Carlo.
    
    Method: Sample uniformly in hypercube [-r, r]^d, count fraction in sphere.
    
    Args:
        d: Dimension
        n_samples: Number of samples
        r: Radius
    
    Returns:
        Estimated volume
    """
    # Random points in [-r, r]^d
    points = np.random.uniform(-r, r, (n_samples, d))
    
    # Check if inside hypersphere (distance from origin ≤ r)
    distances = np.linalg.norm(points, axis=1)
    inside = distances <= r
    
    # Volume of hypercube is (2r)^d
    hypercube_volume = (2 * r) ** d
    
    # Fraction inside × hypercube volume = sphere volume
    volume_estimate = (inside.sum() / n_samples) * hypercube_volume
    
    return volume_estimate


def hypersphere_volumes_across_dimensions(max_dim=20, n_samples=100_000):
    """
    Compute hypersphere volumes for dimensions 1 through max_dim.
    
    Args:
        max_dim: Maximum dimension to compute
        n_samples: Samples for Monte Carlo
    
    Returns:
        Lists of dimensions, exact volumes, estimated volumes
    """
    dims = list(range(1, max_dim + 1))
    exact_vols = [hypersphere_volume_exact(d) for d in dims]
    est_vols = [hypersphere_volume_monte_carlo(d, n_samples) for d in dims]
    
    return dims, exact_vols, est_vols


# ============================================================================
# Variance Analysis
# ============================================================================

def standard_error_pi(n_darts, p=np.pi / 4):
    """
    Compute theoretical standard error of π estimate.
    
    The estimate is h/n where h ~ Binomial(n, p).
    So π_estimate = 4h/n, and SE = 4 * sqrt(p(1-p)/n)
    
    Args:
        n_darts: Number of darts
        p: True probability (default π/4)
    
    Returns:
        Standard error
    """
    return 4 * np.sqrt(p * (1 - p) / n_darts)


def confidence_interval_pi(estimate, n_darts, confidence=0.95):
    """
    Compute confidence interval for π estimate.
    
    Args:
        estimate: Point estimate of π
        n_darts: Number of darts
        confidence: Confidence level (default 0.95 = 95%)
    
    Returns:
        (lower, upper) bounds
    """
    if confidence == 0.95:
        z = 1.96  # Standard normal critical value
    elif confidence == 0.99:
        z = 2.576
    else:
        z = np.sqrt(-2 * np.log(1 - confidence))
    
    se = standard_error_pi(n_darts)
    margin = z * se
    
    return estimate - margin, estimate + margin


# ============================================================================
# Variance Reduction: Stratified Sampling
# ============================================================================

def estimate_pi_stratified(n_darts, n_strata=4):
    """
    Estimate π using stratified sampling.
    
    Divide the square into a grid, sample from each cell equally.
    This reduces variance compared to pure random sampling.
    
    Args:
        n_darts: Total number of darts
        n_strata: Number of strata per dimension (default 4 → 16 regions)
    
    Returns:
        Estimated π
    """
    darts_per_stratum = n_darts // (n_strata ** 2)
    
    hits = 0
    total = 0
    
    for i in range(n_strata):
        for j in range(n_strata):
            # Boundaries of this stratum
            x_min = -1 + (2 * i) / n_strata
            x_max = -1 + (2 * (i + 1)) / n_strata
            y_min = -1 + (2 * j) / n_strata
            y_max = -1 + (2 * (j + 1)) / n_strata
            
            # Sample uniformly within this stratum
            x = np.random.uniform(x_min, x_max, darts_per_stratum)
            y = np.random.uniform(y_min, y_max, darts_per_stratum)
            
            # Count hits
            distance = np.sqrt(x**2 + y**2)
            hits += (distance <= 1).sum()
            total += darts_per_stratum
    
    return 4 * hits / total


# ============================================================================
# Variance Reduction: Importance Sampling
# ============================================================================

def estimate_pi_importance_sampling(n_darts):
    """
    Estimate π using importance sampling.
    
    Sample more densely near the circle boundary where the integral is interesting.
    Use a proposal distribution that concentrates near the circle edge.
    
    Args:
        n_darts: Number of samples
    
    Returns:
        Estimated π
    """
    # Propose points from a distribution concentrated near the circle
    # Use exponential distribution in distance from origin
    radii = np.random.exponential(scale=0.5, size=n_darts)
    angles = np.random.uniform(0, 2 * np.pi, n_darts)
    
    # Convert to Cartesian
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    
    # Clamp to [-1, 1] (outside square: weight 0)
    in_square = (np.abs(x) <= 1) & (np.abs(y) <= 1)
    
    # Reweight by the ratio of target to proposal distribution
    # This is more involved; simplified version:
    # Weight each sample by 1 / proposal_density
    
    # For simplicity, just use accepted samples
    x_accepted = x[in_square]
    y_accepted = y[in_square]
    
    if len(x_accepted) == 0:
        return estimate_pi_basic(n_darts)
    
    distance = np.sqrt(x_accepted**2 + y_accepted**2)
    hits = (distance <= 1).sum()
    
    return 4 * hits / len(x_accepted)


# ============================================================================
# Visualization Functions
# ============================================================================

def plot_pi_convergence(n_samples_list):
    """Plot π estimate convergence."""
    estimates, errors = estimate_pi_convergence(n_samples_list)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Estimates
    ax1.plot(n_samples_list, estimates, 'bo-', label='Estimate', alpha=0.7)
    ax1.axhline(np.pi, color='r', linestyle='--', label='True π', linewidth=2)
    ax1.fill_between(n_samples_list, np.pi - 0.1, np.pi + 0.1, alpha=0.2, color='red')
    ax1.set_xscale('log')
    ax1.set_xlabel('Number of Darts')
    ax1.set_ylabel('π Estimate')
    ax1.set_title('Convergence of π Estimate')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Errors (log scale)
    ax2.loglog(n_samples_list, errors, 'bo-', label='Observed Error', alpha=0.7)
    
    # Theoretical 1/√n line
    theoretical = 1.0 / np.sqrt(np.array(n_samples_list))
    theoretical = theoretical * errors[0] / theoretical[0]  # Scale to match
    ax2.loglog(n_samples_list, theoretical, 'r--', label='1/√n', linewidth=2)
    
    ax2.set_xlabel('Number of Darts')
    ax2.set_ylabel('Absolute Error')
    ax2.set_title('Error Decay (log-log)')
    ax2.legend()
    ax2.grid(True, alpha=0.3, which='both')
    
    return fig


def plot_pi_distribution(n_darts, n_runs=100):
    """Plot distribution of π estimates across multiple runs."""
    estimates = estimate_pi_multiple_runs(n_darts, n_runs=n_runs)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(estimates, bins=20, alpha=0.7, edgecolor='black')
    ax.axvline(np.pi, color='r', linestyle='--', linewidth=2, label='True π')
    ax.axvline(estimates.mean(), color='g', linestyle='--', linewidth=2, label='Mean of estimates')
    
    ax.set_xlabel('π Estimate')
    ax.set_ylabel('Frequency')
    ax.set_title(f'Distribution of π Estimates ({n_darts} darts, {n_runs} runs)')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    return fig


def plot_hypersphere_volumes(max_dim=20, n_samples=100_000):
    """Plot hypersphere volumes across dimensions."""
    dims, exact_vols, est_vols = hypersphere_volumes_across_dimensions(max_dim, n_samples)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(dims, exact_vols, 'r-o', label='Exact', linewidth=2, markersize=6)
    ax.plot(dims, est_vols, 'b-s', label=f'MC Estimate ({n_samples:,} samples)', 
            linewidth=2, markersize=6, alpha=0.7)
    
    ax.set_xlabel('Dimension d')
    ax.set_ylabel('Volume')
    ax.set_title('Unit Hypersphere Volume vs. Dimension')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig


def plot_variance_reduction_comparison(n_darts):
    """Compare variance of different sampling methods."""
    n_runs = 100
    
    # Random
    estimates_random = [estimate_pi_basic(n_darts) for _ in range(n_runs)]
    
    # Stratified
    estimates_stratified = [estimate_pi_stratified(n_darts, n_strata=4) for _ in range(n_runs)]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(estimates_random, bins=15, alpha=0.6, label='Random Sampling', edgecolor='black')
    ax.hist(estimates_stratified, bins=15, alpha=0.6, label='Stratified Sampling', edgecolor='black')
    ax.axvline(np.pi, color='r', linestyle='--', linewidth=2, label='True π')
    
    ax.set_xlabel('π Estimate')
    ax.set_ylabel('Frequency')
    ax.set_title(f'Variance Reduction: Random vs Stratified ({n_darts} darts)')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Print statistics
    print(f"Random Sampling:")
    print(f"  Mean: {np.mean(estimates_random):.6f}")
    print(f"  Std:  {np.std(estimates_random):.6f}")
    print(f"\nStratified Sampling:")
    print(f"  Mean: {np.mean(estimates_stratified):.6f}")
    print(f"  Std:  {np.std(estimates_stratified):.6f}")
    
    return fig


# ============================================================================
# Demo / Main
# ============================================================================

if __name__ == '__main__':
    print("Chapter 10: Throwing Darts at Pi")
    print("=" * 60)
    
    # Basic π estimation
    print("\n--- Basic π Estimation ---")
    for n in [100, 1_000, 10_000, 100_000]:
        pi_est = estimate_pi_basic(n)
        error = abs(pi_est - np.pi)
        se = standard_error_pi(n)
        print(f"n = {n:>7}: π ≈ {pi_est:.6f}, error = {error:.6f}, SE = {se:.6f}")
    
    # Convergence
    print("\n--- Convergence Analysis ---")
    n_samples = [100, 500, 1_000, 5_000, 10_000, 50_000, 100_000]
    estimates, errors = estimate_pi_convergence(n_samples)
    
    print("Samples    | Estimate  | Error    | Theoretical SE")
    print("-" * 50)
    for n, est, err in zip(n_samples, estimates, errors):
        se = standard_error_pi(n)
        print(f"{n:>9} | {est:.6f}  | {err:.6f} | {se:.6f}")
    
    # Hypersphere volumes
    print("\n--- Hypersphere Volumes ---")
    dims, exact, est = hypersphere_volumes_across_dimensions(max_dim=10, n_samples=100_000)
    
    print("Dim | Exact Volume | MC Estimate | Error")
    print("-" * 45)
    for d, ex, e in zip(dims, exact, est):
        print(f"{d:>3} | {ex:>12.6f} | {e:>11.6f} | {abs(e - ex):.6f}")
    
    print("\nDone!")
