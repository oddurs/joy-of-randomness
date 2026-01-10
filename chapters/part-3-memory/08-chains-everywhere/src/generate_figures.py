"""
Figure generation for Chapter 8: Chains Everywhere
"""

import sys
from pathlib import Path
import random
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = False
plt.rcParams['mathtext.default'] = 'regular'

chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))

from shared.figures import figure

OUTPUT_DIR = Path(__file__).parent / "figures"


def generate_figure_8_1():
    """Figure 8.1: Weather transition matrix and simulation"""
    np.random.seed(42)
    
    # Transition matrix for weather
    P = np.array([[0.7, 0.2, 0.1],
                  [0.25, 0.5, 0.25],
                  [0.1, 0.4, 0.5]])
    
    states = ['Sunny', 'Cloudy', 'Rainy']
    
    with figure(3, 8, 1, output_dir=OUTPUT_DIR) as fig:
        # Heatmap of transition matrix
        ax1 = fig.add_subplot(121)
        im = ax1.imshow(P, cmap='RdYlBu_r', aspect='auto', vmin=0, vmax=1)
        ax1.set_xticks(np.arange(len(states)))
        ax1.set_yticks(np.arange(len(states)))
        ax1.set_xticklabels(states)
        ax1.set_yticklabels(states)
        ax1.set_xlabel('Tomorrow\'s Weather')
        ax1.set_ylabel('Today\'s Weather')
        ax1.set_title('Transition Matrix')
        
        # Add values
        for i in range(len(states)):
            for j in range(len(states)):
                text = ax1.text(j, i, f'{P[i, j]:.2f}',
                              ha="center", va="center", color="black", fontsize=10, weight='bold')
        
        plt.colorbar(im, ax=ax1)
        
        # Time series simulation
        ax2 = fig.add_subplot(122)
        current_state = 0  # Start sunny
        weather_sequence = [current_state]
        
        for day in range(365):
            next_state = np.random.choice(3, p=P[current_state])
            weather_sequence.append(next_state)
            current_state = next_state
        
        colors_map = ['gold', 'gray', 'blue']
        for i, state in enumerate(weather_sequence[:100]):
            ax2.scatter(i, state, color=colors_map[state], s=30, zorder=3)
        
        ax2.set_yticks([0, 1, 2])
        ax2.set_yticklabels(states)
        ax2.set_xlabel('Day')
        ax2.set_title('100-Day Weather Simulation')
        ax2.grid(True, alpha=0.3, axis='x')
        ax2.set_xlim([-2, 102])
        
        fig.suptitle('Markov Chain Weather Model', fontsize=14, y=0.98)


def generate_figure_8_2():
    """Figure 8.2: Stationary distribution and convergence"""
    np.random.seed(42)
    
    P = np.array([[0.7, 0.2, 0.1],
                  [0.25, 0.5, 0.25],
                  [0.1, 0.4, 0.5]])
    
    states = ['Sunny', 'Cloudy', 'Rainy']
    
    with figure(3, 8, 2, output_dir=OUTPUT_DIR) as fig:
        # Stationary distribution
        ax1 = fig.add_subplot(121)
        
        # Compute stationary distribution
        eigenvalues, eigenvectors = np.linalg.eig(P.T)
        stationary = np.real(eigenvectors[:, 0])
        stationary = stationary / stationary.sum()
        
        colors = ['gold', 'gray', 'blue']
        ax1.bar(states, stationary, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        ax1.set_ylabel('Probability')
        ax1.set_title('Stationary Distribution')
        ax1.set_ylim([0, 0.6])
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add values on bars
        for i, (state, val) in enumerate(zip(states, stationary)):
            ax1.text(i, val + 0.02, f'{val:.3f}', ha='center', fontsize=10, weight='bold')
        
        # Convergence from different starting points
        ax2 = fig.add_subplot(122)
        
        time_steps = np.arange(0, 101)
        for start_state in range(3):
            initial = np.zeros(3)
            initial[start_state] = 1.0
            
            convergence = []
            for t in time_steps:
                P_power = np.linalg.matrix_power(P, t)
                prob = initial @ P_power
                convergence.append(prob[start_state])
            
            ax2.plot(time_steps, convergence, marker='', linewidth=2.5,
                    label=f'Start: {states[start_state]}', color=colors[start_state])
        
        ax2.axhline(y=stationary[0], color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
        ax2.set_xlabel('Time Steps')
        ax2.set_ylabel('Probability of Current State')
        ax2.set_title('Convergence to Stationary Distribution')
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim([0, 1])
        
        fig.suptitle('Long-Run Behavior of Markov Chains', fontsize=14, y=0.98)


def generate_figure_8_3():
    """Figure 8.3: Applications of Markov chains"""
    np.random.seed(42)
    
    with figure(3, 8, 3, output_dir=OUTPUT_DIR) as fig:
        # DNA sequence evolution
        ax1 = fig.add_subplot(131)
        dna_states = ['A', 'T', 'G', 'C']
        P_dna = np.array([[0.6, 0.1, 0.2, 0.1],
                         [0.1, 0.7, 0.1, 0.1],
                         [0.2, 0.1, 0.6, 0.1],
                         [0.1, 0.1, 0.1, 0.7]])
        
        im1 = ax1.imshow(P_dna, cmap='Greens', aspect='auto', vmin=0, vmax=1)
        ax1.set_xticks(np.arange(4))
        ax1.set_yticks(np.arange(4))
        ax1.set_xticklabels(dna_states)
        ax1.set_yticklabels(dna_states)
        ax1.set_title('DNA Evolution')
        ax1.set_xlabel('Next Base')
        ax1.set_ylabel('Current Base')
        
        # Queue system (M/M/1)
        ax2 = fig.add_subplot(132)
        queue_depths = np.arange(0, 6)
        queue_probs = np.array([0.25, 0.19, 0.14, 0.11, 0.08, 0.06])
        ax2.bar(queue_depths, queue_probs, color='coral', alpha=0.7, edgecolor='black', linewidth=1.5)
        ax2.set_xlabel('Queue Length')
        ax2.set_ylabel('Steady-State Probability')
        ax2.set_title('Queue System')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Page rank (simplified)
        ax3 = fig.add_subplot(133)
        pages = ['Page A', 'Page B', 'Page C', 'Page D']
        pagerank = np.array([0.35, 0.25, 0.20, 0.20])
        colors_rank = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        ax3.barh(pages, pagerank, color=colors_rank, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax3.set_xlabel('PageRank Score')
        ax3.set_title('Web Graph (PageRank)')
        ax3.set_xlim([0, 0.4])
        ax3.grid(True, alpha=0.3, axis='x')
        
        # Add values
        for i, val in enumerate(pagerank):
            ax3.text(val + 0.01, i, f'{val:.2f}', va='center', fontsize=9)
        
        fig.suptitle('Applications of Markov Chains', fontsize=14, y=0.98)


def main():
    print("Generating Chapter 8 figures...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print('Figure 8.1: Weather Model'); generate_figure_8_1()
    print(f"✓ Saved figure: {OUTPUT_DIR}/8.1.png")
    print('Figure 8.2: Stationary Distribution'); generate_figure_8_2()
    print(f"✓ Saved figure: {OUTPUT_DIR}/8.2.png")
    print('Figure 8.3: Applications'); generate_figure_8_3()
    print(f"✓ Saved figure: {OUTPUT_DIR}/8.3.png")
    print("✓ All figures generated!")


if __name__ == "__main__":
    main()
