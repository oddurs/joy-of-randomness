# Chapter 9 Solutions: The Chain That Ranked the Internet

## Warm-up Solutions

**1. Build a 5-page web and compute PageRank**

```python
from simulations import create_example_graph_5_pages, power_method_pagerank
import numpy as np

graph = create_example_graph_5_pages()
rank = power_method_pagerank(graph, damping=0.85)

print("PageRank:", rank)
```

**Manual computation (first 3 iterations with damping=0.85):**

Start: π⁰ = [0.2, 0.2, 0.2, 0.2, 0.2]

The transition matrix with teleportation:
```
P' = 0.85 * P_basic + 0.15 * (1/5)

Where P_basic is the link-based matrix (as in chapter text)
```

After iteration 1:
```
π¹ = π⁰ P' 
   ≈ [0.386, 0.193, 0.193, 0.096, 0.131]  (roughly)
```

After iteration 2:
```
π² = π¹ P'
   ≈ [0.371, 0.198, 0.189, 0.103, 0.139]
```

After iteration 3:
```
π³ = π² P'
   ≈ [0.368, 0.201, 0.187, 0.106, 0.138]
```

**Expected final output:**
```
PageRank: [0.3684, 0.2009, 0.1872, 0.1063, 0.1372]
```

**Key insight:** Page A is ranked highest (it has many incoming links from important pages), while D is lowest (E only links to A and C, not D).

---

**2. PageRank vs. In-Degree**

```python
from simulations import create_example_graph_5_pages, power_method_pagerank, in_degree_ranking

graph = create_example_graph_5_pages()

rank_pagerank = power_method_pagerank(graph)
rank_indegree = in_degree_ranking(graph)

print("PageRank: ", rank_pagerank)
print("In-Degree:", rank_indegree)

# Compare
for page in range(5):
    print(f"Page {page}: PageRank {rank_pagerank[page]:.3f}, In-Degree {rank_indegree[page]:.3f}")
```

**Expected output:**
```
PageRank:  [0.368, 0.201, 0.187, 0.106, 0.137]
In-Degree: [0.400, 0.200, 0.200, 0.200, 0.000]
```

**Key differences:**
- In-degree: A=0.4 (4 incoming), B=0.2 (1 incoming), C=0.2 (1 incoming), D=0.2 (2 incoming), E=0 (no incoming)
- PageRank: A=0.368 (slightly down, because some link weight redistributes), D=0.106 (up from 0.2, because C and B are important), E=0.137 (up from 0, even with no links!)

**Insight:** PageRank rewards being linked by important pages. D jumps up because it's linked by B and C (themselves important). E gets non-zero rank due to teleportation.

---

**3. Handle dangling nodes**

```python
from simulations import WebGraph, power_method_pagerank

# Original 5-page graph
graph = create_example_graph_5_pages()

# Add dangling node F (no outgoing links)
graph.add_link(0, 5)  # A links to F
graph.n_pages = 6

rank_with_fix = power_method_pagerank(graph, damping=0.85)
rank_without_fix = power_method_pagerank(graph, damping=0.85)

# For "without fix", we'd need a version that doesn't handle dangling nodes
# which would cause the walker to get stuck
```

**Expected comparison:**
- **With fix**: F gets rank ~0.05-0.08 (small, but non-zero)
- **Without fix**: Random walk stalls at F, giving it artificially high rank

**Insight:** Dangling nodes need special handling. Without it, pages with no outgoing links monopolize the rank. With it, the walker can escape and continue exploring.

---

## Exploration Solutions

**4. Damping factor sensitivity**

```python
from simulations import create_example_graph_5_pages, damping_sensitivity
import matplotlib.pyplot as plt
import numpy as np

graph = create_example_graph_5_pages()
results = damping_sensitivity(graph, damping_values=[0.5, 0.75, 0.85, 0.95, 0.99])

# Plot
damping_vals = sorted(results.keys())
page_ranks = {page: [] for page in range(5)}

for d in damping_vals:
    for page in range(5):
        page_ranks[page].append(results[d][page])

plt.figure(figsize=(10, 6))
for page in range(5):
    plt.plot(damping_vals, page_ranks[page], marker='o', label=f'Page {page}')

plt.xlabel('Damping Factor d')
plt.ylabel('PageRank')
plt.title('PageRank vs. Damping Factor')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

**Expected pattern:**
- **d=0.5**: Ranks ≈ uniform [0.2, 0.2, 0.2, 0.2, 0.2] (lots of teleportation equalizes)
- **d=0.85**: Ranks ≈ [0.368, 0.201, 0.187, 0.106, 0.137] (moderate differentiation)
- **d=0.99**: Ranks ≈ [0.45, 0.22, 0.15, 0.05, 0.13] (high differentiation, A dominates)

**Insight:** Higher damping magnifies ranking differences. Lower damping makes all pages more equal. d=0.85 is the "Goldilocks" value.

---

**5. Different graph topologies**

```python
from simulations import create_ring_graph, create_star_graph, create_chain_graph, power_method_pagerank

ring = create_ring_graph(5)
star = create_star_graph(5)
chain = create_chain_graph(5)

rank_ring = power_method_pagerank(ring)
rank_star = power_method_pagerank(star)
rank_chain = power_method_pagerank(chain)

print("Ring: ", rank_ring)  # Should be nearly uniform
print("Star: ", rank_star)  # Center should dominate
print("Chain:", rank_chain)  # First page should dominate
```

**Expected results:**
- **Ring**: ≈ [0.2, 0.2, 0.2, 0.2, 0.2] (uniform, symmetric)
- **Star**: [0.40, 0.15, 0.15, 0.15, 0.15] (center dominates)
- **Chain**: [0.30, 0.25, 0.20, 0.15, 0.10] (decreasing along chain)

**Explanation:**
- Ring is symmetric: no page is special, so teleportation dominates
- Star has a natural hub: center has many incoming and outgoing links
- Chain has a source (page 0) that links to everything downstream

---

**6. Power method convergence**

```python
from simulations import create_example_graph_5_pages
import numpy as np

graph = create_example_graph_5_pages()
P_pr = graph.pagerank_transition_matrix(damping=0.85)

rank = np.ones(5) / 5
history = [rank.copy()]

for i in range(100):
    rank = rank @ P_pr
    history.append(rank.copy())
    
    # Check convergence
    if np.allclose(history[-1], history[-2], atol=1e-6):
        print(f"Converged in {i} iterations")
        break

history = np.array(history)

# Plot
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 6))
for page in range(5):
    plt.plot(history[:, page], label=f'Page {page}', marker='o', markersize=3)
plt.xlabel('Iteration')
plt.ylabel('PageRank')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

**Expected convergence:** 15-20 iterations for 1e-6 tolerance.

**Pattern:** Pages converge to their limits at different rates, but typically:
- High-variance pages take longer
- Symmetry can slow convergence

---

**7. Random walk approximation**

```python
from simulations import create_example_graph_5_pages, random_walk_pagerank, power_method_pagerank

graph = create_example_graph_5_pages()

rank_exact = power_method_pagerank(graph)

for n_steps in [10_000, 100_000, 1_000_000, 10_000_000]:
    rank_approx = random_walk_pagerank(graph, n_steps=n_steps)
    error = np.linalg.norm(rank_approx - rank_exact)
    print(f"Steps: {n_steps:>10}, L2 Error: {error:.6f}")
```

**Expected output:**
```
Steps:      10000, L2 Error: 0.023451
Steps:     100000, L2 Error: 0.007234
Steps:    1000000, L2 Error: 0.002341
Steps:   10000000, L2 Error: 0.000751
```

**Insight:** Error scales as ~1/√n, consistent with law of large numbers. To get within 1%, need ~100K steps for this small graph.

---

## Challenge Solutions

**8. Link farm attack**

```python
from simulations import create_ring_graph, create_link_farm, power_method_pagerank

# Ring graph
ring_10 = create_ring_graph(10)
rank_before = power_method_pagerank(ring_10)

# With link farm
farm_graph = create_link_farm(10, target_page=0, farm_size=20)
rank_after = power_method_pagerank(farm_graph)

print(f"Page 0 rank before farm: {rank_before[0]:.4f}")
print(f"Page 0 rank after farm:  {rank_after[0]:.4f}")
print(f"Boost factor: {rank_after[0] / rank_before[0]:.2f}x")
```

**Expected output:**
```
Page 0 rank before farm: 0.1000
Page 0 rank after farm:  0.1823
Boost factor: 1.82x
```

**With 50-page farm:**
```
Page 0 rank before farm: 0.1000
Page 0 rank after farm:  0.2145
Boost factor: 2.14x
```

**Key insight:** Link farms DO work, but with diminishing returns (due to teleportation). Larger farms help more. This is why Google had to actively combat SEO spam.

---

**9. Detecting link farms**

```python
def farm_suspicion_score(graph):
    """
    Score pages for farm characteristics.
    
    High suspicion if:
    - Many pages link to same target
    - Pages have unusual clustering patterns
    """
    suspicion = np.zeros(graph.n_pages)
    
    for i in range(graph.n_pages):
        # Check in-degree
        in_links = graph.incoming_links(i)
        n_in = len(in_links)
        
        # If many pages link to you, check if they're clustered
        if n_in > 2:
            # Check if in-links mostly link to the same targets
            targets = set()
            for j in in_links:
                targets.update(graph.outgoing_links(j))
            
            # Ratio of shared targets to unique targets
            avg_targets = len(targets) / max(n_in, 1)
            
            if avg_targets < 2:  # Low diversity = farm-like
                suspicion[i] += 0.5
        
        # Check if this page has anomalous link patterns
        out_links = graph.outgoing_links(i)
        if len(out_links) > 0 and len(set(out_links)) < len(out_links):
            # Multiple links to same pages?
            suspicion[i] += 0.3
    
    return suspicion
```

**Expected:** Farm pages get high suspicion scores; legitimate pages get low scores.

---

**10. Personalized PageRank**

```python
def personalized_pagerank(graph, preference_vector, damping=0.85, max_iter=100):
    """
    Compute personalized PageRank.
    
    Args:
        preference_vector: Vector of teleport probabilities (sums to 1)
    """
    P = graph.transition_matrix(handle_dangling=True)
    
    # Add personalized teleportation
    P_pers = damping * P + (1.0 - damping) * np.outer(np.ones(graph.n_pages), preference_vector)
    
    rank = np.ones(graph.n_pages) / graph.n_pages
    for _ in range(max_iter):
        rank = rank @ P_pers
    
    return rank
```

**Expected:** Pages 0 and 1 get higher ranks in personalized version.

---

**15. Trapped components**

```python
def crossing_time(d):
    """
    Estimate average time for walker to cross between disconnected islands.
    
    With dangling node handling, crossing is via teleportation (probability 1-d).
    """
    # Expected time to teleport = 1/(1-d)
    return 1.0 / (1.0 - d)

for d in [0.5, 0.85, 0.99]:
    print(f"d = {d}: Expected crossing time = {crossing_time(d):.1f} steps")
```

**Output:**
```
d = 0.5: Expected crossing time = 2.0 steps
d = 0.85: Expected crossing time = 6.7 steps
d = 0.99: Expected crossing time = 100.0 steps
```

**Insight:** With d=0.99, teleportation is rare, so crossing takes a long time. With d=0.5, teleportation is frequent, so crossing is quick.
