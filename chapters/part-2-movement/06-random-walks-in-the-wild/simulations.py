"""
Chapter 6: Random Walks in the Wild
Simulations and utilities for exploring real-world movement patterns:
- Animal movement tracks
- Lévy flights and power-law step distributions
- Correlated random walks
- Step-length analysis and power-law fitting
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import ks_2samp
import warnings
warnings.filterwarnings('ignore')


# ============================================================================
# Core Simulation Functions
# ============================================================================

def simulate_ideal_random_walk_2d(num_steps, fixed_step_size=1.0):
    """
    Standard 2D random walk with fixed step sizes.
    
    Args:
        num_steps: Number of steps to simulate
        fixed_step_size: Length of each step (default 1.0)
    
    Returns:
        x, y: Arrays of x and y positions
    """
    x, y = [0.0], [0.0]
    
    for _ in range(num_steps):
        angle = np.random.uniform(0, 2 * np.pi)
        dx = fixed_step_size * np.cos(angle)
        dy = fixed_step_size * np.sin(angle)
        x.append(x[-1] + dx)
        y.append(y[-1] + dy)
    
    return np.array(x), np.array(y)


def simulate_levy_flight_2d(num_steps, alpha=1.5, x_min=1.0):
    """
    2D random walk with power-law distributed step sizes (Lévy flight).
    
    Args:
        num_steps: Number of steps
        alpha: Power-law exponent (1 < alpha < 3, typically)
        x_min: Minimum step size (scales the distribution)
    
    Returns:
        x, y: Arrays of positions
    """
    x, y = [0.0], [0.0]
    
    for _ in range(num_steps):
        # Power-law: use Pareto distribution (P(s > x) ~ x^{-alpha})
        step_size = np.random.pareto(a=alpha) + x_min
        angle = np.random.uniform(0, 2 * np.pi)
        x.append(x[-1] + step_size * np.cos(angle))
        y.append(y[-1] + step_size * np.sin(angle))
    
    return np.array(x), np.array(y)


def simulate_correlated_random_walk_2d(num_steps, step_dist='exponential', 
                                       persistence=0.3, x_mean=1.0):
    """
    2D random walk with directional persistence and variable step sizes.
    
    Args:
        num_steps: Number of steps
        step_dist: 'exponential' or 'power_law' for step size distribution
        persistence: Standard deviation of angle change (higher = more persistent)
        x_mean: Mean step size
    
    Returns:
        x, y: Arrays of positions
    """
    x, y = [0.0], [0.0]
    angle = np.random.uniform(0, 2 * np.pi)
    
    for _ in range(num_steps):
        # Direction persists with Gaussian perturbation
        angle += np.random.normal(loc=0, scale=persistence)
        
        # Variable step sizes
        if step_dist == 'exponential':
            step_size = np.random.exponential(scale=x_mean)
        elif step_dist == 'power_law':
            step_size = (np.random.pareto(a=1.5) + 1) * x_mean
        else:
            step_size = np.random.exponential(scale=x_mean)
        
        x.append(x[-1] + step_size * np.cos(angle))
        y.append(y[-1] + step_size * np.sin(angle))
    
    return np.array(x), np.array(y)


def simulate_realistic_animal_track(num_steps, species='default'):
    """
    Simulate realistic animal movement with species-specific parameters.
    
    Args:
        num_steps: Number of steps
        species: 'albatross', 'turtle', 'bacterium', or 'default'
    
    Returns:
        x, y: Arrays of positions
    """
    # Set parameters by species (tuned to roughly match real behaviors)
    params = {
        'albatross': {'persistence': 0.2, 'step_dist': 'power_law', 'alpha': 1.6},
        'turtle': {'persistence': 0.25, 'step_dist': 'power_law', 'alpha': 1.7},
        'bacterium': {'persistence': 0.1, 'step_dist': 'exponential', 'alpha': 2.0},
        'default': {'persistence': 0.3, 'step_dist': 'exponential', 'alpha': 2.0}
    }
    
    p = params.get(species, params['default'])
    x, y = [0.0], [0.0]
    angle = np.random.uniform(0, 2 * np.pi)
    
    for _ in range(num_steps):
        angle += np.random.normal(loc=0, scale=p['persistence'])
        
        if p['step_dist'] == 'power_law':
            step_size = (np.random.pareto(a=p['alpha']) + 1) * 0.5
        else:
            step_size = np.random.exponential(scale=0.5)
        
        x.append(x[-1] + step_size * np.cos(angle))
        y.append(y[-1] + step_size * np.sin(angle))
    
    return np.array(x), np.array(y)


# ============================================================================
# Step Length Analysis Functions
# ============================================================================

def extract_step_lengths(x, y):
    """Extract distances between consecutive positions."""
    dx = np.diff(x)
    dy = np.diff(y)
    return np.sqrt(dx**2 + dy**2)


def fit_power_law_exponent(steps, x_min=None, method='mle'):
    """
    Estimate power-law exponent from step length data.
    
    For P(s > x) ~ x^{-alpha}, the MLE is:
    alpha = 1 + n / sum(log(s_i / s_min))
    
    Args:
        steps: Array of step lengths
        x_min: Minimum step size (if None, uses min of data)
        method: 'mle' or 'linfit'
    
    Returns:
        alpha: Estimated exponent
    """
    if x_min is None:
        x_min = np.min(steps[steps > 0])
    
    steps_above = steps[steps > x_min]
    
    if len(steps_above) < 10:
        return None
    
    if method == 'mle':
        alpha = 1 + len(steps_above) / np.sum(np.log(steps_above / x_min))
    else:
        # Log-log linear fit
        sorted_steps = np.sort(steps_above)
        ccdf = 1 - np.arange(len(sorted_steps)) / len(sorted_steps)
        log_steps = np.log(sorted_steps)
        log_ccdf = np.log(ccdf)
        alpha = -np.polyfit(log_steps, log_ccdf, 1)[0]
    
    return alpha


def compare_distributions(steps_a, steps_b, n_bins=50):
    """
    Statistically compare two step-length distributions.
    
    Returns:
        ks_statistic, p_value: Kolmogorov-Smirnov test results
    """
    return ks_2samp(steps_a, steps_b)


# ============================================================================
# Analysis Functions
# ============================================================================

def analyze_path_geometry(x, y):
    """
    Compute summary statistics of a path.
    
    Returns dictionary with:
    - final_distance: Distance from start to end
    - max_distance: Maximum distance from origin
    - path_length: Total path length
    - displacement_ratio: Final distance / path length
    """
    final_distance = np.sqrt(x[-1]**2 + y[-1]**2)
    distances = np.sqrt(x**2 + y**2)
    max_distance = np.max(distances)
    
    steps = extract_step_lengths(x, y)
    path_length = np.sum(steps)
    
    displacement_ratio = final_distance / path_length if path_length > 0 else 0
    
    return {
        'final_distance': final_distance,
        'max_distance': max_distance,
        'path_length': path_length,
        'displacement_ratio': displacement_ratio,
        'num_steps': len(x) - 1
    }


def compare_walk_types(num_steps=5000, num_replicates=10):
    """
    Simulate multiple walks of different types and compare their spreads.
    
    Returns:
        results: Dictionary with final_distances for each walk type
    """
    results = {
        'ideal': [],
        'levy': [],
        'correlated': [],
        'animal': []
    }
    
    for _ in range(num_replicates):
        # Ideal random walk
        x, y = simulate_ideal_random_walk_2d(num_steps)
        results['ideal'].append(np.sqrt(x[-1]**2 + y[-1]**2))
        
        # Lévy flight
        x, y = simulate_levy_flight_2d(num_steps, alpha=1.5)
        results['levy'].append(np.sqrt(x[-1]**2 + y[-1]**2))
        
        # Correlated walk
        x, y = simulate_correlated_random_walk_2d(num_steps, step_dist='exponential')
        results['correlated'].append(np.sqrt(x[-1]**2 + y[-1]**2))
        
        # Realistic animal track
        x, y = simulate_realistic_animal_track(num_steps)
        results['animal'].append(np.sqrt(x[-1]**2 + y[-1]**2))
    
    return results


# ============================================================================
# Visualization Functions
# ============================================================================

def plot_walk_comparison(num_steps=3000):
    """Plot four walk types side by side."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    np.random.seed(42)
    
    # Ideal random walk
    x, y = simulate_ideal_random_walk_2d(num_steps)
    axes[0, 0].plot(x, y, linewidth=0.3, alpha=0.7)
    axes[0, 0].scatter([0], [0], color='red', s=100, zorder=5)
    axes[0, 0].scatter([x[-1]], [y[-1]], color='green', s=100, zorder=5)
    axes[0, 0].set_title('Ideal Random Walk')
    axes[0, 0].set_aspect('equal')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Lévy flight
    x, y = simulate_levy_flight_2d(num_steps, alpha=1.5)
    axes[0, 1].plot(x, y, linewidth=0.3, alpha=0.7)
    axes[0, 1].scatter([0], [0], color='red', s=100, zorder=5)
    axes[0, 1].scatter([x[-1]], [y[-1]], color='green', s=100, zorder=5)
    axes[0, 1].set_title('Lévy Flight (α=1.5)')
    axes[0, 1].set_aspect('equal')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Correlated walk
    x, y = simulate_correlated_random_walk_2d(num_steps, step_dist='exponential')
    axes[1, 0].plot(x, y, linewidth=0.3, alpha=0.7)
    axes[1, 0].scatter([0], [0], color='red', s=100, zorder=5)
    axes[1, 0].scatter([x[-1]], [y[-1]], color='green', s=100, zorder=5)
    axes[1, 0].set_title('Correlated Random Walk')
    axes[1, 0].set_aspect('equal')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Realistic animal track
    x, y = simulate_realistic_animal_track(num_steps)
    axes[1, 1].plot(x, y, linewidth=0.3, alpha=0.7)
    axes[1, 1].scatter([0], [0], color='red', s=100, zorder=5)
    axes[1, 1].scatter([x[-1]], [y[-1]], color='green', s=100, zorder=5)
    axes[1, 1].set_title('Realistic Animal Track')
    axes[1, 1].set_aspect('equal')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_step_distributions(num_steps=5000):
    """Compare step-length distributions for different walk types."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    np.random.seed(42)
    
    # Ideal random walk
    x, y = simulate_ideal_random_walk_2d(num_steps)
    steps = extract_step_lengths(x, y)
    axes[0, 0].hist(steps, bins=30, density=True, alpha=0.7, edgecolor='black')
    axes[0, 0].set_title('Ideal Random Walk')
    axes[0, 0].set_xlabel('Step Length')
    axes[0, 0].set_ylabel('Density')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Exponential (animal)
    x, y = simulate_correlated_random_walk_2d(num_steps, step_dist='exponential')
    steps = extract_step_lengths(x, y)
    axes[0, 1].hist(steps, bins=30, density=True, alpha=0.7, edgecolor='black')
    axes[0, 1].set_title('Exponential Steps (Animal-like)')
    axes[0, 1].set_xlabel('Step Length')
    axes[0, 1].set_ylabel('Density')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Power-law (Lévy flight) - linear scale
    x, y = simulate_levy_flight_2d(num_steps, alpha=1.5)
    steps = extract_step_lengths(x, y)
    axes[1, 0].hist(steps[steps < 20], bins=30, density=True, alpha=0.7, edgecolor='black')
    axes[1, 0].set_title('Power-Law Steps (Lévy, tail cut off)')
    axes[1, 0].set_xlabel('Step Length')
    axes[1, 0].set_ylabel('Density')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Power-law on log-log scale
    sorted_steps = np.sort(steps)
    ccdf = 1 - np.arange(len(sorted_steps)) / len(sorted_steps)
    axes[1, 1].loglog(sorted_steps[sorted_steps > 0.1], ccdf[sorted_steps > 0.1], 
                      'o', markersize=3, alpha=0.7)
    axes[1, 1].set_title('Power-Law Steps (log-log, CCDF)')
    axes[1, 1].set_xlabel('Step Length (log)')
    axes[1, 1].set_ylabel('P(S > s) (log)')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_spread_comparison(num_steps_array=None, num_replicates=5):
    """
    Compare how different walk types spread over time.
    
    Args:
        num_steps_array: Array of step counts to test
        num_replicates: Number of walks to average over
    """
    if num_steps_array is None:
        num_steps_array = [100, 500, 1000, 5000, 10000]
    
    results = {walk_type: [] for walk_type in ['ideal', 'levy', 'correlated', 'animal']}
    
    for num_steps in num_steps_array:
        for walk_type in results:
            distances = []
            for _ in range(num_replicates):
                if walk_type == 'ideal':
                    x, y = simulate_ideal_random_walk_2d(num_steps)
                elif walk_type == 'levy':
                    x, y = simulate_levy_flight_2d(num_steps, alpha=1.5)
                elif walk_type == 'correlated':
                    x, y = simulate_correlated_random_walk_2d(num_steps)
                else:  # animal
                    x, y = simulate_realistic_animal_track(num_steps)
                
                distances.append(np.sqrt(x[-1]**2 + y[-1]**2))
            
            results[walk_type].append(np.mean(distances))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for walk_type, distances in results.items():
        ax.plot(num_steps_array, distances, 'o-', label=walk_type, linewidth=2, markersize=8)
    
    # Overlay √n reference line
    sqrt_n = np.sqrt(np.array(num_steps_array))
    ax.plot(num_steps_array, sqrt_n / sqrt_n[0] * results['ideal'][0], 'k--', 
            alpha=0.5, label='√n reference')
    
    ax.set_xlabel('Number of Steps')
    ax.set_ylabel('Mean Final Distance from Origin')
    ax.set_title('Spread Comparison: Different Walk Types')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    return fig


def plot_power_law_fit(alpha=1.5, num_steps=5000):
    """
    Generate Lévy flight data and fit power-law exponent.
    """
    np.random.seed(42)
    x, y = simulate_levy_flight_2d(num_steps, alpha=alpha)
    steps = extract_step_lengths(x, y)
    
    x_min = 0.5
    alpha_est = fit_power_law_exponent(steps, x_min=x_min)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Empirical CCDF
    sorted_steps = np.sort(steps[steps > x_min])
    ccdf = 1 - np.arange(len(sorted_steps)) / len(sorted_steps)
    ax.loglog(sorted_steps, ccdf, 'o', markersize=3, alpha=0.7, label='Empirical')
    
    # Fitted power law
    s_range = np.logspace(-0.5, 2.5, 200)
    s_range = s_range[s_range > x_min]
    ax.loglog(s_range, (x_min / s_range)**alpha_est, '-', linewidth=2.5,
              label=f'Fitted (α={alpha_est:.2f})')
    
    ax.set_xlabel('Step Length (log scale)')
    ax.set_ylabel('P(S > s) (log scale)')
    ax.set_title(f'Power-Law Fitting: True α={alpha}, Estimated α={alpha_est:.2f}')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    return fig, alpha_est


# ============================================================================
# Demo / Main
# ============================================================================

if __name__ == '__main__':
    print("Chapter 6: Random Walks in the Wild")
    print("=" * 50)
    
    # Compare walk types
    print("\nComparing walk types (5 replicates, 5000 steps each):")
    results = compare_walk_types(num_steps=5000, num_replicates=5)
    for walk_type, distances in results.items():
        mean_dist = np.mean(distances)
        std_dist = np.std(distances)
        print(f"  {walk_type:12s}: {mean_dist:8.2f} ± {std_dist:.2f} (mean ± std)")
    
    # Fit power-law to Lévy flight
    print("\nFitting power-law exponent:")
    x, y = simulate_levy_flight_2d(5000, alpha=1.5)
    steps = extract_step_lengths(x, y)
    alpha_est = fit_power_law_exponent(steps, x_min=0.5)
    print(f"  True exponent: 1.50, Estimated: {alpha_est:.2f}")
    
    print("\nGenerating visualizations...")
    plot_walk_comparison()
    plot_step_distributions()
    plot_spread_comparison()
    plot_power_law_fit(alpha=1.5)
    
    print("Done!")
