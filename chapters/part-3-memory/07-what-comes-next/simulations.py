"""
Chapter 7: What Comes Next?
Markov chains, text generation, and entropy estimation.
"""

import numpy as np
import re
from collections import defaultdict, Counter
import matplotlib.pyplot as plt


# ============================================================================
# Core Functions: Building and Using Markov Chains
# ============================================================================

def load_text(text_string):
    """Load and preprocess text from a string."""
    text = text_string.lower()
    words = re.findall(r'\b\w+\b', text)
    return words


def build_transition_matrix(words, order=1):
    """
    Build a Markov chain transition matrix.
    
    Args:
        words: List of words
        order: Order of the chain (1, 2, 3, ...)
    
    Returns:
        transitions: dict mapping states to Counter of next words
    """
    transitions = defaultdict(Counter)
    
    for i in range(len(words) - order):
        if order == 1:
            state = words[i]
        else:
            state = tuple(words[i:i+order])
        
        next_word = words[i + order]
        transitions[state][next_word] += 1
    
    return transitions


def generate_text(transitions, start_state, length=100, order=1):
    """
    Generate text using a Markov chain.
    
    Args:
        transitions: Transition dictionary
        start_state: Starting word or tuple of words
        length: Number of words to generate
        order: Order of the chain
    
    Returns:
        Generated text as a string
    """
    if order == 1:
        state = start_state
        words = [state]
    else:
        state = start_state if isinstance(start_state, tuple) else tuple(start_state)
        words = list(state)
    
    for _ in range(length - order):
        if state not in transitions:
            break
        
        next_words_counter = transitions[state]
        if not next_words_counter:
            break
        
        candidates = list(next_words_counter.elements())
        next_word = np.random.choice(candidates)
        words.append(next_word)
        
        if order == 1:
            state = next_word
        else:
            state = (state[1:] + (next_word,)) if order > 1 else next_word
    
    return ' '.join(words)


def compute_entropy(transitions, order=1):
    """
    Compute Shannon entropy of a Markov chain (in bits per transition).
    
    Args:
        transitions: Transition dictionary
        order: Order of the chain (for reference/documentation)
    
    Returns:
        entropy: Entropy in bits
    """
    total_entropy = 0.0
    total_count = 0
    
    for state, next_words in transitions.items():
        state_total = sum(next_words.values())
        
        for next_word, count in next_words.items():
            prob = count / state_total
            if prob > 0:
                total_entropy -= prob * np.log2(prob)
            total_count += count
    
    return total_entropy


def perplexity(transitions, test_words, order=1):
    """
    Compute perplexity of a test sequence under the model.
    
    Perplexity = 2^(-average_log_prob)
    Lower is better (more predictable)
    """
    log_prob_sum = 0.0
    count = 0
    
    for i in range(len(test_words) - order):
        if order == 1:
            state = test_words[i]
        else:
            state = tuple(test_words[i:i+order])
        
        next_word = test_words[i + order]
        
        if state in transitions:
            next_words = transitions[state]
            state_total = sum(next_words.values())
            
            if next_word in next_words:
                prob = next_words[next_word] / state_total
                log_prob_sum += np.log2(prob)
        
        count += 1
    
    if count == 0:
        return float('inf')
    
    return 2.0 ** (-log_prob_sum / count)


# ============================================================================
# Analysis Functions
# ============================================================================

def compare_orders(words, orders=[1, 2, 3], test_fraction=0.2):
    """
    Build and compare Markov chains of different orders.
    
    Returns:
        results: dict with entropy and perplexity for each order
    """
    split_idx = int(len(words) * (1 - test_fraction))
    train_words = words[:split_idx]
    test_words = words[split_idx:]
    
    results = {}
    
    for order in orders:
        trans = build_transition_matrix(train_words, order=order)
        entropy = compute_entropy(trans, order=order)
        perp = perplexity(trans, test_words, order=order)
        
        num_states = len(trans)
        num_transitions = sum(sum(c.values()) for c in trans.values())
        
        results[order] = {
            'entropy': entropy,
            'perplexity': perp,
            'num_states': num_states,
            'num_transitions': num_transitions,
            'transitions': trans
        }
    
    return results


def vocabulary_size_growth(words, max_order=5):
    """
    Show how vocabulary (number of states) grows with order.
    """
    growth = {}
    
    for order in range(1, max_order + 1):
        trans = build_transition_matrix(words, order=order)
        growth[order] = len(trans)
    
    return growth


# ============================================================================
# Visualization Functions
# ============================================================================

def plot_entropy_by_order(results):
    """Plot entropy as a function of order."""
    orders = sorted(results.keys())
    entropies = [results[o]['entropy'] for o in orders]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(orders, entropies, 'o-', linewidth=2, markersize=8)
    ax.set_xlabel('Chain Order')
    ax.set_ylabel('Entropy (bits per transition)')
    ax.set_title('Entropy vs. Markov Chain Order')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(orders)
    
    return fig


def plot_perplexity_by_order(results):
    """Plot perplexity as a function of order."""
    orders = sorted(results.keys())
    perplexities = [results[o]['perplexity'] for o in orders]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.semilogy(orders, perplexities, 'o-', linewidth=2, markersize=8, color='red')
    ax.set_xlabel('Chain Order')
    ax.set_ylabel('Perplexity (log scale)')
    ax.set_title('Perplexity vs. Markov Chain Order')
    ax.grid(True, alpha=0.3, which='both')
    ax.set_xticks(orders)
    
    return fig


def plot_state_growth(growth):
    """Plot vocabulary growth with order."""
    orders = sorted(growth.keys())
    sizes = [growth[o] for o in orders]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.loglog(orders, sizes, 'o-', linewidth=2, markersize=8, color='green')
    ax.set_xlabel('Chain Order')
    ax.set_ylabel('Number of States (log scale)')
    ax.set_title('Vocabulary/State Space Growth')
    ax.grid(True, alpha=0.3, which='both')
    ax.set_xticks(orders)
    
    return fig


# ============================================================================
# Demo / Main
# ============================================================================

if __name__ == '__main__':
    # Sample text (short for demo; would be larger in practice)
    sample_text = """
    to be or not to be that is the question whether tis nobler in the mind
    to suffer the slings and arrows of outrageous fortune or to take arms against
    a sea of troubles and by opposing end them to die to sleep no more
    """
    
    print("Chapter 7: What Comes Next?")
    print("=" * 50)
    
    words = load_text(sample_text)
    print(f"Loaded {len(words)} words, {len(set(words))} unique")
    
    # Compare orders
    print("\nComparing Markov chain orders:")
    results = compare_orders(words, orders=[1, 2, 3])
    
    for order in sorted(results.keys()):
        r = results[order]
        print(f"\nOrder {order}:")
        print(f"  Entropy: {r['entropy']:.3f} bits/transition")
        print(f"  Perplexity: {r['perplexity']:.2f}")
        print(f"  States: {r['num_states']}")
    
    # Generate samples
    print("\n" + "=" * 50)
    print("Generated text samples:")
    
    for order in [1, 2, 3]:
        trans = results[order]['transitions']
        if order == 1:
            start = 'to'
        else:
            start = ('to', 'be')
        
        generated = generate_text(trans, start, length=30, order=order)
        print(f"\nOrder {order}: {generated}")
    
    # State space growth
    print("\n" + "=" * 50)
    growth = vocabulary_size_growth(words, max_order=4)
    print("Vocabulary growth with order:")
    for order, size in growth.items():
        print(f"  Order {order}: {size} states")
    
    print("\nDone!")
