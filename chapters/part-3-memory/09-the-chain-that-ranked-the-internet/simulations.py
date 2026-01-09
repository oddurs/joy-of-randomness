"""
Chapter 9: The Chain That Ranked the Internet
PageRank and web graph analysis using Markov chains.
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict, deque


# ============================================================================
# Web Graph Representation
# ============================================================================

class WebGraph:
    """Represent a web graph with pages and links."""
    
    def __init__(self, n_pages):
        """Initialize graph with n_pages."""
        self.n_pages = n_pages
        self.links = defaultdict(set)  # links[i] = set of pages i links to
        self.incoming = defaultdict(set)  # incoming[i] = set of pages linking to i
    
    def add_link(self, from_page, to_page):
        """Add a link from from_page to to_page."""
        if from_page == to_page:
            return  # No self-links
        self.links[from_page].add(to_page)
        self.incoming[to_page].add(from_page)
    
    def outgoing_links(self, page):
        """Get list of pages that page links to."""
        return list(self.links[page])
    
    def incoming_links(self, page):
        """Get list of pages linking to page."""
        return list(self.incoming[page])
    
    def transition_matrix(self, handle_dangling=True):
        """
        Build transition matrix for random walk on the web.
        
        Args:
            handle_dangling: If True, dangling nodes link uniformly to all pages
        
        Returns:
            Transition matrix P (n_pages x n_pages)
        """
        P = np.zeros((self.n_pages, self.n_pages))
        
        for i in range(self.n_pages):
            outgoing = self.links[i]
            n_out = len(outgoing)
            
            if n_out == 0:
                # Dangling node
                if handle_dangling:
                    P[i, :] = 1.0 / self.n_pages  # Links to all pages uniformly
            else:
                # Normal: uniform over outgoing links
                for j in outgoing:
                    P[i, j] = 1.0 / n_out
        
        return P
    
    def pagerank_transition_matrix(self, damping=0.85, handle_dangling=True):
        """
        Build PageRank transition matrix with teleportation.
        
        Args:
            damping: Damping factor d (usually 0.85)
            handle_dangling: Handle dangling nodes first
        
        Returns:
            Modified transition matrix P_PR
        """
        P = self.transition_matrix(handle_dangling=handle_dangling)
        
        # Add teleportation
        P_pr = damping * P + (1.0 - damping) / self.n_pages
        
        return P_pr


# ============================================================================
# PageRank Computation
# ============================================================================

def power_method_pagerank(graph, damping=0.85, max_iter=100, tol=1e-6):
    """
    Compute PageRank using the power method.
    
    Args:
        graph: WebGraph object
        damping: Damping factor (default 0.85)
        max_iter: Maximum iterations
        tol: Convergence tolerance
    
    Returns:
        PageRank vector (probabilities)
    """
    P_pr = graph.pagerank_transition_matrix(damping=damping)
    n = graph.n_pages
    
    # Start with uniform distribution
    rank = np.ones(n) / n
    
    for iteration in range(max_iter):
        rank_new = rank @ P_pr  # Left multiply (row vector)
        
        if np.allclose(rank, rank_new, atol=tol):
            break
        
        rank = rank_new
    
    return rank


def random_walk_pagerank(graph, damping=0.85, n_steps=1_000_000, start=None):
    """
    Compute PageRank by simulating a random walk.
    
    Args:
        graph: WebGraph object
        damping: Damping factor
        n_steps: Number of steps in simulation
        start: Starting page (default: random)
    
    Returns:
        Approximate PageRank vector
    """
    P_pr = graph.pagerank_transition_matrix(damping=damping)
    
    if start is None:
        current = np.random.randint(0, graph.n_pages)
    else:
        current = start
    
    visits = np.zeros(graph.n_pages)
    
    for _ in range(n_steps):
        visits[current] += 1
        current = np.random.choice(graph.n_pages, p=P_pr[current])
    
    return visits / visits.sum()


def compare_pagerank_methods(graph, damping=0.85):
    """Compare power method and random walk PageRank."""
    rank_power = power_method_pagerank(graph, damping=damping)
    rank_walk = random_walk_pagerank(graph, damping=damping, n_steps=1_000_000)
    
    return rank_power, rank_walk


# ============================================================================
# Predefined Graph Builders
# ============================================================================

def create_example_graph_5_pages():
    """Create the 5-page example from the chapter."""
    graph = WebGraph(5)
    graph.add_link(0, 1)  # A → B
    graph.add_link(0, 2)  # A → C
    graph.add_link(1, 0)  # B → A
    graph.add_link(1, 3)  # B → D
    graph.add_link(2, 0)  # C → A
    graph.add_link(2, 3)  # C → D
    graph.add_link(3, 4)  # D → E
    graph.add_link(4, 0)  # E → A
    graph.add_link(4, 2)  # E → C
    
    return graph


def create_ring_graph(n):
    """Create a ring: 0→1→2→...→n-1→0."""
    graph = WebGraph(n)
    for i in range(n):
        graph.add_link(i, (i + 1) % n)
    return graph


def create_star_graph(n):
    """Create a star: all nodes link to center (node 0), center links to all."""
    graph = WebGraph(n)
    for i in range(1, n):
        graph.add_link(i, 0)  # Links to center
        graph.add_link(0, i)  # Center links out
    return graph


def create_chain_graph(n):
    """Create a chain: 0→1→2→...→n-1."""
    graph = WebGraph(n)
    for i in range(n - 1):
        graph.add_link(i, i + 1)
    return graph


def create_link_farm(n_pages, target_page, farm_size):
    """
    Create a link farm attack.
    
    Args:
        n_pages: Total pages in graph
        target_page: Page to boost
        farm_size: Number of fake pages in the farm
    
    Returns:
        WebGraph with farm linking to target
    """
    graph = WebGraph(n_pages + farm_size)
    
    # Create base web (ring)
    for i in range(n_pages):
        graph.add_link(i, (i + 1) % n_pages)
    
    # Create farm: all farm pages link to target
    for i in range(farm_size):
        farm_page = n_pages + i
        graph.add_link(farm_page, target_page)
        # Farm pages can link to each other
        if i > 0:
            graph.add_link(farm_page, n_pages + i - 1)
    
    return graph


# ============================================================================
# Analysis Functions
# ============================================================================

def damping_sensitivity(graph, damping_values=[0.5, 0.85, 0.99]):
    """
    Analyze how damping factor affects PageRank.
    
    Returns:
        dict: {damping: pagerank_vector}
    """
    results = {}
    for d in damping_values:
        rank = power_method_pagerank(graph, damping=d)
        results[d] = rank
    return results


def in_degree_ranking(graph):
    """Compute ranking by in-degree (number of incoming links)."""
    in_degree = np.zeros(graph.n_pages)
    for page in range(graph.n_pages):
        in_degree[page] = len(graph.incoming_links(page))
    
    # Normalize
    return in_degree / in_degree.sum()


def detect_dangling_nodes(graph):
    """Find pages with no outgoing links."""
    dangling = []
    for i in range(graph.n_pages):
        if len(graph.links[i]) == 0:
            dangling.append(i)
    return dangling


# ============================================================================
# Visualization Functions
# ============================================================================

def plot_pagerank_comparison(pagerank, labels=None, title="PageRank"):
    """Plot PageRank scores."""
    if labels is None:
        labels = [f"Page {i}" for i in range(len(pagerank))]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    indices = np.argsort(pagerank)[::-1]  # Sort descending
    sorted_rank = pagerank[indices]
    sorted_labels = [labels[i] for i in indices]
    
    ax.bar(range(len(sorted_rank)), sorted_rank, alpha=0.7)
    ax.set_xticks(range(len(sorted_rank)))
    ax.set_xticklabels(sorted_labels, rotation=45)
    ax.set_ylabel('PageRank')
    ax.set_title(title)
    ax.grid(True, alpha=0.3, axis='y')
    
    return fig


def plot_damping_effects(results):
    """Plot how damping factor affects rankings."""
    damping_values = sorted(results.keys())
    n_pages = len(results[damping_values[0]])
    
    fig, axes = plt.subplots(1, len(damping_values), figsize=(15, 4), sharey=True)
    
    for ax, d in zip(axes, damping_values):
        rank = results[d]
        ax.bar(range(n_pages), rank, alpha=0.7)
        ax.set_title(f'd = {d}')
        ax.set_xlabel('Page')
        if ax == axes[0]:
            ax.set_ylabel('PageRank')
        ax.grid(True, alpha=0.3, axis='y')
    
    fig.suptitle('Effect of Damping Factor on PageRank', fontsize=14)
    return fig


def plot_convergence(graph, damping=0.85, max_iter=50):
    """Plot convergence of power method."""
    P_pr = graph.pagerank_transition_matrix(damping=damping)
    n = graph.n_pages
    
    rank = np.ones(n) / n
    history = [rank.copy()]
    
    for _ in range(max_iter):
        rank = rank @ P_pr
        history.append(rank.copy())
    
    history = np.array(history)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for page in range(n):
        ax.plot(history[:, page], label=f'Page {page}', marker='o', markersize=3)
    
    ax.set_xlabel('Iteration')
    ax.set_ylabel('PageRank')
    ax.set_title('Convergence of Power Method')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig


# ============================================================================
# Demo / Main
# ============================================================================

if __name__ == '__main__':
    print("Chapter 9: The Chain That Ranked the Internet")
    print("=" * 60)
    
    # Example graph
    print("\n--- 5-Page Example ---")
    graph = create_example_graph_5_pages()
    
    rank_power = power_method_pagerank(graph, damping=0.85)
    rank_walk = random_walk_pagerank(graph, damping=0.85, n_steps=100_000)
    rank_indeg = in_degree_ranking(graph)
    
    print("Method              | A      | B      | C      | D      | E")
    print("-" * 60)
    print(f"Power Method        | {rank_power[0]:.3f}  | {rank_power[1]:.3f}  | {rank_power[2]:.3f}  | {rank_power[3]:.3f}  | {rank_power[4]:.3f}")
    print(f"Random Walk (100K)  | {rank_walk[0]:.3f}  | {rank_walk[1]:.3f}  | {rank_walk[2]:.3f}  | {rank_walk[3]:.3f}  | {rank_walk[4]:.3f}")
    print(f"In-Degree          | {rank_indeg[0]:.3f}  | {rank_indeg[1]:.3f}  | {rank_indeg[2]:.3f}  | {rank_indeg[3]:.3f}  | {rank_indeg[4]:.3f}")
    
    # Damping sensitivity
    print("\n--- Damping Factor Sensitivity ---")
    results = damping_sensitivity(graph, damping_values=[0.5, 0.85, 0.99])
    
    for d, rank in results.items():
        print(f"d = {d}: {rank}")
    
    # Ring graph
    print("\n--- Ring Graph (10 nodes) ---")
    ring = create_ring_graph(10)
    rank_ring = power_method_pagerank(ring)
    print(f"PageRank (should be uniform): {rank_ring}")
    print(f"Std dev: {np.std(rank_ring):.6f}")
    
    # Star graph
    print("\n--- Star Graph (10 nodes) ---")
    star = create_star_graph(10)
    rank_star = power_method_pagerank(star)
    print(f"Center (page 0): {rank_star[0]:.3f}")
    print(f"Periphery (avg): {np.mean(rank_star[1:]):.3f}")
    
    # Link farm attack
    print("\n--- Link Farm Attack ---")
    print("Ring graph with link farm targeting page 0")
    
    ring_10 = create_ring_graph(10)
    rank_before = power_method_pagerank(ring_10)
    
    farm_graph = create_link_farm(10, target_page=0, farm_size=50)
    rank_after = power_method_pagerank(farm_graph)
    
    print(f"Page 0 rank before: {rank_before[0]:.4f}")
    print(f"Page 0 rank after:  {rank_after[0]:.4f}")
    print(f"Boost factor: {rank_after[0] / rank_before[0]:.2f}x")
    
    print("\nDone!")
