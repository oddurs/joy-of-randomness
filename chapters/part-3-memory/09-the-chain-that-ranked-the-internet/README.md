# Chapter 9: The Chain That Ranked the Internet

## Metadata

```yaml
Part: 3 - Memory
Topics: PageRank, Google algorithm, random walks on graphs, information retrieval
Key Concepts: Stationary distributions, eigenvectors, web graph structure
```

---

## How a Random Walk Solved the Information Retrieval Problem

In 1998, two Stanford PhD students had a strange idea: to find the best page on the internet, imagine a person clicking links at random, forever. The pages they visit most often are the most important. This elegant insight—rooted in Markov chain theory—became Google and changed how humanity accesses information.

---

## First Contact: A Tiny Web

Let's build a toy internet: 5 pages with links between them.

```
Page A → B, C
Page B → A, D
Page C → A, D
Page D → E
Page E → A, C
```

We represent this as a **directed graph** where edges are links. Now imagine a random surfer:
1. Start at a random page
2. Click a random outgoing link
3. Repeat forever

Which pages get visited most?

Intuition says "pages with many incoming links." But that's not quite right. A link from an important page matters more than a link from an unimportant page. This creates a circular definition: *importance depends on the importance of pages that link to you*.

Let's build a transition matrix. From page A (which has 2 outgoing links):
- Probability to B: 1/2
- Probability to C: 1/2

From page B (2 outgoing links):
- Probability to A: 1/2
- Probability to D: 1/2

The full transition matrix P:

```
     A    B    C    D    E
A  [ 0   1/2  1/2   0    0  ]
B  [1/2   0    0   1/2   0  ]
C  [1/2   0    0   1/2   0  ]
D  [ 0    0    0    0    1  ]
E  [1/3  1/3  1/3   0    0  ]
```

Now simulate a random walk: start at page A, take 1 million steps, and count visits.

```python
import numpy as np

P = np.array([
    [0,   1/2, 1/2,  0,   0],
    [1/2, 0,   0,   1/2, 0],
    [1/2, 0,   0,   1/2, 0],
    [0,   0,   0,    0,   1],
    [1/3, 1/3, 1/3,  0,   0]
])

# Simulate
current = 0  # Start at A
visits = np.zeros(5)

for _ in range(1_000_000):
    visits[current] += 1
    current = np.random.choice(5, p=P[current])

# Normalize to probabilities
ranking = visits / visits.sum()
print("PageRank:", ranking)
```

Output:
```
PageRank: [0.386, 0.193, 0.193, 0.096, 0.131]
```

**Page A is visited most often!** Why? Because:
- Page E links to A (and C)
- Page B links to A
- Page C links to A
- A has many incoming links from important pages

Page D is visited least because E links only to A and C.

---

## Patterns Emerge: The Circular Logic Resolves

The key insight is that this circular definition **actually resolves**. After enough steps, the random walker settles into a stable pattern—a stationary distribution.

The importance rank of page A is exactly its visit frequency. And critically, this importance is *self-consistent*: it depends only on the importance of pages linking to it.

But notice something: **Page D has no outgoing links!** This is called a "dangling node." Our surfer gets stuck there. In reality, they'd teleport to a random page or go back (use the back button).

---

## The Theory: PageRank Formalized

Let's formalize this into the PageRank algorithm.

### The Web as a Graph

- **Vertices**: webpages
- **Edges**: hyperlinks (directed: i → j means page i links to page j)
- **Outgoing links**: O(i) = number of links from page i

### The Transition Matrix

The basic transition matrix is:

$$P_{ij} = \begin{cases}
\frac{1}{O(i)} & \text{if } i \text{ links to } j \\
0 & \text{otherwise}
\end{cases}$$

This represents: "From page i, choose uniformly among its outgoing links."

### The Problem of Dangling Nodes

Some pages have no outgoing links (PDFs, images, dead-end pages). Our surfer gets stuck! We need to fix this.

**Solution**: Treat dangling nodes as linking to all pages uniformly:

$$P_{ij} = \begin{cases}
\frac{1}{O(i)} & \text{if } i \text{ links to } j \text{ and } O(i) > 0 \\
\frac{1}{N} & \text{if } O(i) = 0 \text{ (dangling node)} \\
0 & \text{otherwise}
\end{cases}$$

where N = total number of pages.

### The Teleportation Fix

Even with the dangling node fix, there's another problem: disconnected components. Imagine pages {A, B} that only link to each other, and {C, D} that only link to each other. A random walker starting in one component never reaches the other.

**Solution**: "Teleportation." With some probability, the surfer abandons clicking links and jumps to a random page:

$$P'_{ij} = d \cdot P_{ij} + (1 - d) \cdot \frac{1}{N}$$

where:
- $d$ = **damping factor** (usually 0.85)
- With probability $d$, follow a link
- With probability $(1 - d)$, teleport to any page

This ensures the chain is irreducible (you can eventually reach any page) and aperiodic (you settle into a steady state).

### The PageRank Vector

The **PageRank** is the stationary distribution of this modified chain:

$$\pi P' = \pi$$

In other words, if the visitation frequencies follow π, they'll stay that way after one step. The PageRank of page i is $\pi_i$.

The equation can be rewritten as:

$$\text{PageRank}(i) = \frac{1-d}{N} + d \sum_{j \to i} \frac{\text{PageRank}(j)}{O(j)}$$

This is elegant: the PageRank of page i is:
1. A baseline: $(1 - d)/N$ (everyone gets something)
2. Plus credit from pages linking to it, weighted by their importance and normalized by their outgoing links

---

## Going Deeper: Computing PageRank

Computing the stationary distribution directly is slow for billions of pages. Instead, we use the **power method**:

1. Start with any distribution: $\pi^{(0)} = [1/N, 1/N, \ldots, 1/N]$
2. Repeatedly apply the transition matrix: $\pi^{(k+1)} = \pi^{(k)} P'$
3. Stop when convergence: $|\pi^{(k+1)} - \pi^{(k)}| < \epsilon$

The power method is efficient and parallelizable—you can compute PageRank for billions of pages by distributing the computation across machines.

### The Damping Factor

The damping factor $d$ is a crucial design choice:

- **d = 0.5**: High teleportation. All pages become more equal. Less useful for ranking.
- **d = 0.85**: Standard. Good balance between following links and teleporting.
- **d = 0.99**: Low teleportation. Links matter a lot. Extreme ranking differences.

Higher d → smaller differences between popular and unpopular pages. Lower d → larger differences.

### Personalized PageRank

You can bias the teleportation:

$$P'_{ij} = d \cdot P_{ij} + (1 - d) \cdot \frac{T_j}{T}$$

where $T$ is a "preference vector" (not uniform). If you prefer technology pages, set $T$ high for tech pages, low otherwise. This gives you **personalized** PageRank—the ranking that matters to you.

This is more powerful than the original: it lets Google show different results to different people.

### The Eigenvector Interpretation

Mathematically, the PageRank vector is the principal left eigenvector of $P'$:

$$\pi P' = \pi$$

Eigenvalue decomposition reveals why this matters: the stationary distribution is the "natural" or "canonical" distribution for the system. It's the most stable, and it emerges regardless of starting conditions.

---

## Real Data: From Toy Networks to the Web

### Citation Networks

In academic papers, citations are links. PageRank on a citation network identifies the most influential papers—those that are cited by influential papers.

Compare:
- **In-degree**: Number of times cited (crude)
- **PageRank**: Importance accounting for who cited you (smarter)

A paper cited once by a highly influential paper may rank higher than a paper cited 10 times by obscure papers.

### Social Networks

On Twitter or social media, "follows" are links. PageRank identifies influential users—not just those with many followers, but those followed by influential people.

### Biology

Gene regulatory networks have links: gene A activates/represses gene B. PageRank identifies hub genes—those that regulate or are regulated by other important genes.

---

## Rabbit Holes

### The Original Brin & Page Paper

In 1998, Sergey Brin and Lawrence Page published "The Anatomy of a Large-Scale Hypertextual Web Search Engine" (worth reading). Their insight was deceptively simple:
- Query-independent ranking: instead of matching keywords, rank by importance
- Importance from link structure: self-reinforcing and hard to fake

The paper is short, readable, and revolutionary. Every search engine worth its salt has incorporated some version of PageRank.

### The Hilltop Algorithm

An alternative approach: pages are important if they're linked by "hubs." A hub is a page with many outgoing links to topical authorities. This creates a dual ranking: hubs and authorities.

It's mathematically interesting and sometimes better than PageRank for topic-specific queries, but PageRank is simpler and more robust.

### Detecting and Punishing Manipulation

Early spammers tried to game PageRank by creating "link farms"—networks of fake pages linking to their target page.

Google learned to detect these by:
- Analyzing link patterns (do links look natural?)
- Trust scores (pages linked from old, reputable pages score higher)
- Manual review of suspicious patterns

The arms race between SEO and search engines continues to this day.

### PageRank Beyond Search

PageRank has been applied everywhere:
- **Biology**: Identifying disease genes by importance in protein networks
- **Economics**: Ranking industries by economic dependency
- **Epidemiology**: Finding super-spreader nodes in disease networks
- **Neuroscience**: Important brain regions from connectivity

It's a general tool for finding importance in networks.

---

## Summary

PageRank is one of the most elegant algorithms in computer science. It shows that:

1. **Simple rules produce complex behavior**: A random walk generates meaningful ranking
2. **Importance is self-reinforcing**: A page matters because important pages link to it
3. **Markov chains solve real problems**: Theory meets practice at Google scale
4. **Network structure encodes information**: Links are votes of importance

The key insight that makes PageRank work: *let the structure speak for itself*. Don't try to understand "what makes a good page"—instead, let the collective voting of the web (through links) define importance.

This is why PageRank was revolutionary. Before Google, search engines used keyword matching and manual directories. Google said: ignore keywords, just follow links. The result was a search engine that actually worked.

---

## Exercises

See [exercises.md](exercises.md) for 15 progressive exercises covering:
- Warm-up: Build and simulate a toy web
- Exploration: Effects of damping factor and network structure
- Challenge: Create and detect link farm attacks
- Thought experiments: Ranking in the real world
