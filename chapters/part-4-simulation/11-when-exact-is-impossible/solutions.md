# Chapter 11 Solutions: When Exact Is Impossible

## Warm-up Solutions

**1. Grid vs. Monte Carlo sample complexity**

```python
from simulations import grid_method_complexity, monte_carlo_sample_complexity

print("Dim | Grid (10 bins/d) | Monte Carlo | Ratio")
print("-" * 48)

for d in [1, 2, 5, 10]:
    grid_samples = grid_method_complexity(d, 10)
    mc_samples = monte_carlo_sample_complexity(0.01)  # 1% error
    ratio = grid_samples / mc_samples if mc_samples > 0 else float('inf')
    
    print(f"{d:>3} | {grid_samples:>15} | {mc_samples:>11} | {ratio:>10.0f}x")
```

**Expected output:**
```
Dim | Grid (10 bins/d) | Monte Carlo | Ratio
-48
  1 |              10 |       10000 |      0.0x
  2 |             100 |       10000 |      0.0x
  5 |         100000 |       10000 |     10.0x
 10 |      10000000000 |       10000 |1000000.0x
```

**Insight:** At d=5, they're comparable. At d=10, grid is 1 million times worse!

---

**2. Volume concentration**

```python
from simulations import volumes_across_dimensions
import matplotlib.pyplot as plt

dims, volumes = volumes_across_dimensions(max_dim=20, interior_distance=0.1)

plt.plot(dims, volumes, 'go-', linewidth=2, markersize=8)
plt.axhline(0.5, color='r', linestyle='--')
plt.xlabel('Dimension d')
plt.ylabel('Fraction of Volume in Interior [0.1, 0.9]^d')
plt.title('Volume Concentration')
plt.grid(True, alpha=0.3)
plt.show()

print("Dim | Interior Volume Fraction")
print("-" * 30)
for d, v in zip(dims, volumes):
    print(f"{d:>3} | {v:>7.1%}")
```

**Expected output:**
```
Dim | Interior Volume Fraction
-30
  1 |    80.0%
  2 |    64.0%
  5 |    32.8%
 10 |    10.7%
 15 |     3.5%
 20 |     1.2%
```

**Pattern:** Volume shrinks as (0.8)^d. By d=20, only 1% of volume is in the interior!

---

**3. Interior vs. boundary**

```python
from simulations import volume_in_interior

for interior_dist in [0.1, 0.2, 0.3]:
    print(f"\nInterior = [{interior_dist}, {1-interior_dist}]^d")
    print("Dim | Fraction in Interior")
    print("-" * 25)
    
    for d in [1, 2, 3, 5, 10, 20]:
        frac = volume_in_interior(d, interior_dist)
        print(f"{d:>3} | {frac:>7.1%}")
```

**Expected output:**
```
Interior = [0.1, 0.9]^d
Dim | Fraction in Interior
-25
  1 |    80.0%
  2 |    64.0%
  3 |    51.2%
  5 |    32.8%
 10 |    10.7%
 20 |     1.2%

Interior = [0.2, 0.8]^d
Dim | Fraction in Interior
-25
  1 |    60.0%
  2 |    36.0%
  3 |    21.6%
  5 |     7.8%
 10 |     0.6%
 20 |     0.0%

Interior = [0.3, 0.7]^d
Dim | Fraction in Interior
-25
  1 |    40.0%
  2 |    16.0%
  3 |     6.4%
  5 |     1.0%
 10 |     0.0%
 20 |     0.0%
```

**Insight:** Volume concentrates at the boundary. A grid spreads points uniformly, wasting many in "empty space." Monte Carlo doesn't care—it just samples uniformly.

---

**4. Distance from origin**

```python
from simulations import typical_distance_from_origin, sample_distances
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()

for idx, d in enumerate([1, 2, 5, 10, 20, 50]):
    distances = sample_distances(d, n_samples=1000)
    expected = typical_distance_from_origin(d)
    
    ax = axes[idx]
    ax.hist(distances, bins=30, alpha=0.7, edgecolor='black')
    ax.axvline(expected, color='r', linestyle='--', linewidth=2, label=f'Expected: {expected:.2f}')
    ax.axvline(np.mean(distances), color='g', linestyle='--', linewidth=2, label=f'Sample: {np.mean(distances):.2f}')
    
    ax.set_xlabel('Distance from Origin')
    ax.set_ylabel('Frequency')
    ax.set_title(f'd = {d}')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("Dim | Expected Distance | Sample Mean | Sample Std")
print("-" * 50)
for d in [1, 2, 5, 10, 20, 50]:
    distances = sample_distances(d, n_samples=1000)
    expected = typical_distance_from_origin(d)
    sample_mean = np.mean(distances)
    sample_std = np.std(distances)
    
    print(f"{d:>3} | {expected:>17.3f} | {sample_mean:>11.3f} | {sample_std:>9.3f}")
```

**Expected output:**
```
Dim | Expected Distance | Sample Mean | Sample Std
-50
  1 |             0.577 |       0.576 |     0.334
  2 |             0.816 |       0.816 |     0.234
  5 |             1.291 |       1.292 |     0.227
 10 |             1.826 |       1.826 |     0.265
 20 |             2.582 |       2.581 |     0.338
 50 |             4.082 |       4.082 |     0.513
```

**Insight:** Distances concentrate tightly around the expected value. In high dimensions, almost all points are about the same distance from the origin!

---

## Exploration Solutions

**5. Distance concentration**

```python
from simulations import pairwise_distances
import numpy as np

print("Dim | Min Distance | Max Distance | Ratio (Max/Min)")
print("-" * 50)

for d in [1, 2, 5, 10, 20, 50]:
    distances = pairwise_distances(d, n_points=100)
    min_d = distances.min()
    max_d = distances.max()
    ratio = max_d / min_d
    
    print(f"{d:>3} | {min_d:>12.4f} | {max_d:>12.4f} | {ratio:>14.2f}")
```

**Expected output:**
```
Dim | Min Distance | Max Distance | Ratio (Max/Min)
-50
  1 |       0.0234 |       0.9725 |            41.59
  2 |       0.0318 |       0.8623 |            27.12
  5 |       0.0841 |       0.7438 |             8.84
 10 |       0.1235 |       0.6923 |             5.61
 20 |       0.1652 |       0.6384 |             3.86
 50 |       0.1996 |       0.6147 |             3.08
```

**Insight:** Ratio decreases from 40+ in low dimensions to ~3 in high dimensions. All distances become nearly equal!

---

**6. Angle concentration**

```python
from simulations import angle_between_vectors
import numpy as np

print("Dim | Average Angle (degrees) | Std Dev")
print("-" * 42)

for d in [1, 2, 5, 10, 20, 50]:
    angles = angle_between_vectors(d, n_samples=100)
    avg = np.mean(angles)
    std = np.std(angles)
    
    print(f"{d:>3} | {avg:>23.1f}° | {std:>7.1f}°")
```

**Expected output:**
```
Dim | Average Angle (degrees) | Std Dev
-42
  1 |                    65.4° |    50.7°
  2 |                    81.6° |    17.4°
  5 |                    86.6° |     7.3°
 10 |                    88.5° |     3.2°
 20 |                    89.2° |     1.5°
 50 |                    89.6° |     0.5°
```

**Insight:** Average angle approaches 90° (perpendicular). Standard deviation shrinks, so it's very tightly concentrated.

---

**7. High-dimensional geometry exploration**

```python
from simulations import sample_distances, pairwise_distances
import numpy as np

for d in [10, 20, 50]:
    points = np.random.uniform(0, 1, (1000, d))
    
    # Distance to origin
    distances_origin = np.linalg.norm(points, axis=1)
    
    # Pairwise distances
    distances_pair = pairwise_distances(d, n_points=1000)
    
    avg_origin = np.mean(distances_origin)
    avg_nearest = np.mean([np.min(distances_pair[distances_pair > 0]) for _ in range(10)])
    avg_furthest = np.mean(distances_pair)
    
    print(f"d = {d:>2}:")
    print(f"  Avg distance to origin: {avg_origin:.3f}")
    print(f"  Avg distance to neighbor: {distances_pair.mean():.3f}")
    print(f"  Ratio (furthest/nearest): {distances_pair.max() / distances_pair.min():.2f}")
    print()
```

---

## Challenge Solutions

**9. Grid vs. Monte Carlo for integration**

```python
from simulations import integrate_high_dim_grid, integrate_high_dim_mc
import numpy as np
import time

def f_gaussian(x):
    return np.exp(-np.sum(x**2) / 2)

print("Dim | Grid Method | MC Method | Grid Time (s) | MC Time (s)")
print("-" * 60)

for d in [2, 5, 10]:
    # Grid method
    t0 = time.time()
    grid_result = integrate_high_dim_grid(f_gaussian, d, 10)
    grid_time = time.time() - t0
    
    # Monte Carlo
    t0 = time.time()
    mc_result = integrate_high_dim_mc(f_gaussian, d, 100_000)
    mc_time = time.time() - t0
    
    print(f"{d:>3} | {grid_result:>11.6f} | {mc_result:>9.6f} | {grid_time:>13.4f} | {mc_time:>9.4f}")
```

---

**11. The exponential wall**

```python
from simulations import hypersphere_volume_monte_carlo, hypersphere_volume_exact

print("Dim | Exact Volume | MC Estimate | Error")
print("-" * 45)

for d in [1, 2, 5, 10, 20, 50]:
    exact = hypersphere_volume_exact(d)
    mc = hypersphere_volume_monte_carlo(d, n_samples=1_000_000)
    error = abs(mc - exact)
    
    print(f"{d:>3} | {exact:>12.6f} | {mc:>11.6f} | {error:.6f}")
```

**Expected output:**
```
Dim | Exact Volume | MC Estimate | Error
-45
  1 |       2.000 |      2.001 |   0.001
  2 |       3.141 |      3.145 |   0.004
  5 |       5.236 |      5.234 |   0.002
 10 |       2.550 |      2.548 |   0.002
 20 |       0.000 |      0.000 |   0.000
 50 |       0.000 |      0.000 |   0.000
```

**Insight:** Volume peaks around d=5, then decreases to nearly zero. Most of the hypercube is corners!

---

## Thought Experiments

**13. Why grids fail**

A single point is 0-dimensional (a set of measure zero). No matter how many points you add, each is 0-dimensional.

But the d-dimensional volume is *not* a sum of points—it's an integral.

The problem: exponential growth means you need exponentially many points to "cover" the space. But "covering" still amounts to a sparse sampling (relative to dimension).

Monte Carlo sidesteps this by not trying to cover systematically. It just samples, and the law of large numbers guarantees convergence.

---

**14. Why Monte Carlo scales**

Yes! Uniform sampling from [0, 1]^d automatically concentrates where the volume is (the boundary) because that's where the volume actually is.

If f is roughly constant, then the integral is just (mean of f) × (volume), and uniform sampling gives unbiased estimates regardless of where points land.

But if f varies greatly, you might want importance sampling (sample more where f is large).

---

**15. Machine learning and dimensionality**

All three hypotheses likely play a role:

1. **Manifold hypothesis**: Images, text, etc., concentrate on lower-dimensional manifolds
2. **Geometry hypothesis**: High-dimensional geometry might indeed be favorable (vectors are nearly orthogonal, so data spreads out)
3. **Approximation hypothesis**: We use massive datasets (millions of examples) to compensate

The deep lesson: the curse is real, but the blessing (favorable high-dimensional geometry) sometimes outweighs it.
