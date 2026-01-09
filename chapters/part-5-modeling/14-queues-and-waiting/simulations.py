"""
Chapter 14: Queues and Waiting
M/M/1 and M/M/c queueing systems, arrivals, service times, and Little's Law.
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from scipy.special import factorial


# ============================================================================
# Poisson Process: Random Arrivals
# ============================================================================

def poisson_arrivals(lambda_rate, t_max):
    """
    Generate arrival times from a Poisson process with rate lambda.
    
    Args:
        lambda_rate: arrival rate (customers per unit time)
        t_max: total time period
    
    Returns:
        Array of arrival times
    """
    inter_arrival_times = np.random.exponential(1 / lambda_rate, size=1000)
    arrival_times = np.cumsum(inter_arrival_times)
    arrival_times = arrival_times[arrival_times <= t_max]
    return arrival_times


def exponential_service_time(mu):
    """
    Generate a random service time from exponential distribution with rate mu.
    
    Args:
        mu: service rate (customers per unit time)
    
    Returns:
        Service time
    """
    return np.random.exponential(1 / mu)


# ============================================================================
# M/M/1 Queue Simulation
# ============================================================================

def simulate_mm1_queue(lambda_rate, mu, t_max):
    """
    Simulate an M/M/1 queue (single server).
    
    Args:
        lambda_rate: arrival rate
        mu: service rate
        t_max: simulation time
    
    Returns:
        times, queue_lengths, wait_times (dict: customer -> wait time)
    """
    arrivals = poisson_arrivals(lambda_rate, t_max)
    
    queue = deque()  # customers waiting (arrival_time, service_duration)
    server_busy_until = 0.0
    
    times = [0.0]
    queue_lengths = [0]
    
    wait_times = {}  # customer_id -> wait time
    customer_id = 0
    
    for arrival_time in arrivals:
        # Move time forward to this arrival
        if arrival_time > times[-1]:
            times.append(arrival_time)
            queue_lengths.append(len(queue) + (1 if server_busy_until > arrival_time else 0))
        
        # Add customer to queue
        service_duration = exponential_service_time(mu)
        queue.append((arrival_time, service_duration, customer_id))
        customer_id += 1
        
        # If server is free, start serving immediately
        if server_busy_until <= arrival_time:
            _, service_dur, cid = queue.popleft()
            server_busy_until = arrival_time + service_dur
            wait_times[cid] = 0.0  # no wait
        else:
            # Server is busy, customer waits
            while queue and server_busy_until > 0:
                earliest_arrival, service_dur, cid = queue.popleft()
                wait = server_busy_until - earliest_arrival
                wait_times[cid] = max(0, wait)
                server_busy_until = server_busy_until + service_dur
    
    # Drain remaining queue
    while queue and server_busy_until > t_max:
        break
    
    return np.array(times), np.array(queue_lengths), wait_times


def simulate_mm1_discrete(lambda_rate, mu, n_events):
    """
    Simulate M/M/1 queue using discrete-event simulation.
    
    Args:
        lambda_rate: arrival rate
        mu: service rate
        n_events: number of events to simulate
    
    Returns:
        times, queue_lengths, wait_times
    """
    queue_length = 0
    server_busy = False
    
    times = [0.0]
    queue_lengths = [0]
    wait_times = []
    
    current_time = 0.0
    
    for _ in range(n_events):
        # Time until next arrival
        time_to_arrival = np.random.exponential(1 / lambda_rate)
        current_time += time_to_arrival
        
        # Arrival
        arrival_time = current_time
        queue_length += 1
        
        # If server is free, start serving
        if not server_busy:
            server_busy = True
            service_time = exponential_service_time(mu)
            current_time += service_time
            queue_length -= 1
            wait_times.append(0.0)
            server_busy = False
        
        times.append(current_time)
        queue_lengths.append(queue_length)
    
    return np.array(times), np.array(queue_lengths), np.array(wait_times)


# ============================================================================
# M/M/c Queue (Multiple Servers)
# ============================================================================

def simulate_mmc_queue(lambda_rate, mu, c, t_max):
    """
    Simulate an M/M/c queue (c servers).
    
    Args:
        lambda_rate: arrival rate
        mu: service rate per server
        c: number of servers
        t_max: simulation time
    
    Returns:
        times, queue_lengths, wait_times
    """
    arrivals = poisson_arrivals(lambda_rate, t_max)
    
    queue = deque()  # customers waiting
    server_free_at = np.zeros(c)  # when each server becomes free
    
    times = [0.0]
    queue_lengths = [0]
    wait_times = {}
    customer_id = 0
    
    for arrival_time in arrivals:
        # Record time and queue state
        if arrival_time > times[-1]:
            times.append(arrival_time)
            busy_servers = np.sum(server_free_at > arrival_time)
            queue_lengths.append(len(queue) + busy_servers)
        
        # Find the next free server
        earliest_free_idx = np.argmin(server_free_at)
        earliest_free_time = server_free_at[earliest_free_idx]
        
        service_duration = exponential_service_time(mu)
        
        if earliest_free_time <= arrival_time:
            # Server is available now
            wait = 0.0
            server_free_at[earliest_free_idx] = arrival_time + service_duration
        else:
            # Customer must wait
            wait = earliest_free_time - arrival_time
            server_free_at[earliest_free_idx] = earliest_free_time + service_duration
        
        wait_times[customer_id] = wait
        customer_id += 1
    
    return np.array(times), np.array(queue_lengths), wait_times


# ============================================================================
# Queue Statistics
# ============================================================================

def compute_queue_statistics(queue_lengths, times):
    """
    Compute average queue length using time-weighted average.
    
    Args:
        queue_lengths: queue length at each event
        times: time of each event
    
    Returns:
        Average queue length
    """
    if len(queue_lengths) < 2:
        return 0.0
    
    avg_queue = 0.0
    for i in range(len(queue_lengths) - 1):
        time_interval = times[i+1] - times[i]
        avg_queue += queue_lengths[i] * time_interval
    
    total_time = times[-1] - times[0]
    if total_time > 0:
        avg_queue /= total_time
    
    return avg_queue


def littles_law_check(lambda_rate, avg_queue_length, avg_wait_time):
    """
    Verify Little's Law: L = λW
    
    Args:
        lambda_rate: arrival rate
        avg_queue_length: average queue length (L)
        avg_wait_time: average wait time (W)
    
    Returns:
        Expected L (from Little's Law) and observed L
    """
    expected_L = lambda_rate * avg_wait_time
    return expected_L


def theoretical_mm1_queue_length(rho):
    """
    Theoretical average queue length for M/M/1.
    
    L = ρ / (1 - ρ)
    
    Args:
        rho: utilization = λ/μ
    
    Returns:
        Average queue length
    """
    if rho >= 1:
        return np.inf
    return rho / (1 - rho)


def theoretical_mm1_wait_time(rho, mu):
    """
    Theoretical average wait time for M/M/1.
    
    W = 1 / (μ(1 - ρ))
    
    Args:
        rho: utilization
        mu: service rate
    
    Returns:
        Average wait time
    """
    if rho >= 1:
        return np.inf
    return 1 / (mu * (1 - rho))


def mm1_stationary_distribution(rho, n_max=50):
    """
    Compute stationary distribution for M/M/1.
    
    P(n) = (1 - ρ) ρ^n
    
    Args:
        rho: utilization
        n_max: maximum queue length to compute
    
    Returns:
        Array of probabilities P(n) for n = 0, 1, ..., n_max
    """
    if rho >= 1:
        return None
    
    n = np.arange(n_max + 1)
    probs = (1 - rho) * rho ** n
    return probs


# ============================================================================
# Visualization
# ============================================================================

def plot_queue_dynamics(lambda_rate, mu, t_max=100, title="M/M/1 Queue"):
    """Plot queue length and wait times over time."""
    times, queue_lengths, wait_times = simulate_mm1_queue(lambda_rate, mu, t_max)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Queue length over time
    ax1.step(times, queue_lengths, where='post', linewidth=1.5)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Queue Length')
    ax1.set_title(f'{title}: Queue Length over Time (λ={lambda_rate}, μ={mu})')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(ymin=0)
    
    # Wait time histogram
    if wait_times:
        waits = np.array(list(wait_times.values()))
        ax2.hist(waits, bins=30, density=True, alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Wait Time')
        ax2.set_ylabel('Density')
        ax2.set_title(f'{title}: Distribution of Wait Times')
        ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig


def plot_utilization_effect(mu=1.0):
    """Plot how waiting time increases with utilization."""
    lambda_rates = np.linspace(0.1, 0.95, 20) * mu
    avg_waits = []
    
    for lam in lambda_rates:
        rho = lam / mu
        if rho < 0.99:
            wait = theoretical_mm1_wait_time(rho, mu)
            avg_waits.append(wait)
        else:
            avg_waits.append(np.nan)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    rhos = lambda_rates / mu
    ax.plot(rhos, avg_waits, 'bo-', linewidth=2, markersize=8)
    ax.set_xlabel('Utilization (ρ = λ/μ)')
    ax.set_ylabel('Average Wait Time (1/(μ(1-ρ)))')
    ax.set_title('M/M/1: How Wait Time Explodes Near Capacity')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(ymin=0, ymax=10)
    
    return fig


def plot_single_vs_multiple_servers(lambda_rate, mu, t_max=100):
    """Compare single server vs. multiple servers."""
    # M/M/1: all traffic to one server
    times1, queue1, waits1 = simulate_mm1_queue(lambda_rate, mu, t_max)
    avg_queue1 = compute_queue_statistics(queue1, times1)
    avg_wait1 = np.mean(list(waits1.values())) if waits1 else 0
    
    # M/M/2: traffic split between two servers
    times2, queue2, waits2 = simulate_mmc_queue(lambda_rate, mu, 2, t_max)
    avg_queue2 = compute_queue_statistics(queue2, times2)
    avg_wait2 = np.mean(list(waits2.values())) if waits2 else 0
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Queue length comparison
    ax1.step(times1, queue1, where='post', label='1 Server (M/M/1)', linewidth=1.5)
    ax1.step(times2, queue2, where='post', label='2 Servers (M/M/2)', linewidth=1.5, alpha=0.7)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Queue Length')
    ax1.set_title(f'Queue Length: Single vs. Multiple Servers')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(ymin=0)
    
    # Wait time histograms
    if waits1 and waits2:
        waits1_array = np.array(list(waits1.values()))
        waits2_array = np.array(list(waits2.values()))
        ax2.hist(waits1_array, bins=20, density=True, alpha=0.6, label=f'1 Server (mean={avg_wait1:.2f})', edgecolor='black')
        ax2.hist(waits2_array, bins=20, density=True, alpha=0.6, label=f'2 Servers (mean={avg_wait2:.2f})', edgecolor='black')
        ax2.set_xlabel('Wait Time')
        ax2.set_ylabel('Density')
        ax2.set_title('Distribution of Wait Times')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
    
    return fig


def plot_stationary_distribution(rho):
    """Plot the stationary queue length distribution for M/M/1."""
    if rho >= 1:
        print("Error: ρ must be < 1")
        return None
    
    probs = mm1_stationary_distribution(rho, n_max=30)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    n = np.arange(len(probs))
    ax.bar(n, probs, alpha=0.7, edgecolor='black')
    ax.set_xlabel('Queue Length (n)')
    ax.set_ylabel('Probability P(n) = (1-ρ)ρⁿ')
    ax.set_title(f'M/M/1 Stationary Distribution (ρ={rho:.2f})')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Expected queue length
    expected = theoretical_mm1_queue_length(rho)
    ax.axvline(expected, color='r', linestyle='--', linewidth=2, label=f'E[N] = {expected:.2f}')
    ax.legend()
    
    return fig


# ============================================================================
# Demo / Main
# ============================================================================

if __name__ == '__main__':
    print("Chapter 14: Queues and Waiting")
    print("=" * 60)
    
    lambda_rate = 0.8
    mu = 1.0
    t_max = 1000
    rho = lambda_rate / mu
    
    print(f"\nParameters:")
    print(f"  Arrival rate: λ = {lambda_rate}")
    print(f"  Service rate: μ = {mu}")
    print(f"  Utilization: ρ = λ/μ = {rho:.2f}")
    
    # Theoretical values
    print(f"\n--- Theoretical M/M/1 ---")
    theoretical_queue = theoretical_mm1_queue_length(rho)
    theoretical_wait = theoretical_mm1_wait_time(rho, mu)
    print(f"  Average queue length L = ρ/(1-ρ) = {theoretical_queue:.2f}")
    print(f"  Average wait time W = 1/(μ(1-ρ)) = {theoretical_wait:.2f}")
    print(f"  P(queue empty) = 1 - ρ = {1 - rho:.2f}")
    
    # Simulation
    print(f"\n--- Simulation ---")
    times, queue_lengths, wait_times = simulate_mm1_queue(lambda_rate, mu, t_max)
    simulated_queue = compute_queue_statistics(queue_lengths, times)
    simulated_waits = np.array(list(wait_times.values()))
    simulated_avg_wait = np.mean(simulated_waits)
    
    print(f"  Average queue length: {simulated_queue:.2f}")
    print(f"  Average wait time: {simulated_avg_wait:.2f}")
    print(f"  Total customers: {len(wait_times)}")
    
    # Little's Law check
    print(f"\n--- Little's Law Verification ---")
    expected_L = littles_law_check(lambda_rate, simulated_queue, simulated_avg_wait)
    print(f"  Expected L = λ × W = {lambda_rate:.2f} × {simulated_avg_wait:.2f} = {expected_L:.2f}")
    print(f"  Observed L = {simulated_queue:.2f}")
    print(f"  Match: {abs(expected_L - simulated_queue) < 0.5}")
    
    # Compare with 2-server system
    print(f"\n--- M/M/2 (2 Servers) ---")
    times2, queue2, waits2 = simulate_mmc_queue(lambda_rate, mu, 2, t_max)
    queue2_avg = compute_queue_statistics(queue2, times2)
    waits2_avg = np.mean(list(waits2.values())) if waits2 else 0
    print(f"  Average queue length: {queue2_avg:.2f}")
    print(f"  Average wait time: {waits2_avg:.2f}")
    print(f"  Improvement vs. 1 server: {(simulated_queue - queue2_avg) / simulated_queue * 100:.0f}% less queue")
    
    print("\nDone!")
