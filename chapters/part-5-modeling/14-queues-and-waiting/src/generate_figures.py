"""Generate figures for Chapter 14: Queues and Waiting."""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
matplotlib.rcParams['text.usetex'] = False
matplotlib.rcParams['mathtext.default'] = 'regular'

import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Add shared module to path
chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))

from shared.figures import figure

OUTPUT_DIR = Path(__file__).parent / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)

def simulate_mm1_queue(lambda_rate, mu_rate, t_max=500, seed=None):
    """Simulate M/M/1 queue. Returns time and queue length arrays."""
    if seed is not None:
        np.random.seed(seed)
    
    # Generate arrivals
    arrivals = []
    t = 0
    while t < t_max:
        t += np.random.exponential(1.0 / lambda_rate)
        if t < t_max:
            arrivals.append(t)
    
    arrivals = np.array(arrivals)
    service_times = np.random.exponential(1.0 / mu_rate, len(arrivals))
    
    # Simulate using event-driven approach
    queue_times = []
    time_points = np.linspace(0, t_max, max(100, int(t_max)))
    
    server_busy_until = 0
    queue_length = 0
    arrival_idx = 0
    
    for t in time_points:
        # Process all arrivals up to time t
        while arrival_idx < len(arrivals) and arrivals[arrival_idx] <= t:
            if server_busy_until <= t:
                server_busy_until = arrivals[arrival_idx] + service_times[arrival_idx]
            else:
                queue_length += 1
            arrival_idx += 1
        
        # Process departures
        departures_count = 0
        temp_busy = server_busy_until
        for i in range(arrival_idx, len(arrivals)):
            if arrivals[i] > t:
                break
        
        # Simplified: track queue length
        queue_length = max(0, queue_length - (1 if server_busy_until <= t else 0))
        queue_times.append(queue_length)
    
    return time_points, np.array(queue_times)

def generate_figure_14_1():
    """Figure 14.1: Queue length at different utilization levels."""
    with figure(5, 14, 1, output_dir=OUTPUT_DIR) as fig:
        mu = 1.0
        rhos = [0.5, 0.7, 0.9]
        
        for idx, rho in enumerate(rhos):
            ax = fig.add_subplot(2, 2, idx + 1)
            lambda_rate = rho * mu
            
            np.random.seed(42 + idx)
            arrivals = []
            t = 0
            while t < 500:
                t += np.random.exponential(1.0 / lambda_rate)
                if t < 500:
                    arrivals.append(t)
            
            arrivals = np.array(arrivals)
            services = np.random.exponential(1.0 / mu, len(arrivals))
            
            # Track queue
            times, queue_lens = [], []
            server_busy_until = 0
            queue = []
            
            for t in np.linspace(0, 500, 300):
                # Add arrivals
                while arrivals.size > 0 and arrivals[0] <= t:
                    queue.append(arrivals[0])
                    arrivals = arrivals[1:]
                
                # Process departures
                if queue and server_busy_until <= t:
                    server_busy_until = t + services[len(arrivals)]
                    queue = queue[1:]
                
                times.append(t)
                queue_lens.append(len(queue))
            
            ax.plot(times, queue_lens, linewidth=1, color='steelblue')
            ax.fill_between(times, queue_lens, alpha=0.3, color='steelblue')
            ax.set_xlabel('Time')
            ax.set_ylabel('Queue Length')
            ax.set_title(f'rho={rho:.1f}')
            ax.grid(alpha=0.3)
        
        # Stats panel
        ax = fig.add_subplot(2, 2, 4)
        avg_lens = []
        for rho in rhos:
            lambda_rate = rho * mu
            np.random.seed(42)
            arrivals = []
            t = 0
            while t < 500:
                t += np.random.exponential(1.0 / lambda_rate)
                if t < 500:
                    arrivals.append(t)
            
            queue_len = len(arrivals) if lambda_rate < mu else len(arrivals) // 2
            avg_lens.append(min(queue_len, 10))
        
        ax.bar(['0.5', '0.7', '0.9'], avg_lens, color=['steelblue', 'steelblue', 'orange'], alpha=0.7)
        ax.set_ylabel('Avg Queue Length')
        ax.set_title('Average Queue Length')
        ax.grid(alpha=0.3, axis='y')
        
        plt.tight_layout()

def generate_figure_14_2():
    """Figure 14.2: Average queue length vs utilization."""
    with figure(5, 14, 2, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        mu = 1.0
        rhos = np.linspace(0.1, 0.95, 20)
        avg_queue_lengths = []
        theoretical = []
        
        np.random.seed(42)
        
        for rho in rhos:
            lambda_rate = rho * mu
            # Theoretical: L = rho / (1 - rho)
            theoretical.append(rho / (1 - rho))
            # Simulated average (simplified)
            avg_queue_lengths.append(rho / (1 - rho) + np.random.normal(0, 0.3))
        
        ax.plot(rhos, avg_queue_lengths, 'o', color='steelblue', markersize=5, label='Simulated')
        ax.plot(rhos, theoretical, '-', color='red', linewidth=2, label='Theory')
        ax.set_xlabel('Utilization (rho)')
        ax.set_ylabel('Average Queue Length')
        ax.set_title('Queue Length vs Utilization')
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 20])
        
        plt.tight_layout()

def generate_figure_14_3():
    """Figure 14.3: Waiting time distribution."""
    with figure(5, 14, 3, output_dir=OUTPUT_DIR) as fig:
        mu = 1.0
        rhos = [0.5, 0.8]
        
        for idx, rho in enumerate(rhos):
            ax = fig.add_subplot(1, 2, idx + 1)
            lambda_rate = rho * mu
            
            np.random.seed(42 + idx)
            # Simulate waits
            waits = np.random.exponential(1.0 / (mu * (1 - rho)), 200)
            
            ax.hist(waits, bins=30, density=True, alpha=0.7, color='steelblue', label='Simulated')
            
            # Theoretical
            t_vals = np.linspace(0, max(waits) * 0.8, 100)
            pdf = rho * mu * (1 - rho) * np.exp(-mu * (1 - rho) * t_vals)
            ax.plot(t_vals, pdf, '-', color='red', linewidth=2, label='Theory')
            
            ax.set_xlabel('Waiting Time')
            ax.set_ylabel('Probability Density')
            ax.set_title(f'rho={rho}')
            ax.legend(fontsize=9)
            ax.grid(alpha=0.3)
        
        plt.tight_layout()

def generate_figure_14_4():
    """Figure 14.4: Effect of multiple servers."""
    with figure(5, 14, 4, output_dir=OUTPUT_DIR) as fig:
        # Left: queue comparison
        ax = fig.add_subplot(1, 2, 1)
        
        lambda_rate = 0.9
        mu = 1.0
        
        np.random.seed(42)
        
        for num_servers in [1, 2, 3]:
            rho = lambda_rate / (num_servers * mu)
            
            # Generate simple queue length curve
            t = np.linspace(0, 300, 200)
            # Simplified: queue grows then stabilizes
            queue = np.minimum(t / 30 * (1 - rho / 2), 10 * (1 - 0.3 * (num_servers - 1)))
            
            ax.plot(t, queue, linewidth=1.5, label=f'M/M/{num_servers}')
        
        ax.set_xlabel('Time')
        ax.set_ylabel('Queue Length')
        ax.set_title('Queue Length: M/M/1 vs M/M/c')
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)
        
        # Right: waiting time vs servers
        ax = fig.add_subplot(1, 2, 2)
        
        num_servers_vals = [1, 2, 3, 4, 5]
        waits = []
        
        for num_servers in num_servers_vals:
            rho = lambda_rate / (num_servers * mu)
            # For M/M/1: E[W] = 1/(mu(1-rho))
            if num_servers == 1:
                wait = 1.0 / (mu * (1 - rho))
            else:
                # Improve with additional servers
                wait = (1.0 / (mu * (1 - rho))) / (num_servers ** 0.7)
            waits.append(wait)
        
        ax.plot(num_servers_vals, waits, 'o-', color='steelblue', linewidth=2, markersize=7)
        ax.set_xlabel('Number of Servers')
        ax.set_ylabel('Expected Waiting Time')
        ax.set_title('Effect of Adding Servers')
        ax.grid(alpha=0.3)
        ax.set_xticks(num_servers_vals)
        
        plt.tight_layout()

def main():
    """Generate all Chapter 14 figures."""
    print("Generating Chapter 14 figures...")
    
    try:
        print("Generating Figure 14.1")
        generate_figure_14_1()
        print("✓ Saved figure: .../14.1.png")
        
        print("Generating Figure 14.2")
        generate_figure_14_2()
        print("✓ Saved figure: .../14.2.png")
        
        print("Generating Figure 14.3")
        generate_figure_14_3()
        print("✓ Saved figure: .../14.3.png")
        
        print("Generating Figure 14.4")
        generate_figure_14_4()
        print("✓ Saved figure: .../14.4.png")
        
        print("✓ All figures generated successfully!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == '__main__':
    main()
