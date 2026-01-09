# Chapter 7 Solutions: What Comes Next?

## Warm-up Solutions

**1. Build a first-order Markov text generator**

```python
from simulations import load_text, build_transition_matrix, generate_text
import numpy as np

# Load text
with open('shakespeare.txt', 'r') as f:
    text = f.read()

words = load_text(text)
print(f"Loaded {len(words)} words")

# Build first-order model
transitions = build_transition_matrix(words, order=1)

# Generate text
random_start = np.random.choice(list(transitions.keys()))
generated = generate_text(transitions, random_start, length=100, order=1)
print("Generated text:")
print(generated)
```

**Expected output:** Something like "the king did see the lord of the land, and the queen did speak to the king, and he did say..." It reads somewhat like English but lacks narrative coherence.

**Key observation:** The output captures word associations (what words naturally follow each other) but has no memory of context beyond the immediately previous word.

---

**2. Visualize the transition structure**

```python
state = 'the'
if state in transitions:
    next_words = transitions[state]
    total = sum(next_words.values())
    print(f"Words most likely to follow '{state}':")
    for word, count in next_words.most_common(10):
        prob = count / total
        print(f"  {word:15s}: {prob:.3f}")
```

**Expected output (from Shakespeare):**
```
Words most likely to follow 'the':
  king             : 0.125
  lord             : 0.089
  queen            : 0.067
  hand             : 0.045
  world            : 0.034
  great            : 0.030
  ...
```

**Interpretation:** "the" most commonly precedes nouns in Shakespeare. This makes sense; articles in English usually precede nouns.

---

**3. Compare corpus entropy**

```python
from simulations import compute_entropy

# Load two different texts
with open('shakespeare.txt', 'r') as f:
    shak_text = f.read()
with open('news.txt', 'r') as f:
    news_text = f.read()

shak_words = load_text(shak_text)
news_words = load_text(news_text)

# Build models
shak_trans = build_transition_matrix(shak_words, order=1)
news_trans = build_transition_matrix(news_words, order=1)

# Compute entropies
shak_entropy = compute_entropy(shak_trans)
news_entropy = compute_entropy(news_trans)

print(f"Shakespeare entropy: {shak_entropy:.3f} bits/transition")
print(f"News entropy: {news_entropy:.3f} bits/transition")
```

**Expected output:**
```
Shakespeare entropy: 4.523 bits/transition
News entropy: 3.287 bits/transition
```

**Explanation:** Shakespeare has higher entropy because it uses richer vocabulary and more varied sentence structures. News articles are more formulaic and repetitive, making them more predictable.

---

## Exploration Solutions

**4. Order comparison: Generate samples**

```python
for order in [1, 2, 3]:
    trans = build_transition_matrix(words, order=order)
    
    # Construct appropriate starting state
    if order == 1:
        start = 'to'
    elif order == 2:
        start = ('to', 'be')
    else:
        start = ('to', 'be', 'or')
    
    generated = generate_text(trans, start, length=50, order=order)
    print(f"\n--- Order {order} ---")
    print(generated)
```

**Expected outputs:**

Order 1:
> to the lord and the king of the world did see the hand of the queen...

Order 2:
> to be or not to be a king, and the lord did say unto the king...

Order 3:
> to be or not to be the question whether tis nobler in the mind to suffer...

**Observation:** Higher order chains produce progressively more coherent output, but by order 3 or 4, they start reproducing the original text.

---

**5. The memorization threshold**

```python
for order in range(1, 6):
    trans = build_transition_matrix(words, order=order)
    generated = generate_text(trans, start_state, length=100, order=order)
    
    # Check how much matches the original
    original_text = ' '.join(words[:100])
    match_fraction = len([w for w in generated.split() if w in original_text.split()]) / 100
    
    print(f"Order {order}: {match_fraction:.1%} overlap with original")
```

**Expected pattern:**
- Order 1: ~30% overlap
- Order 2: ~50% overlap
- Order 3: ~70% overlap
- Order 4: ~85% overlap
- Order 5: ~95% overlap (essentially reproducing original)

**Insight:** As order increases exponentially, the model shifts from generation to memorization.

---

**6. Entropy curve**

```python
from simulations import compare_orders
import matplotlib.pyplot as plt

results = compare_orders(words, orders=[1, 2, 3, 4, 5])

orders = sorted(results.keys())
entropies = [results[o]['entropy'] for o in orders]

plt.figure(figsize=(10, 6))
plt.plot(orders, entropies, 'o-', linewidth=2, markersize=8)
plt.xlabel('Chain Order')
plt.ylabel('Entropy (bits)')
plt.title('Entropy vs. Markov Chain Order')
plt.grid(True, alpha=0.3)
plt.show()

for order in orders:
    print(f"Order {order}: {results[order]['entropy']:.3f} bits")
```

**Expected output:**
```
Order 1: 4.523 bits
Order 2: 3.876 bits
Order 3: 2.654 bits
Order 4: 1.245 bits
Order 5: 0.123 bits
```

**Pattern:** Entropy decreases with order because higher-order chains have fewer ambiguous states—more context means more deterministic transitions.

---

**7. Perplexity on held-out data**

```python
results = compare_orders(words, orders=[1, 2, 3], test_fraction=0.2)

for order in [1, 2, 3]:
    perp = results[order]['perplexity']
    print(f"Order {order}: Perplexity = {perp:.2f}")
```

**Expected output:**
```
Order 1: Perplexity = 87.34
Order 2: Perplexity = 34.56
Order 3: Perplexity = 28.91
```

**Interpretation:** Order 3 has the lowest perplexity on test data, suggesting it generalizes best. Order 4+ might overfit (train perplexity improves, but test perplexity gets worse).

---

## Challenge Solutions

**8. Character-level model**

```python
def load_text_chars(filename):
    """Load text as character sequence."""
    with open(filename, 'r') as f:
        return list(f.read().lower())

chars = load_text_chars('shakespeare.txt')

# Character-level, order 1
char_trans = build_transition_matrix(chars, order=1)
generated_chars = generate_text(char_trans, 'e', length=100, order=1)
print("Generated character sequence:")
print(generated_chars)
```

**Expected output:**
> ethethee ndath ath the ath and ththe nd aththe at hath and he thee the...

**Key difference:** Character-level models produce plausible letter sequences (e.g., 'th', 'and', 'the') but often fail to form complete words. This is because character-level transitions are more constrained (fewer total characters than words).

---

**9. Entropy estimation with different test sets**

```python
# Build model on Shakespeare
shak_words = load_text(open('shakespeare.txt').read())
shak_trans = build_transition_matrix(shak_words, order=2)
shak_entropy = compute_entropy(shak_trans)

# Test on news
news_words = load_text(open('news.txt').read())
news_perp = perplexity(shak_trans, news_words, order=2)

print(f"Shakespeare model entropy: {shak_entropy:.3f}")
print(f"Perplexity on news: {news_perp:.2f}")
print(f"Perplexity on Shakespeare test: {results[2]['perplexity']:.2f}")
```

**Expected output:**
```
Shakespeare model entropy: 3.876
Perplexity on news: 234.56 (much higher!)
Perplexity on Shakespeare test: 34.56
```

**Explanation:** The news articles use different vocabulary and phrases. The Shakespeare model is "surprised" by this new domain and assigns low probability, leading to high perplexity.

---

**10. Estimate vocabulary growth rate**

```python
from simulations import vocabulary_size_growth
import numpy as np
import matplotlib.pyplot as plt

growth = vocabulary_size_growth(words, max_order=5)

orders = list(growth.keys())
sizes = list(growth.values())

# Fit on log-log scale
log_orders = np.log(orders)
log_sizes = np.log(sizes)
alpha = np.polyfit(log_orders, log_sizes, 1)[0]

plt.loglog(orders, sizes, 'o-', linewidth=2)
plt.xlabel('Order')
plt.ylabel('Number of States')
plt.title(f'Vocabulary Growth (exponent α ≈ {alpha:.2f})')
plt.grid(True, alpha=0.3, which='both')
plt.show()

print(f"Vocabulary growth rate: States ~ Order^{alpha:.2f}")
```

**Expected output:**
```
Order 1:   500 states
Order 2:  8,234 states
Order 3: 67,891 states
Order 4: 234,567 states
Order 5: 567,890 states

Vocabulary growth rate: States ~ Order^3.12
```

**Interpretation:** For a corpus of ~100K words, the state space grows roughly cubically with order (α ≈ 3). This is why higher-order models are data-hungry.

---

**11. The Shannon redundancy of English**

```python
chars = load_text_chars('english_text.txt')
char_trans = build_transition_matrix(chars, order=1)
char_entropy = compute_entropy(char_trans)

print(f"Character-level entropy: {char_entropy:.3f} bits/char")
print(f"Shannon's estimate: ~1.0-1.5 bits/char")
```

**Expected output:**
```
Character-level entropy: 1.23 bits/char
Shannon's estimate: ~1.0-1.5 bits/char
```

**Match!** Your estimate should be close to Shannon's famous result from 1948. This shows that English has about 1-1.5 bits of "surprise" per character—the rest is highly predictable structure.

---

## Thought Experiments

**12. Long-range dependence**

Example sentence:
> "The elephant, which walked across the savanna with its trunk raised high in the air and its ears flapping majestically, was..."

The verb must agree with "elephant" (singular: "was"), not the nearest noun. A first-order Markov chain would look at the word immediately before "was" (probably something like "air"), which gives no guidance on number.

**Why Markov chains fail:**
- They have no concept of grammatical structure
- They can't track "open parentheses" or "subject noun" across many words
- They operate purely on surface-level statistical patterns

Modern neural networks solve this with:
- Attention mechanisms that can look back arbitrarily far
- Learned representations of grammatical roles
- Implicit hierarchical structure

---

**13. The illusion of understanding**

Generated: "The king and the queen were married to the lord, and they lived in a great castle with many knights and ladies, and every day the sun rose and the moon set..."

This reads somewhat plausibly locally but has no plot, character development, or intentional structure.

**Tasks requiring global structure:**
- Narrative arc (setup, conflict, resolution)
- Character consistency (same character behaves consistently)
- Logical reasoning (premises → conclusions)
- Compositional semantics (meaning depends on structure, not just words)

Markov chains generate plausible *style* but not plausible *content*.

---

**14. From Markov chains to neural networks**

**Advantages of neural/distributed approaches:**
- Learned representations compress long-range patterns
- Attention mechanisms select relevant history
- Implicit memory in activation patterns
- Much more parameter-efficient than explicit state spaces

**What might be lost:**
- Interpretability (explicit transitions were readable)
- Exact probability computation (networks give implicit distributions)
- Theoretical guarantees (Markov chains have nice convergence proofs)

But in practice, the gains vastly outweigh the losses.

---

**15. Compression and entropy**

```python
import gzip

# Compute entropy estimate
text = open('corpus.txt').read()
chars = load_text_chars('corpus.txt')
entropy_estimate = compute_entropy(build_transition_matrix(chars, order=1))
theoretical_min_bytes = len(text) * entropy_estimate / 8

# Actual compression
original_size = len(text)
compressed_size = len(gzip.compress(text.encode()))

print(f"Original: {original_size} bytes")
print(f"Theoretical minimum (from entropy): {theoretical_min_bytes:.0f} bytes")
print(f"gzip achieves: {compressed_size} bytes")
print(f"Efficiency: {compressed_size / theoretical_min_bytes:.1%}")
```

**Expected output:**
```
Original: 100,000 bytes
Theoretical minimum: 12,500 bytes (at 1 bit/char)
gzip achieves: 28,000 bytes
Efficiency: 224%
```

**Interpretation:** gzip uses more bytes than the theoretical minimum because:
1. It uses a practical algorithm (LZ77), not an optimal one
2. We're only using order-1 entropy; real English has more structure at higher orders
3. Overhead for dictionary and metadata

But gzip is still much better than storing the original 100,000 bytes!
