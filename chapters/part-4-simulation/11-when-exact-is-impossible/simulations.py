"""
Chapter 11: When Exact Is Impossible
The curse of dimensionality and why Monte Carlo thrives in high dimensions.
"""

import numpy as np
import matplotlib.pyplot as plt


# ============================================================================
# Grid vs. Monte Carlo Comparison
# ============================================================================

def grid_method_complexity(d, bins_per_dim):
    """
    Compute number of points needed for grid method in d dimensions.
    
    Args:
        d: Dimension
        bins_per_dim: Number of bins per dimension
    
    Returns:
        Total number of grid points
    """
    return bins_per_dim ** d


def monte_carlo_sample_complexity(error_target, variance=1.0):
    """
    Compute number of samples needed for Monte Carlo to achieve target error.
    
    Args:
        error_target: Desired error level
        variance: Variance of integrand
    
    Returns:
        Number of samples needed
    """
    # Error ~ sqrt(variance / n)
    # n ~ variance / error^2
    return int(np.ceil(variance / (error_target ** 2)))


def complexity_comparison(max_dim=20, bins_per_dim=10, error_target=0.01):
    """
    Compare grid and Monte Carlo sample complexity across dimensions.
    
    Args:
        max_dim: Maximum dimension to compute
        bins_per_dim: Bins per dimension for grid
        error_target: Target error for Monte Carlo
    
    Returns:
        Lists of dimensions, grid samples, MC samples
    """
    dims = list(range(1, max_dim + 1))
    grid_samples = [grid_method_complexity(d, bins_per_dim) for d in dims]
    mc_samples = [monte_carlo_sample_complexity(error_target) for d in dims]
    
    return dims, grid_samples, mc_samples


# ============================================================================
# Volume Concentration
# ============================================================================

def volume_in_interior(d, interior_distance=0.1):
    """
    Compute fraction of d-dimensional unit cube in interior.
    
    Interior = points with distance > interior_distance from all boundaries.
    
    Args:
        d: Dimension
        interior_distance: Distance from boundary
    
    Returns:
        Fraction of volume in interior
    """
    # Interior = [interior_distance, 1-interior_distance]^d
    interior_width = 1.0 - 2 * interior_distance
    interior_volume = interior_width ** d
    return interior_volume


def volumes_across_dimensions(max_dim=20, interior_distance=0.1):
    """
    Compute interior volume fraction for dimensions 1 through max_dim.
    
    Args:
        max_dim: Maximum dimension
        interior_distance: Distance from boundary defining "interior"
    
    Returns:
        Lists of dimensions and interior volume fractions
    """
    dims = list(range(1, max_dim + 1))
    volumes = [volume_in_interior(d, interior_distance) for d in dims]
    return dims, volumes


# ============================================================================
# High-Dimensional Geometry: Distance Analysis
# ============================================================================

def typical_distance_from_origin(d):
    """
    Compute typical distance from origin to a random point in [-1, 1]^d.
    
    For uniform random x in [-1, 1]^d:
    E[||x||^2] = d * E[x_i^2] = d * (1/3)
    
    Args:
        d: Dimension
    
    Returns:
        Typical (expected) distance
    """
    return np.sqrt(d / 3)


def sample_distances(d, n_samples=1000):
    """
    Sample distances from origin for random points in [-1, 1]^d.
    
    Args:
        d: Dimension
        n_samples: Number of random points
    
    Returns:
        Array of distances
    """
    points = np.random.uniform(-1, 1, (n_samples, d))
    distances = np.linalg.norm(points, axis=1)
    return distances


def pairwise_distances(d, n_points=100):
    """
    Compute pairwise distances between random points in [0, 1]^d.
    
    Args:
        d: Dimension
        n_points: Number of random points
    
    Returns:
        Array of pairwise distances (excluding diagonal)
    """
    points = np.random.uniform(0, 1, (n_points, d))
    
    # Compute pairwise distances
    distances = np.linalg.norm(points[:, np.newaxis, :] - points[np.newaxis, :, :], axis=2)
    
    # Return upper triangle (excluding diagonal)
    distances = distances[np.triu_indices_from(distances, k=1)]
    
    return distances


def distance_concentration(d_values, n_points=100):
    """
    Compute max/min pairwise distance ratio for different dimensions.
    
    High ratio = distances vary widely. Low ratio = distances nearly equal.
    
    Args:
        d_values: List of dimensions to test
        n_points: Number of random points per dimension
    
    Returns:
        Lists of dimensions and max/min ratios
    """
    ratios = []
    
    for d in d_values:
        distances = pairwise_distances(d, n_points)
        ratio = distances.max() / distances.min()
        ratios.append(ratio)
    
    return d_values, ratios


# ============================================================================
# High-Dimensional Geometry: Angles
# ============================================================================

def angle_between_vectors(d, n_samples=100):
    """
    Compute angles between random vectors in d dimensions.
    
    Args:
        d: Dimension
        n_samples: Number of random vector pairs
    
    Returns:
        Array of angles (in degrees)
    """
    angles = []
    
    for _ in range(n_samples):
        u = np.random.randn(d)
        v = np.random.randn(d)
        
        # Compute angle
        cos_angle = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
        cos_angle = np.clip(cos_angle, -1, 1)  # Numerical safety
        angle_rad = np.arccos(cos_angle)
        angle_deg = angle_rad * 180 / np.pi
        
        angles.append(angle_deg)
    
    return np.array(angles)


def average_angle_across_dimensions(d_values, n_samples=100):
    """
    Compute average angle between random vectors for different dimensions.
    
    Args:
        d_values: List of dimensions
        n_samples: Number of vector pairs per dimension
    
    Returns:
        Lists of dimensions and average angles
    """
    avg_angles = []
    
    for d in d_values:
        angles = angle_between_vectors(d, n_samples)
        avg_angles.append(np.mean(angles))
    
    return d_values, avg_angles


# ============================================================================
# High-Dimensional Integration: Comparison
# ============================================================================

def integrate_high_dim_grid(f, d, bins_per_dim):
    """
    Integrate f over [0,1]^d using grid method.
    
    Args:
        f: Function to integrate (takes d-dim point)
        d: Dimension
        bins_per_dim: Number of bins per dimension
    
    Returns:
        Integral estimate
    """
    bin_width = 1.0 / bins_per_dim
    bin_volume = bin_width ** d
    
    # Generate grid points (at bin centers)
    linspace = np.linspace(bin_width/2, 1 - bin_width/2, bins_per_dim)
    grid_points = np.meshgrid(*[linspace] * d, indexing='ij')
    
    # Flatten to list of points
    points = np.column_stack([g.ravel() for g in grid_points])
    
    # Evaluate and average
    values = np.array([f(point) for point in points])
    integral = bin_volume * values.sum()
    
    return integral


def integrate_high_dim_mc(f, d, n_samples):
    """
    Integrate f over [0,1]^d using Monte Carlo.
    
    Args:
        f: Function to integrate
        d: Dimension
        n_samples: Number of random samples
    
    Returns:
        Integral estimate
    """
    points = np.random.uniform(0, 1, (n_samples, d))
    values = np.array([f(point) for point in points])
    integral = np.mean(values)
    
    return integral


# ============================================================================
# Visualization Functions
# ============================================================================

def plot_complexity_comparison(max_dim=20):
    """Plot grid vs. Monte Carlo complexity across dimensions."""
    dims, grid_samples, mc_samples = complexity_comparison(max_dim=max_dim, bins_per_dim=10)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Linear scale
    ax1.plot(dims, grid_samples, 'ro-', label='Grid (10^d)', linewidth=2, markersize=8)
    ax1.plot(dims, mc_samples, 'bs-', label='Monte Carlo', linewidth=2, markersize=8)
    ax1.set_xlabel('Dimension d')
    ax1.set_ylabel('Number of Samples')
    ax1.set_title('Sample Complexity: Grid vs. Monte Carlo (Linear Scale)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(ymin=0, ymax=1e7)
    
    # Log scale
    ax2.loglog(dims, grid_samples, 'ro-', label='Grid (10^d)', linewidth=2, markersize=8)
    ax2.loglog(dims, mc_samples, 'bs-', label='Monte Carlo', linewidth=2, markersize=8)
    ax2.set_xlabel('Dimension d')
    ax2.set_ylabel('Number of Samples (log scale)')
    ax2.set_title('Sample Complexity: Grid vs. Monte Carlo (Log Scale)')
    ax2.legend()
    ax2.grid(True, alpha=0.3, which='both')
    
    return fig


def plot_volume_concentration(max_dim=20):
    """Plot volume concentration in interior."""
    dims, volumes = volumes_across_dimensions(max_dim=max_dim)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(dims, volumes, 'go-', linewidth=2, markersize=8)
    ax.axhline(0.5, color='r', linestyle='--', linewidth=1, alpha=0.5, label='50%')
    ax.set_xlabel('Dimension d')
    ax.set_ylabel('Fraction of Volume in Interior')
    ax.set_title('Volume Concentration: Curse of Dimensionality')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(ymin=0, ymax=1)
    
    return fig


def plot_distance_concentration(max_dim=20):
    """Plot distance concentration."""
    d_values = list(range(1, max_dim + 1))
    d_values_plot, ratios = distance_concentration(d_values)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(d_values_plot, ratios, 'mo-', linewidth=2, markersize=8)
    ax.set_xlabel('Dimension d')
    ax.set_ylabel('Max/Min Pairwise Distance Ratio')
    ax.set_title('Distance Concentration: All Distances Become Similar')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3, which='both')
    
    return fig


def plot_angle_concentration(max_dim=20):
    """Plot angle concentration."""
    d_values = list(range(1, max_dim + 1))
    d_values_plot, avg_angles = average_angle_across_dimensions(d_values)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(d_values_plot, avg_angles, 'co-', linewidth=2, markersize=8)
    ax.axhline(90, color='r', linestyle='--', linewidth=2, label='90° (perpendicular)')
    ax.set_xlabel('Dimension d')
    ax.set_ylabel('Average Angle (degrees)')
    ax.set_title('Angle Concentration: Random Vectors Become Perpendicular')
    ax.set_ylim(ymin=0, ymax=95)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig


# ============================================================================
# Demo / Main
# ============================================================================

if __name__ == '__main__':
    print("Chapter 11: When Exact Is Impossible")
    print("=" * 60)
    
    # Sample complexity
    print("\n--- Sample Complexity: Grid vs. Monte Carlo ---")
    dims, grid_samps, mc_samps = complexity_comparison(max_dim=10)
    
    print("Dim | Grid (10 bins/dim) | Monte Carlo | Ratio (Grid/MC)")
    print("-" * 55)
    for d, g, m in zip(dims, grid_samps, mc_samps):
        ratio = g / m if m > 0 else np.inf
        print(f"{d:>3} | {g:>18} | {m:>11} | {ratio:>14.1f}x")
    
    # Volume concentration
    print("\n--- Volume Concentration in Interior ---")
    dims, vols = volumes_across_dimensions(max_dim=10, interior_distance=0.1)
    
    print("Dim | Fraction of Volume in Interior")
    print("-" * 35)
    for d, v in zip(dims, vols):
        print(f"{d:>3} | {v:>6.1%}")
    
    # Distance from origin
    print("\n--- Typical Distance from Origin ---")
    print("Dim | Expected Distance | Sample Mean | Sample Std")
    print("-" * 50)
    for d in [1, 2, 5, 10, 20, 50, 100]:
        expected = typical_distance_from_origin(d)
        distances = sample_distances(d, n_samples=1000)
        sample_mean = np.mean(distances)
        sample_std = np.std(distances)
        print(f"{d:>3} | {expected:>17.3f} | {sample_mean:>11.3f} | {sample_std:>9.3f}")
    
    # Distance concentration
    print("\n--- Distance Concentration (Max/Min Ratio) ---")
    d_vals = [1, 2, 5, 10, 20, 50]
    d_vals_plot, ratios = distance_concentration(d_vals, n_points=100)
    
    print("Dim | Max/Min Pairwise Distance Ratio")
    print("-" * 35)
    for d, r in zip(d_vals_plot, ratios):
        print(f"{d:>3} | {r:>7.2f}")
    
    # Angle concentration
    print("\n--- Angle Concentration ---")
    d_vals = [1, 2, 5, 10, 20, 50]
    d_vals_plot, angles = average_angle_across_dimensions(d_vals, n_samples=100)
    
    print("Dim | Average Angle (degrees)")
    print("-" * 28)
    for d, a in zip(d_vals_plot, angles):
        print(f"{d:>3} | {a:>23.1f}°")
    
    print("\nDone!")
