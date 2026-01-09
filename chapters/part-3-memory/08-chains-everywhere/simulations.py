"""
Chapter 8: Chains Everywhere
Markov chain simulations: weather, games, genetics, queues.
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


# ============================================================================
# Core Markov Chain Tools
# ============================================================================

def simulate_markov_chain(P, initial_state, n_steps):
    """
    Simulate a Markov chain.
    
    Args:
        P: Transition matrix (k x k)
        initial_state: Starting state (0 to k-1)
        n_steps: Number of steps to simulate
    
    Returns:
        Array of states visited
    """
    k = P.shape[0]
    path = [initial_state]
    current = initial_state
    
    for _ in range(n_steps):
        current = np.random.choice(k, p=P[current])
        path.append(current)
    
    return np.array(path)


def stationary_distribution(P, tol=1e-8, max_iter=1000):
    """
    Compute stationary distribution by power iteration.
    
    π is such that πP = π (left eigenvector of P).
    """
    k = P.shape[0]
    pi = np.ones(k) / k  # Start with uniform
    
    for _ in range(max_iter):
        pi_new = pi @ P
        if np.allclose(pi, pi_new, atol=tol):
            break
        pi = pi_new
    
    return pi


def n_step_transition(P, n):
    """Compute n-step transition matrix P^n."""
    result = np.eye(P.shape[0])
    for _ in range(n):
        result = result @ P
    return result


def expected_steps_to_state(P, target_state, initial_state, max_steps=10000):
    """
    Estimate expected time to reach target from initial (by simulation).
    """
    times = []
    
    for _ in range(1000):  # 1000 independent simulations
        path = simulate_markov_chain(P, initial_state, max_steps)
        
        # Find first occurrence of target
        indices = np.where(path == target_state)[0]
        if len(indices) > 0:
            times.append(indices[0])  # First passage time
        else:
            times.append(max_steps)  # Didn't reach it
    
    return np.mean(times), np.std(times)


# ============================================================================
# Weather Modeling
# ============================================================================

def weather_model_basic():
    """Create a simple 3-state weather model."""
    P = np.array([[0.7, 0.2, 0.1],
                  [0.25, 0.5, 0.25],
                  [0.1, 0.4, 0.5]])
    
    states = ['Sunny', 'Cloudy', 'Rainy']
    return P, states


def fit_weather_model(weather_sequence):
    """
    Fit a Markov model to observed weather data.
    
    Args:
        weather_sequence: String or list of states ('S', 'C', 'R')
    
    Returns:
        Fitted transition matrix
    """
    state_to_idx = {'S': 0, 'C': 1, 'R': 2}
    idx_to_state = {0: 'S', 1: 'C', 2: 'R'}
    
    transitions = defaultdict(lambda: defaultdict(int))
    
    for i in range(len(weather_sequence) - 1):
        current = state_to_idx.get(weather_sequence[i], 0)
        next_state = state_to_idx.get(weather_sequence[i+1], 0)
        transitions[current][next_state] += 1
    
    # Normalize to probabilities
    P = np.zeros((3, 3))
    for i in range(3):
        total = sum(transitions[i].values())
        if total > 0:
            for j in range(3):
                P[i, j] = transitions[i][j] / total
    
    return P


def simulate_weather(P, initial_state, n_days):
    """Simulate weather for n days."""
    states = ['Sunny', 'Cloudy', 'Rainy']
    path = simulate_markov_chain(P, initial_state, n_days)
    return [states[s] for s in path]


# ============================================================================
# Chutes and Ladders (Snakes and Ladders)
# ============================================================================

def create_chutes_and_ladders_board():
    """
    Create a Chutes and Ladders board as a Markov chain.
    
    Simplified: only key chutes and ladders.
    Returns the "boost" array: boost[i] is the position you land on from i.
    """
    boost = np.arange(101)  # Default: land where you roll
    
    # Ladders (simplified selection)
    ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 51: 67, 72: 91, 80: 99}
    
    # Chutes (simplified)
    chutes = {17: 7, 19: 11, 60: 39, 63: 18, 87: 24, 93: 73, 95: 75, 98: 78}
    
    for start, end in ladders.items():
        boost[start] = end
    
    for start, end in chutes.items():
        boost[start] = end
    
    return boost


def chutes_and_ladders_transition_matrix():
    """
    Create full transition matrix for Chutes and Ladders.
    States: 0-100 (100 is absorbing, you win).
    """
    boost = create_chutes_and_ladders_board()
    P = np.zeros((101, 101))
    
    for pos in range(100):  # From each position
        for dice_roll in range(1, 7):  # Die roll 1-6
            new_pos = pos + dice_roll
            
            if new_pos >= 100:
                new_pos = 100  # Land on or past 100 = win
            else:
                new_pos = boost[new_pos]  # Apply chutes/ladders
            
            P[pos, new_pos] += 1.0 / 6.0  # Probability 1/6 for each die roll
    
    P[100, 100] = 1.0  # Absorbing state
    
    return P


def expected_turns_to_win(P, start_pos=0, n_sims=10000):
    """Estimate expected number of turns to win from start_pos."""
    turns = []
    
    for _ in range(n_sims):
        pos = start_pos
        turn = 0
        
        while pos < 100:
            # Roll die
            dice = np.random.randint(1, 7)
            pos += dice
            
            if pos >= 100:
                pos = 100
            else:
                boost = create_chutes_and_ladders_board()
                pos = boost[pos]
            
            turn += 1
        
        turns.append(turn)
    
    return np.mean(turns), np.std(turns)


# ============================================================================
# DNA Mutation Model
# ============================================================================

def dna_mutation_matrix(mutation_rate):
    """
    Create a 4-state Markov chain for DNA nucleotides.
    
    States: 0=A, 1=T, 2=G, 3=C
    """
    P = np.zeros((4, 4))
    
    for i in range(4):
        P[i, i] = 1 - 3 * mutation_rate  # Stay same
        for j in range(4):
            if i != j:
                P[i, j] = mutation_rate  # Mutate to each other equally
    
    return P


def simulate_dna_sequence(initial_seq, P, n_generations):
    """
    Simulate DNA sequence evolution.
    
    Args:
        initial_seq: String like "ATGC..."
        P: Mutation transition matrix
        n_generations: Number of generations to simulate
    
    Returns:
        Array of sequences, one per generation
    """
    nucleotides = ['A', 'T', 'G', 'C']
    state_to_idx = {n: i for i, n in enumerate(nucleotides)}
    
    # Convert initial sequence to state indices
    seq = [state_to_idx[n] for n in initial_seq]
    sequences = [''.join(nucleotides[s] for s in seq)]
    
    for _ in range(n_generations):
        # Each position mutates independently
        new_seq = []
        for state in seq:
            new_state = np.random.choice(4, p=P[state])
            new_seq.append(new_state)
        seq = new_seq
        sequences.append(''.join(nucleotides[s] for s in seq))
    
    return sequences


def hamming_distance(seq1, seq2):
    """Count the number of differing positions."""
    return sum(c1 != c2 for c1, c2 in zip(seq1, seq2))


# ============================================================================
# M/M/1 Queue Model
# ============================================================================

def mm1_queue_model(arrival_rate, service_rate, max_customers=100):
    """
    Create a Markov chain for M/M/1 queue.
    
    States: number of customers in system (0 to max_customers)
    
    Args:
        arrival_rate: λ (customers per unit time)
        service_rate: μ (customers per unit time)
        max_customers: Truncate state space here
    
    Returns:
        Transition matrix
    """
    P = np.zeros((max_customers + 1, max_customers + 1))
    
    # Normalize rates to probabilities
    # Assuming unit time step
    p_arrival = arrival_rate / (arrival_rate + service_rate)
    p_service = service_rate / (arrival_rate + service_rate)
    
    for n in range(max_customers + 1):
        if n == 0:
            # No customer: only arrival possible
            P[0, 1] = 1.0  # Customer arrives
        elif n == max_customers:
            # At capacity: only service possible
            P[n, n-1] = 1.0  # Customer leaves
        else:
            # Interior: can arrive or be served
            P[n, n+1] = p_arrival  # Arrival
            P[n, n-1] = p_service  # Service
            P[n, n] = 1 - p_arrival - p_service  # No change
    
    return P


def simulate_mm1_queue(arrival_rate, service_rate, n_customers):
    """
    Simulate an M/M/1 queue.
    
    Returns:
        Queue_lengths: Array of queue lengths over time
        Wait_times: Wait time for each customer
    """
    queue_lengths = [0]
    wait_times = []
    current_queue = 0
    
    for _ in range(n_customers):
        # Customer arrives
        current_queue += 1
        
        # Service time (exponential)
        # Approximation: with rate μ, expected service = 1/μ
        service_time = np.random.exponential(1.0 / service_rate)
        wait_times.append(service_time)
        
        # Customer leaves
        current_queue -= 1
        queue_lengths.append(current_queue)
    
    return queue_lengths, wait_times


def theoretical_mm1_statistics(arrival_rate, service_rate):
    """
    Compute theoretical statistics for M/M/1 queue.
    
    Returns:
        rho: Utilization (λ/μ)
        avg_customers: Average number in system
        avg_wait: Average wait time
    """
    rho = arrival_rate / service_rate
    
    if rho >= 1:
        return rho, float('inf'), float('inf')  # Unstable
    
    avg_customers = rho / (1 - rho)
    avg_wait = 1 / (service_rate - arrival_rate)
    
    return rho, avg_customers, avg_wait


# ============================================================================
# Visualization Functions
# ============================================================================

def plot_weather_timeseries(weather_sequence, title="Weather Over Time"):
    """Plot a weather sequence."""
    state_to_num = {'Sunny': 0, 'Cloudy': 1, 'Rainy': 2}
    nums = [state_to_num[w] for w in weather_sequence]
    
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.scatter(range(len(nums)), nums, alpha=0.5, s=10)
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(['Sunny', 'Cloudy', 'Rainy'])
    ax.set_xlabel('Days')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    
    return fig


def plot_stationary_comparison(observed_freq, stationary):
    """Compare observed vs. stationary distribution."""
    states = ['Sunny', 'Cloudy', 'Rainy']
    x = np.arange(len(states))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width/2, observed_freq, width, label='Observed', alpha=0.8)
    ax.bar(x + width/2, stationary, width, label='Stationary', alpha=0.8)
    ax.set_ylabel('Frequency')
    ax.set_title('Observed vs. Theoretical Distribution')
    ax.set_xticks(x)
    ax.set_xticklabels(states)
    ax.legend()
    
    return fig


def plot_dna_divergence(sequences, initial_seq):
    """Plot Hamming distance from initial sequence over generations."""
    distances = [hamming_distance(seq, initial_seq) for seq in sequences]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(distances, linewidth=2)
    ax.set_xlabel('Generation')
    ax.set_ylabel('Hamming Distance from Initial')
    ax.set_title('DNA Sequence Divergence')
    ax.grid(True, alpha=0.3)
    
    return fig


def plot_mm1_queue_lengths(queue_lengths):
    """Plot queue length over time."""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(queue_lengths, linewidth=1, alpha=0.7)
    ax.set_xlabel('Time')
    ax.set_ylabel('Number in Queue')
    ax.set_title('M/M/1 Queue Length Over Time')
    ax.grid(True, alpha=0.3)
    
    return fig


# ============================================================================
# Demo / Main
# ============================================================================

if __name__ == '__main__':
    print("Chapter 8: Chains Everywhere")
    print("=" * 60)
    
    # Weather
    print("\n--- Weather Model ---")
    P_weather, states = weather_model_basic()
    weather = simulate_weather(P_weather, 0, 100)
    print(f"100 days of weather: {' '.join(weather[:20])}...")
    
    pi_weather = stationary_distribution(P_weather)
    print(f"Stationary distribution: {dict(zip(states, pi_weather))}")
    
    # Chutes and Ladders
    print("\n--- Chutes and Ladders ---")
    mean_turns, std_turns = expected_turns_to_win(None, start_pos=0, n_sims=10000)
    print(f"Expected turns to win: {mean_turns:.1f} ± {std_turns:.1f}")
    
    # DNA
    print("\n--- DNA Evolution ---")
    P_dna = dna_mutation_matrix(0.01)
    pi_dna = stationary_distribution(P_dna)
    print(f"Stationary DNA distribution: {pi_dna}")
    
    sequences = simulate_dna_sequence("ATGATGATG", P_dna, 50)
    print(f"Initial:  {sequences[0]}")
    print(f"Gen 10:   {sequences[10]}")
    print(f"Gen 50:   {sequences[50]}")
    
    # M/M/1 Queue
    print("\n--- M/M/1 Queue ---")
    lambda_rate = 0.8
    mu_rate = 1.0
    rho, avg_n, avg_w = theoretical_mm1_statistics(lambda_rate, mu_rate)
    print(f"Arrival rate λ = {lambda_rate}")
    print(f"Service rate μ = {mu_rate}")
    print(f"Utilization ρ = {rho:.2f}")
    print(f"Average in system = {avg_n:.2f}")
    print(f"Average wait time = {avg_w:.2f}")
    
    print("\nDone!")
