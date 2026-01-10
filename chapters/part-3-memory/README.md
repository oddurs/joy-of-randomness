# Part 3: Memory

## Markov Chains and How the Past Constrains the Future

In Parts 1 and 2, we watched random sequences and random walks unfold. Now we ask: *what if the future depends on the past?* 

A Markov chain is a random system where the next state depends only on the current state, not on how you got there. This simple structure—memory of only one step back—turns out to be incredibly powerful and describes everything from weather to web crawlers to protein folding.

In Part 3, you'll learn that randomness with memory creates new patterns. You'll see how to compute probabilities in a Markov chain, recognize when a system reaches a "stationary distribution," and understand why the structure of transitions matters more than you'd expect.

---

## Chapters in Part 3

1. **[Chapter 7: What Comes Next?](07-what-comes-next/README.md)**
   - Introduction to Markov chains
   - Transition matrices and state spaces
   - Computing probabilities of future states

2. **[Chapter 8: Chains Everywhere](08-chains-everywhere/README.md)**
   - Stationary distributions: when chains "settle down"
   - Ergodicity and mixing times
   - Markov chains in climate, language, and web ranking

3. **[Chapter 9: The Chain That Ranked the Internet](09-the-chain-that-ranked-the-internet/README.md)**
   - PageRank and the power of Markov chains
   - How Google uses random walks to find important pages
   - Convergence to stationary distributions in practice

---

**Previous:** [← Part 2: Movement](../part-2-movement/README.md) | **Next:** [Part 4: Simulation →](../part-4-simulation/README.md)
