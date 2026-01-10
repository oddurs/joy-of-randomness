"""
Figure generation for Chapter 9: The Chain That Ranked the Internet
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch

plt.rcParams['text.usetex'] = False
plt.rcParams['mathtext.default'] = 'regular'

chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))

from shared.figures import figure

OUTPUT_DIR = Path(__file__).parent / "figures"


def generate_figure_9_1():
    """Figure 9.1: Web graph structure and random walk"""
    # Define a simple web graph
    pages = ['A', 'B', 'C', 'D', 'E']
    # Positions for visualization (roughly circular)
    pos = {
        'A': (0.5, 0.8),
        'B': (0.2, 0.5),
        'C': (0.8, 0.5),
        'D': (0.2, 0.2),
        'E': (0.8, 0.2)
    }
    
    # Links: A→B, A→C, B→A, B→D, C→A, C→D, D→E, E→A, E→C
    links = [
        ('A', 'B'), ('A', 'C'),
        ('B', 'A'), ('B', 'D'),
        ('C', 'A'), ('C', 'D'),
        ('D', 'E'),
        ('E', 'A'), ('E', 'C')
    ]
    
    with figure(3, 9, 1, output_dir=OUTPUT_DIR) as fig:
        # Left: Web graph
        ax1 = fig.add_subplot(131)
        ax1.set_xlim(-0.1, 1.1)
        ax1.set_ylim(-0.1, 1.1)
        ax1.axis('off')
        
        # Draw nodes
        for page, (x, y) in pos.items():
            circle = plt.Circle((x, y), 0.06, color='steelblue', zorder=3)
            ax1.add_patch(circle)
            ax1.text(x, y, page, ha='center', va='center', fontsize=14, weight='bold', color='white', zorder=4)
        
        # Draw edges with arrows
        for source, target in links:
            x1, y1 = pos[source]
            x2, y2 = pos[target]
            
            # Shorten arrows to not overlap circles
            dx, dy = x2 - x1, y2 - y1
            dist = np.sqrt(dx**2 + dy**2)
            x1_adj = x1 + 0.06 * dx / dist
            y1_adj = y1 + 0.06 * dy / dist
            x2_adj = x2 - 0.06 * dx / dist
            y2_adj = y2 - 0.06 * dy / dist
            
            arrow = FancyArrowPatch((x1_adj, y1_adj), (x2_adj, y2_adj),
                                  arrowstyle='->', mutation_scale=15, linewidth=1.5,
                                  color='gray', alpha=0.6, zorder=1)
            ax1.add_patch(arrow)
        
        ax1.set_title('Web Graph: 5 Pages with Links', fontsize=11, weight='bold')
        
        # Middle: Transition matrix
        ax2 = fig.add_subplot(132)
        P = np.array([
            [0,   0.5, 0.5,  0,   0],
            [0.5, 0,   0,   0.5, 0],
            [0.5, 0,   0,   0.5, 0],
            [0,   0,   0,    0,   1],
            [1/3, 1/3, 1/3,  0,   0]
        ])
        
        im = ax2.imshow(P, cmap='YlOrRd', aspect='auto', vmin=0, vmax=1)
        ax2.set_xticks(range(5))
        ax2.set_yticks(range(5))
        ax2.set_xticklabels(pages)
        ax2.set_yticklabels(pages)
        ax2.set_xlabel('To', fontsize=10)
        ax2.set_ylabel('From', fontsize=10)
        ax2.set_title('Transition Matrix P', fontsize=11, weight='bold')
        
        # Add values to cells
        for i in range(5):
            for j in range(5):
                val = P[i, j]
                if val > 0:
                    ax2.text(j, i, f'{val:.2f}', ha='center', va='center', 
                            fontsize=8, color='black')
        
        plt.colorbar(im, ax=ax2, label='Probability')
        
        # Right: Random walk simulation
        ax3 = fig.add_subplot(133)
        np.random.seed(42)
        current = 0
        visits = np.zeros(5)
        
        for _ in range(10000):
            visits[current] += 1
            current = np.random.choice(5, p=P[current])
        
        ranking = visits / visits.sum()
        colors = plt.cm.Spectral(np.linspace(0, 1, 5))
        bars = ax3.bar(pages, ranking, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax3.set_ylabel('Visit Frequency', fontsize=10)
        ax3.set_title('PageRank (10k Random Steps)', fontsize=11, weight='bold')
        ax3.set_ylim([0, max(ranking) * 1.2])
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add values on bars
        for bar, val in zip(bars, ranking):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.3f}', ha='center', va='bottom', fontsize=9)
        
        fig.suptitle('PageRank on a Toy Web', fontsize=14, y=0.98)


def generate_figure_9_2():
    """Figure 9.2: Effect of damping factor"""
    np.random.seed(42)
    
    # Simple graph: A→B, B→A (two-page cycle)
    P_base = np.array([[0, 1], [1, 0]])
    
    pages = ['A', 'B']
    damping_factors = [0.5, 0.75, 0.85, 0.99]
    
    with figure(3, 9, 2, output_dir=OUTPUT_DIR) as fig:
        for idx, d in enumerate(damping_factors):
            ax = fig.add_subplot(2, 2, idx + 1)
            
            # Modified transition matrix with teleportation
            N = 2
            P_prime = d * P_base + (1 - d) * (np.ones((N, N)) / N)
            
            # Compute stationary distribution (eigenvector)
            eigenvalues, eigenvectors = np.linalg.eig(P_prime.T)
            idx_stat = np.argmax(np.abs(eigenvalues))
            stationary = np.real(eigenvectors[:, idx_stat])
            stationary = stationary / stationary.sum()
            
            colors = ['steelblue', 'coral']
            bars = ax.bar(pages, stationary, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
            
            ax.set_ylabel('Probability')
            ax.set_title(f'Damping d = {d}', fontsize=11, weight='bold')
            ax.set_ylim([0, 1])
            ax.grid(True, alpha=0.3, axis='y')
            
            # Add values
            for bar, val in zip(bars, stationary):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{val:.3f}', ha='center', va='bottom', fontsize=9)
        
        fig.suptitle('Effect of Damping Factor on PageRank Distribution', fontsize=14, y=0.98)


def generate_figure_9_3():
    """Figure 9.3: Convergence of power iteration method"""
    np.random.seed(42)
    
    # 5-node network
    P = np.array([
        [0,   0.5, 0.5,  0,   0],
        [0.5, 0,   0,   0.5, 0],
        [0.5, 0,   0,   0.5, 0],
        [0,   0,   0,    0,   1],
        [1/3, 1/3, 1/3,  0,   0]
    ])
    
    N = 5
    d = 0.85
    P_prime = d * P + (1 - d) * (np.ones((N, N)) / N)
    
    # Power iteration
    pi = np.ones(N) / N
    history = [pi.copy()]
    
    for _ in range(100):
        pi = pi @ P_prime
        history.append(pi.copy())
    
    history = np.array(history)
    
    with figure(3, 9, 3, output_dir=OUTPUT_DIR) as fig:
        # Left: Convergence of each page
        ax1 = fig.add_subplot(121)
        pages = ['A', 'B', 'C', 'D', 'E']
        colors = plt.cm.Set1(np.linspace(0, 1, 5))
        
        for i, (page, color) in enumerate(zip(pages, colors)):
            ax1.plot(history[:, i], marker='o', markersize=2, linewidth=2,
                    label=f'Page {page}', color=color, alpha=0.8)
        
        ax1.set_xlabel('Iteration')
        ax1.set_ylabel('PageRank Value')
        ax1.set_title('Convergence of Power Iteration')
        ax1.legend(loc='right', fontsize=9)
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim([0, 50])
        
        # Right: Difference from final value
        ax2 = fig.add_subplot(122)
        final_pi = history[-1]
        
        for i, (page, color) in enumerate(zip(pages, colors)):
            diff = np.abs(history[:, i] - final_pi[i])
            ax2.semilogy(diff, marker='o', markersize=2, linewidth=2,
                        label=f'Page {page}', color=color, alpha=0.8)
        
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Absolute Error (log scale)')
        ax2.set_title('Convergence Error')
        ax2.legend(loc='upper right', fontsize=9)
        ax2.grid(True, alpha=0.3, which='both')
        ax2.set_xlim([0, 50])
        
        fig.suptitle('Power Iteration Method: How PageRank Converges', fontsize=14, y=0.98)


def generate_figure_9_4():
    """Figure 9.4: Larger network with diverse structure"""
    np.random.seed(42)
    
    # Create a more complex network: hub pages, leaves, cycles
    n_pages = 10
    
    # Create adjacency matrix
    adj = np.zeros((n_pages, n_pages))
    
    # Hub page (0) links to many pages
    adj[0, [1, 2, 3, 4]] = 1
    
    # Authority pages link back to hub
    adj[1, 0] = 1
    adj[2, 0] = 1
    adj[3, [0, 5]] = 1
    adj[4, [0, 6]] = 1
    
    # Leaf pages
    adj[5, [6, 7]] = 1
    adj[6, 7] = 1
    adj[7, 5] = 1  # Cycle
    
    # Isolated component
    adj[8, 9] = 1
    adj[9, 8] = 1
    
    # Convert to transition matrix
    out_degree = adj.sum(axis=1)
    P = np.zeros_like(adj, dtype=float)
    for i in range(n_pages):
        if out_degree[i] > 0:
            P[i, :] = adj[i, :] / out_degree[i]
        else:
            P[i, :] = 1 / n_pages  # Dangling node
    
    # Apply damping
    d = 0.85
    P_prime = d * P + (1 - d) * (np.ones((n_pages, n_pages)) / n_pages)
    
    # Compute stationary distribution
    eigenvalues, eigenvectors = np.linalg.eig(P_prime.T)
    idx_stat = np.argmax(np.abs(eigenvalues - 1))
    pagerank = np.real(eigenvectors[:, idx_stat])
    pagerank = pagerank / pagerank.sum()
    
    with figure(3, 9, 4, output_dir=OUTPUT_DIR) as fig:
        # Left: Network structure (force-directed layout approximation)
        ax1 = fig.add_subplot(121)
        
        # Simple radial layout based on importance
        angles = np.linspace(0, 2*np.pi, n_pages, endpoint=False)
        radii = 0.5 + 0.3 * pagerank / pagerank.max()
        
        x_pos = radii * np.cos(angles)
        y_pos = radii * np.sin(angles)
        
        # Draw edges
        for i in range(n_pages):
            for j in range(n_pages):
                if adj[i, j] > 0:
                    ax1.arrow(x_pos[i], y_pos[i], 
                             x_pos[j] - x_pos[i], y_pos[j] - y_pos[i],
                             head_width=0.03, head_length=0.02, fc='gray', ec='gray',
                             alpha=0.3, length_includes_head=True)
        
        # Draw nodes (size proportional to PageRank)
        sizes = 300 + 2000 * (pagerank / pagerank.max())
        scatter = ax1.scatter(x_pos, y_pos, s=sizes, c=pagerank, cmap='viridis',
                             alpha=0.8, edgecolors='black', linewidth=1.5, zorder=3)
        
        # Labels
        for i, (x, y) in enumerate(zip(x_pos, y_pos)):
            ax1.text(x, y, str(i), ha='center', va='center', fontsize=9,
                    weight='bold', color='white', zorder=4)
        
        ax1.set_xlim([-1.2, 1.2])
        ax1.set_ylim([-1.2, 1.2])
        ax1.set_aspect('equal')
        ax1.axis('off')
        ax1.set_title('Network Structure (Node size = PageRank importance)', fontsize=11, weight='bold')
        plt.colorbar(scatter, ax=ax1, label='PageRank')
        
        # Right: Ranking bars
        ax2 = fig.add_subplot(122)
        page_ids = [str(i) for i in range(n_pages)]
        sorted_indices = np.argsort(pagerank)[::-1]
        
        colors_sorted = plt.cm.viridis(pagerank[sorted_indices] / pagerank.max())
        bars = ax2.barh([page_ids[i] for i in sorted_indices],
                        pagerank[sorted_indices],
                        color=colors_sorted, edgecolor='black', linewidth=1)
        
        ax2.set_xlabel('PageRank')
        ax2.set_title('PageRank Ranking', fontsize=11, weight='bold')
        ax2.grid(True, alpha=0.3, axis='x')
        
        fig.suptitle('PageRank on a Larger Network (10 pages)', fontsize=14, y=0.98)


def main():
    """Generate all figures for Chapter 9."""
    print(f"Generating Chapter 9 figures...")
    print()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating Figure 9.1"); generate_figure_9_1()
    print(f"Generating Figure 9.2"); generate_figure_9_2()
    print(f"Generating Figure 9.3"); generate_figure_9_3()
    print(f"Generating Figure 9.4"); generate_figure_9_4()
    
    print()
    print("✓ All figures generated successfully!")


if __name__ == "__main__":
    main()
