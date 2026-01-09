"""
Simulations for Chapter 5: Wandering in Two Dimensions

This module provides functions for simulating random walks in 2D, 3D, and higher dimensions.
It includes utilities for tracking returns, visualizing paths, and analyzing dimensional effects.
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


# ============================================================================
# Core Simulation Functions
# ============================================================================

def simulate_2d_random_walk(num_steps):
    """
    Simulate a 2D random walk on a grid.
    
    Args:
        num_steps: Number of steps to take
    
    Returns:
        tuple: (x_history, y_history) as numpy arrays
    """
    x, y = 0, 0
    x_history = [x]
    y_history = [y]
    
    # Four directions: up, down, left, right
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    
    for _ in range(num_steps):
        dx, dy = random.choice(directions)
        x += dx
        y += dy
        x_history.append(x)
        y_history.append(y)
    
    return np.array(x_history), np.array(y_history)


def simulate_3d_random_walk(num_steps):
    """
    Simulate a 3D random walk on a grid.
    
    Args:
        num_steps: Number of steps to take
    
    Returns:
        tuple: (x_history, y_history, z_history) as numpy arrays
    """
    x, y, z = 0, 0, 0
    x_history = [x]
    y_history = [y]
    z_history = [z]
    
    # Six directions: ±x, ±y, ±z
    directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    
    for _ in range(num_steps):
        dx, dy, dz = random.choice(directions)
        x += dx
        y += dy
        z += dz
        x_history.append(x)
        y_history.append(y)
        z_history.append(z)
    
    return np.array(x_history), np.array(y_history), np.array(z_history)


def simulate_nd_random_walk(num_steps, dimension):
    """
    Simulate a random walk in d dimensions.
    
    Args:
        num_steps: Number of steps to take
        dimension: Number of dimensions
    
    Returns:
        list: Position history (list of d-tuples)
    """
    position = [0] * dimension
    history = [tuple(position)]
    
    for _ in range(num_steps):
        # Choose random coordinate and direction
        coord = random.randint(0, dimension - 1)
        direction = random.choice([-1, 1])
        position[coord] += direction
        history.append(tuple(position))
    
    return history


def final_position_2d(num_steps):
    """Quick simulation returning only final position."""
    x, y = 0, 0
    for _ in range(num_steps):
        dx, dy = random.choice([(0, 1), (0, -1), (-1, 0), (1, 0)])
        x += dx
        y += dy
    return x, y


def final_distance_2d(num_steps):
    """Quick simulation returning only final distance from origin."""
    x, y = final_position_2d(num_steps)
    return np.sqrt(x**2 + y**2)


def final_position_3d(num_steps):
    """Quick simulation returning only final position."""
    x, y, z = 0, 0, 0
    for _ in range(num_steps):
        dx, dy, dz = random.choice([(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)])
        x += dx
        y += dy
        z += dz
    return x, y, z


def final_distance_3d(num_steps):
    """Quick simulation returning only final distance from origin."""
    x, y, z = final_position_3d(num_steps)
    return np.sqrt(x**2 + y**2 + z**2)


def final_distance_nd(num_steps, dimension):
    """Quick simulation in d dimensions."""
    position = [0] * dimension
    for _ in range(num_steps):
        coord = random.randint(0, dimension - 1)
        position[coord] += random.choice([-1, 1])
    return np.sqrt(sum(p**2 for p in position))


# ============================================================================
# Return Tracking Functions
# ============================================================================

def return_to_origin_2d(max_steps=100000):
    """
    Simulate 2D walk until it returns to origin.
    
    Args:
        max_steps: Maximum steps to allow
    
    Returns:
        int or None: Steps until return, or None if max_steps exceeded
    """
    x, y = 0, 0
    
    for step in range(1, max_steps + 1):
        dx, dy = random.choice([(0, 1), (0, -1), (-1, 0), (1, 0)])
        x += dx
        y += dy
        
        if x == 0 and y == 0:
            return step
    
    return None


def return_to_origin_3d(max_steps=100000):
    """
    Simulate 3D walk until it returns to origin.
    
    Args:
        max_steps: Maximum steps to allow
    
    Returns:
        int or None: Steps until return, or None if max_steps exceeded
    """
    x, y, z = 0, 0, 0
    
    for step in range(1, max_steps + 1):
        dx, dy, dz = random.choice([(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)])
        x += dx
        y += dy
        z += dz
        
        if x == 0 and y == 0 and z == 0:
            return step
    
    return None


def return_probability_nd(dimension, num_walks=100, max_steps=50000):
    """
    Estimate return probability for dimension d.
    
    Args:
        dimension: Number of dimensions
        num_walks: Number of walks to simulate
        max_steps: Maximum steps per walk
    
    Returns:
        float: Fraction of walks that returned
    """
    returns = 0
    
    for _ in range(num_walks):
        position = [0] * dimension
        
        for step in range(max_steps):
            coord = random.randint(0, dimension - 1)
            position[coord] += random.choice([-1, 1])
            
            if all(p == 0 for p in position):
                returns += 1
                break
    
    return returns / num_walks


# ============================================================================
# Maximum Distance Functions
# ============================================================================

def max_distance_reached_2d(num_steps):
    """Track maximum distance during 2D walk."""
    x, y = 0, 0
    max_dist = 0
    
    for _ in range(num_steps):
        dx, dy = random.choice([(0, 1), (0, -1), (-1, 0), (1, 0)])
        x += dx
        y += dy
        dist = np.sqrt(x**2 + y**2)
        max_dist = max(max_dist, dist)
    
    return max_dist


def max_distance_reached_3d(num_steps):
    """Track maximum distance during 3D walk."""
    x, y, z = 0, 0, 0
    max_dist = 0
    
    for _ in range(num_steps):
        dx, dy, dz = random.choice([(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)])
        x += dx
        y += dy
        z += dz
        dist = np.sqrt(x**2 + y**2 + z**2)
        max_dist = max(max_dist, dist)
    
    return max_dist


# ============================================================================
# Analysis Functions
# ============================================================================

def analyze_walks_by_dimension(num_walks, num_steps, dimensions):
    """
    Run walks in multiple dimensions and compare distances.
    
    Args:
        num_walks: Number of walks per dimension
        num_steps: Steps per walk
        dimensions: List of dimensions to test
    
    Returns:
        dict: Statistics for each dimension
    """
    results = {}
    
    for d in dimensions:
        distances = [final_distance_nd(num_steps, d) for _ in range(num_walks)]
        distances = np.array(distances)
        
        results[d] = {
            'distances': distances,
            'mean': distances.mean(),
            'std': distances.std(),
            'min': distances.min(),
            'max': distances.max(),
            'theoretical_mean': np.sqrt(num_steps),  # All dimensions have same expected distance
        }
    
    return results


# ============================================================================
# Visualization Functions
# ============================================================================

def plot_single_2d_walk(num_steps=5000, figsize=(10, 10)):
    """Plot a single 2D random walk."""
    x, y = simulate_2d_random_walk(num_steps)
    
    plt.figure(figsize=figsize)
    plt.plot(x, y, linewidth=0.3, alpha=0.7)
    plt.scatter([0], [0], color='red', s=100, marker='o', label='Start', zorder=5)
    plt.scatter([x[-1]], [y[-1]], color='green', s=100, marker='s', label='End', zorder=5)
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.title(f"A 2D Random Walk: {num_steps} Steps")
    plt.grid(True, alpha=0.3)
    plt.gca().set_aspect('equal')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    final_distance = np.sqrt(x[-1]**2 + y[-1]**2)
    max_distance = np.max(np.sqrt(x**2 + y**2))
    print(f"Final distance from origin: {final_distance:.1f}")
    print(f"Maximum distance reached: {max_distance:.1f}")


def plot_multiple_2d_walks(num_walks=8, num_steps=2000, figsize=(12, 12)):
    """Plot multiple 2D walks overlaid."""
    fig, ax = plt.subplots(figsize=figsize)
    
    colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray']
    
    for i in range(num_walks):
        x, y = simulate_2d_random_walk(num_steps)
        ax.plot(x, y, linewidth=0.4, alpha=0.5, color=colors[i % len(colors)])
    
    ax.scatter([0], [0], color='black', s=200, marker='*', zorder=10, label='Origin')
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.set_title(f"Multiple 2D Random Walks: {num_walks} walks, {num_steps} steps each")
    ax.grid(True, alpha=0.2)
    ax.legend()
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.show()


def plot_distance_by_dimension(num_walks=1000, num_steps=1000, figsize=(16, 5)):
    """Compare final distances in 1D, 2D, and 3D."""
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    
    # 1D
    from simulations import final_distance_1d  # Assuming this exists in chapter 4
    # For now, implement simple 1D
    distances_1d = [abs(sum(random.choice([-1, 1]) for _ in range(num_steps))) for _ in range(num_walks)]
    axes[0].hist(distances_1d, bins=40, alpha=0.7, edgecolor='black', color='blue')
    axes[0].set_title("1D Random Walks")
    axes[0].set_xlabel("Final Distance")
    axes[0].set_ylabel("Count")
    axes[0].axvline(np.sqrt(num_steps), color='red', linestyle='--', linewidth=2, 
                    label=f'Theory: √n = {np.sqrt(num_steps):.1f}')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # 2D
    distances_2d = [final_distance_2d(num_steps) for _ in range(num_walks)]
    axes[1].hist(distances_2d, bins=40, alpha=0.7, edgecolor='black', color='green')
    axes[1].set_title("2D Random Walks")
    axes[1].set_xlabel("Final Distance")
    axes[1].set_ylabel("Count")
    axes[1].axvline(np.sqrt(2*num_steps), color='red', linestyle='--', linewidth=2,
                    label=f'Theory: √(2n) = {np.sqrt(2*num_steps):.1f}')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # 3D
    distances_3d = [final_distance_3d(num_steps) for _ in range(num_walks)]
    axes[2].hist(distances_3d, bins=40, alpha=0.7, edgecolor='black', color='orange')
    axes[2].set_title("3D Random Walks")
    axes[2].set_xlabel("Final Distance")
    axes[2].set_ylabel("Count")
    axes[2].axvline(np.sqrt(3*num_steps), color='red', linestyle='--', linewidth=2,
                    label=f'Theory: √(3n) = {np.sqrt(3*num_steps):.1f}')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    plt.suptitle(f"Final Distance Distributions: 1D vs 2D vs 3D ({num_walks} walks, {num_steps} steps)")
    plt.tight_layout()
    plt.show()
    
    print(f"1D: mean={np.mean(distances_1d):.1f}, std={np.std(distances_1d):.1f}")
    print(f"2D: mean={np.mean(distances_2d):.1f}, std={np.std(distances_2d):.1f}")
    print(f"3D: mean={np.mean(distances_3d):.1f}, std={np.std(distances_3d):.1f}")


def plot_return_rates_by_dimension(dimensions, figsize=(10, 6)):
    """Plot return probability across dimensions."""
    return_rates = []
    
    print("Testing return probability by dimension...")
    for d in dimensions:
        walks = 200 if d <= 3 else 100
        rate = return_probability_nd(d, num_walks=walks, max_steps=30000)
        return_rates.append(rate)
        print(f"  Dimension {d}: {rate:.2f}")
    
    fig, ax = plt.subplots(figsize=figsize)
    
    colors = ['green'] * len([d for d in dimensions if d <= 2])
    colors += ['red'] * len([d for d in dimensions if d > 2])
    
    ax.scatter(dimensions, return_rates, s=100, c=colors, alpha=0.6)
    ax.plot(dimensions[:len([d for d in dimensions if d <= 2])], 
            return_rates[:len([d for d in dimensions if d <= 2])],
            'o-', color='green', linewidth=2, markersize=8, label='Recurrent')
    ax.plot(dimensions[len([d for d in dimensions if d <= 2]):],
            return_rates[len([d for d in dimensions if d <= 2]):],
            's--', color='red', linewidth=2, markersize=8, label='Transient')
    
    ax.axhline(y=1.0, color='green', linestyle=':', alpha=0.3, linewidth=1)
    ax.axhline(y=0.34, color='orange', linestyle=':', alpha=0.3, linewidth=1)
    ax.axvline(x=2.5, color='black', linestyle=':', alpha=0.3, linewidth=1)
    
    ax.set_xlabel("Dimension")
    ax.set_ylabel("Return Probability")
    ax.set_title("Pólya's Recurrence Theorem: Return Probability by Dimension")
    ax.set_ylim(-0.05, 1.1)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11)
    
    plt.tight_layout()
    plt.show()


def plot_2d_vs_3d_returns(num_walks_per_dim=500, max_steps=100000, figsize=(14, 5)):
    """Compare return time distributions in 2D vs 3D."""
    print("Collecting 2D returns...")
    returns_2d = []
    for i in range(num_walks_per_dim):
        if i % 100 == 0:
            print(f"  {i}/{num_walks_per_dim}")
        ret = return_to_origin_2d(max_steps)
        if ret is not None:
            returns_2d.append(ret)
    
    print("Collecting 3D returns...")
    returns_3d = []
    for i in range(num_walks_per_dim):
        if i % 100 == 0:
            print(f"  {i}/{num_walks_per_dim}")
        ret = return_to_origin_3d(max_steps)
        if ret is not None:
            returns_3d.append(ret)
    
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    if len(returns_2d) > 0:
        returns_2d = np.array(returns_2d)
        axes[0].hist(returns_2d, bins=50, alpha=0.7, edgecolor='black', color='green')
        axes[0].set_xlabel("Steps Until Return")
        axes[0].set_ylabel("Count")
        axes[0].set_title(f"2D Return Times ({len(returns_2d)}/{num_walks_per_dim} returned)")
        axes[0].set_xscale('log')
        axes[0].set_yscale('log')
        axes[0].grid(True, alpha=0.3, which='both')
    
    if len(returns_3d) > 0:
        returns_3d = np.array(returns_3d)
        axes[1].hist(returns_3d, bins=50, alpha=0.7, edgecolor='black', color='orange')
        axes[1].set_xlabel("Steps Until Return")
        axes[1].set_ylabel("Count")
        axes[1].set_title(f"3D Return Times ({len(returns_3d)}/{num_walks_per_dim} returned)")
        axes[1].set_xscale('log')
        axes[1].set_yscale('log')
        axes[1].grid(True, alpha=0.3, which='both')
    
    plt.suptitle("Return to Origin: 2D (Recurrent) vs 3D (Transient)")
    plt.tight_layout()
    plt.show()
    
    print(f"\n2D: {100*len(returns_2d)/num_walks_per_dim:.1f}% returned")
    print(f"3D: {100*len(returns_3d)/num_walks_per_dim:.1f}% returned")


# ============================================================================
# Demo / Main
# ============================================================================

if __name__ == "__main__":
    print("Chapter 5: Wandering in Two Dimensions - Simulations")
    print("=" * 50)
    print()
    print("This module contains functions for simulating and visualizing")
    print("random walks in 2D, 3D, and higher dimensions.")
    print()
    print("Examples:")
    print("  plot_single_2d_walk(5000)")
    print("  plot_multiple_2d_walks(8, 2000)")
    print("  plot_distance_by_dimension(1000, 1000)")
    print("  plot_return_rates_by_dimension([1, 2, 3, 4, 5])")
    print()
