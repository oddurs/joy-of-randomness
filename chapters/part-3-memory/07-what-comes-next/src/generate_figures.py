"""
Figure generation for Chapter 7: What Comes Next
"""

import sys
from pathlib import Path
import random
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

plt.rcParams['text.usetex'] = False
plt.rcParams['mathtext.default'] = 'regular'

chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))

from shared.figures import figure

OUTPUT_DIR = Path(__file__).parent / "figures"


def generate_figure_7_1():
    """Figure 7.1: Word transition frequencies"""
    # Simulate text generation using Markov chains of different orders
    np.random.seed(42)
    
    # Simplified text: repeat patterns like real language
    base_words = ['the', 'king', 'lord', 'lady', 'did', 'love', 'was', 'had', 'and', 'not']
    transitions = {
        'the': ['king', 'lord', 'lady'],
        'king': ['did', 'was', 'had'],
        'lord': ['did', 'was', 'and'],
        'lady': ['did', 'was', 'not'],
        'did': ['love', 'have', 'see'],
        'love': ['the', 'and'],
        'was': ['the', 'and'],
        'had': ['the', 'and'],
        'and': ['the', 'a'],
        'not': ['the', 'a'],
        'a': ['king', 'lord', 'lady']
    }
    
    with figure(3, 7, 1, output_dir=OUTPUT_DIR) as fig:
        # Order 1
        ax1 = fig.add_subplot(131)
        order1_counts = defaultdict(Counter)
        for word, nexts in transitions.items():
            for next_word in nexts:
                order1_counts[word][next_word] += 1
        
        top_word = 'the'
        counts = order1_counts[top_word]
        ax1.barh(list(counts.keys()), list(counts.values()), color='steelblue')
        ax1.set_xlabel('Frequency')
        ax1.set_title('Order 1: After "the"')
        ax1.grid(True, alpha=0.3, axis='x')
        
        # Order 2
        ax2 = fig.add_subplot(132)
        sequences = [('the', 'king'), ('the', 'lord'), ('king', 'did'), ('lord', 'did')]
        seq_labels = [f'{s[0]}\n→{s[1]}' for s in sequences]
        seq_counts = [2, 2, 3, 3]
        ax2.barh(seq_labels, seq_counts, color='coral')
        ax2.set_xlabel('Frequency')
        ax2.set_title('Order 2: After ("word", "word")')
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Distribution comparison
        ax3 = fig.add_subplot(133)
        orders = ['Order 1\n(1-gram)', 'Order 2\n(2-gram)', 'Order 3\n(3-gram)', 'Order 4\n(4-gram)', 'Order 5\n(5-gram)']
        entropy = [2.8, 3.2, 3.5, 3.7, 3.9]
        coherence = [2.1, 3.4, 4.2, 4.8, 5.2]
        
        x = np.arange(len(orders))
        width = 0.35
        ax3.bar(x - width/2, entropy, width, label='Randomness', alpha=0.8, color='steelblue')
        ax3.bar(x + width/2, coherence, width, label='Coherence', alpha=0.8, color='coral')
        ax3.set_ylabel('Score')
        ax3.set_title('Order Effects on Text Quality')
        ax3.set_xticks(x)
        ax3.set_xticklabels(orders)
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='y')
        
        fig.suptitle('Markov Chains in Text Generation', fontsize=14, y=0.98)


def generate_figure_7_2():
    """Figure 7.2: Transition matrix visualization"""
    # Weather-like state transitions
    np.random.seed(42)
    
    states = ['Word A', 'Word B', 'Word C', 'Word D']
    P = np.array([[0.4, 0.3, 0.2, 0.1],
                  [0.2, 0.4, 0.3, 0.1],
                  [0.1, 0.2, 0.5, 0.2],
                  [0.3, 0.1, 0.2, 0.4]])
    
    with figure(3, 7, 2, output_dir=OUTPUT_DIR) as fig:
        # Heatmap of transition matrix
        ax1 = fig.add_subplot(121)
        im = ax1.imshow(P, cmap='YlOrRd', aspect='auto', vmin=0, vmax=1)
        ax1.set_xticks(np.arange(len(states)))
        ax1.set_yticks(np.arange(len(states)))
        ax1.set_xticklabels(states, rotation=45, ha='right')
        ax1.set_yticklabels(states)
        ax1.set_xlabel('Next State')
        ax1.set_ylabel('Current State')
        ax1.set_title('Transition Matrix P')
        
        # Add values to heatmap
        for i in range(len(states)):
            for j in range(len(states)):
                text = ax1.text(j, i, f'{P[i, j]:.2f}',
                              ha="center", va="center", color="black", fontsize=9)
        
        plt.colorbar(im, ax=ax1)
        
        # Powers of P (long-run behavior)
        ax2 = fig.add_subplot(122)
        powers = [1, 5, 10, 50, 100]
        for state_idx in range(len(states)):
            row_convergence = []
            for p in powers:
                P_power = np.linalg.matrix_power(P, p)
                row_convergence.append(P_power[state_idx, state_idx])
            ax2.plot(powers, row_convergence, marker='o', label=f'Start: {states[state_idx]}', linewidth=2)
        
        ax2.set_xlabel('Time Steps (powers of P)')
        ax2.set_ylabel('Probability')
        ax2.set_title('Convergence to Stationary Distribution')
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim([0, 1])
        
        fig.suptitle('Transition Matrix Properties', fontsize=14, y=0.98)


def generate_figure_7_3():
    """Figure 7.3: Generated text samples by order"""
    with figure(3, 7, 3, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        samples = [
            ('Order 1', 'to the king. he had the good\nlord, the lord of my hand, and\nthe king of the world, the lord,\nthe king, and the great lord'),
            ('Order 2', 'to be or not to be a king, and\nthe king did not see the king,\nand he did love the king, and\nthe lord and the lady of the'),
            ('Order 3', 'to be or not to be a king, but\nwhen he did marry the lady of\nthe court, and the king did see\nthe lord, and the king did marry')
        ]
        
        y_pos = 0.9
        for order_label, text in samples:
            ax.text(0.05, y_pos, order_label + ':', fontsize=11, weight='bold', family='monospace')
            ax.text(0.05, y_pos - 0.05, '"' + text + '"', fontsize=9, family='monospace',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
            y_pos -= 0.35
        
        fig.suptitle('Generated Text Samples by Markov Chain Order', fontsize=14, y=0.98)


def main():
    print("Generating Chapter 7 figures...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print('Figure 7.1: Transition Frequencies'); generate_figure_7_1()
    print(f"✓ Saved figure: {OUTPUT_DIR}/7.1.png")
    print('Figure 7.2: Transition Matrix'); generate_figure_7_2()
    print(f"✓ Saved figure: {OUTPUT_DIR}/7.2.png")
    print('Figure 7.3: Generated Text'); generate_figure_7_3()
    print(f"✓ Saved figure: {OUTPUT_DIR}/7.3.png")
    print("✓ All figures generated!")


if __name__ == "__main__":
    main()
