# Chapter 9 Exercises: The Chain That Ranked the Internet

## Warm-up Exercises

**1. Build a 5-page web and compute PageRank**

Using the example from the chapter:
- A → B, C
- B → A, D
- C → A, D
- D → E
- E → A, C

Compute PageRank using the power method. Do this by hand (matrix multiplication) for 3 iterations, starting from uniform distribution [1/5, 1/5, 1/5, 1/5, 1/5].

Compare your result to the limiting distribution.

---

**2. PageRank vs. In-Degree**

For the same 5-page web, compute:
- **In-degree ranking**: Score each page by number of incoming links, normalized
- **PageRank ranking** (with damping=0.85)

Compare the rankings. Are they different? If so, which page moved?

---

**3. Handle dangling nodes**

Add a new page F to the example with no outgoing links. Without the dangling node fix, the random walk gets stuck at F. With the fix (dangling nodes link uniformly to all pages), the walk continues.

Compute PageRank with and without the fix. How does page F's rank change?

---

## Exploration Exercises

**4. Damping factor sensitivity**

For the 5-page web, compute PageRank with damping factors d = 0.5, 0.75, 0.85, 0.95, 0.99.

Plot PageRank of all pages vs. damping factor. Notice how:
- Lower d: all pages become more equal
- Higher d: differences magnified

Which ranking do you find more intuitive?

---

**5. Different graph topologies**

Create three graphs:
1. **Ring**: A→B→C→D→A (each page links to next)
2. **Star**: Center links to all, all link to center
3. **Chain**: A→B→C→D→E (one direction only)

Compute PageRank for each. Which graph produces the most equal distribution? Which is most unequal?

Why do you think this is?

---

**6. Power method convergence**

Implement the power method and track how PageRank changes with each iteration. For the 5-page web, how many iterations before convergence (at tolerance 1e-6)?

Plot the PageRank of each page vs. iteration. Do some pages converge faster than others?

---

**7. Random walk approximation**

Compute PageRank by simulation (random walk) and compare to the power method. Use 10K, 100K, 1M, and 10M steps.

How many steps are needed to get within 1% of the power method result?

---

## Challenge Exercises

**8. Link farm attack**

Create a ring graph with 10 pages. Page 0 starts with standard PageRank.

Now create a link farm: 20 new pages that all link to page 0. Recompute PageRank.

How much did page 0's rank increase? Express as a multiplier (e.g., "5x boost").

Can you design a farm that boosts page 0 even more? (Try different strategies: more farms, self-linking, cycles.)

---

**9. Detecting link farms**

The farms you created in Exercise 8 have unnatural properties:
- All farms link to the same target
- Farms have high clustering (many links among themselves)
- Farms have unusual link patterns

Implement a "suspicion score" for each page based on its neighborhood. Can you identify the link farm pages?

---

**10. Personalized PageRank**

Modify the PageRank algorithm to add a "preference vector" P where some pages have higher teleport probability:

$$\text{PageRank}'(i) = d \cdot \text{(link-based)} + (1-d) \cdot P(i)$$

Set P to prefer pages 0 and 1. How does their rank increase compared to standard PageRank?

---

**11. Topic-specific ranking**

You have two topics: Tech and News. Some pages are labeled Tech, others News.

Compute personalized PageRank that teleports to random Tech pages (ignoring News) and random News pages (ignoring Tech).

Compare the rankings. Are they different? Which pages move up in each ranking?

---

**12. Dead end handling**

Instead of treating dangling nodes as linking to all pages, treat them as linking to a random page uniformly:

```python
if outgoing_links == 0:
    P[i, :] = 1.0 / n_pages  # Current approach
else:
    # Alternative: "restart" via teleportation (already in PageRank)
```

Recompute PageRank for the 5-page web with and without dangling node handling. Is there a difference?

---

## Thought Experiments

**13. Circular ranking logic**

The PageRank equation says: "You're important if important pages link to you."

This is circular: importance depends on importance. Yet it works! Why?

Hint: Think of it as a system of equations. Every page's rank is defined in terms of others' ranks. This system has a unique solution under certain conditions (irreducibility, aperiodicity).

---

**14. Biased clicking**

PageRank assumes clicking is uniform: "From page A, click a random outgoing link."

But real users are biased: they're more likely to click links near the top, links with good anchor text, etc.

How would human click patterns change the ranking? What pages would become more important?

Could this be gamed? (Yes—this is modern SEO!)

---

**15. Trapped components**

Imagine the web has two disconnected islands: pages {A, B, C} link only among themselves, and {D, E, F} link only among themselves.

Without teleportation, a random walker starting in island 1 never reaches island 2. With teleportation, they eventually can.

How does the teleportation probability (1-d) affect how often they cross between islands?

---

## Open-Ended Exploration

**PageRank on a real network**

Find a dataset: Wikipedia links, academic citation networks, social network follow graphs, etc.

1. Build the graph
2. Compute PageRank
3. Analyze the top 10 ranked nodes (what do they have in common?)
4. Compare to in-degree ranking (are they different?)
5. Try different damping factors (does ranking change much?)

Write up your findings.

---

**PageRank applications**

PageRank has been applied to:
- Citation networks (identifying influential papers)
- Protein interaction networks (finding disease-related proteins)
- Metabolic networks (identifying essential reactions)
- Social networks (finding influencers)

Pick one domain and:
1. Explain why PageRank makes sense there
2. Discuss what ranking would mean (what does it mean for a protein to be "important"?)
3. Propose an improvement to basic PageRank for that domain

---

**The history of PageRank**

Read about how Google evolved PageRank:
- Original 1998 Brin & Page paper
- How modern Google Search uses (many factors, not just PageRank)
- The rise of SEO and Google's response
- The 2016 patent expiration

Write a brief essay on how PageRank changed the internet.
