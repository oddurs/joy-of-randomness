# Chapter 7 Exercises: What Comes Next?

## Warm-up Exercises

**1. Build a first-order Markov text generator**

Load a text file (Shakespeare, Bible, or any corpus you choose). Build a first-order Markov chain and generate 100 words starting with a random word from the text.

Does the output look like plausible language? What patterns emerge?

**Hint:** Use `load_text()`, `build_transition_matrix(order=1)`, and `generate_text()` from simulations.py.

---

**2. Visualize the transition structure**

Pick a common word (like "the" or "and"). Print out the 10 most likely words that follow it, with their probabilities.

```python
state = 'the'
next_words = transitions[state]
total = sum(next_words.values())
for word, count in next_words.most_common(10):
    prob = count / total
    print(f"  {word}: {prob:.3f}")
```

Do these match your intuition about English?

---

**3. Compare corpus entropy**

Load two different texts (e.g., Shakespeare and a news article). Build first-order models for each and compute their entropies.

Which has higher entropy? Why do you think that is?

**Hint:** Use `compute_entropy()`.

---

## Exploration Exercises

**4. Order comparison: Generate samples**

Build first-order, second-order, and third-order Markov chains on the same corpus. Generate 50 words from each (using the same starting state).

Compare the outputs:
- Order 1: Does it have local coherence?
- Order 2: Does it form recognizable phrases?
- Order 3: Does it form complete thoughts?

**Hint:** You can use the same starting words tuple for each: `generate_text(trans, ('to', 'be'), length=50, order=order)`.

---

**5. The memorization threshold**

Keep increasing the order (1, 2, 3, 4, 5) and generate text from each. At what order does the generator start reproducing the original text verbatim?

This is the "memorization threshold" for your corpus.

---

**6. Entropy curve**

Build Markov chains of order 1, 2, 3, 4, and 5 on your corpus. Compute entropy for each.

Plot entropy vs. order. Does it decrease monotonically? Does it plateau?

**Hint:** Use `compare_orders()` to build all chains at once.

---

**7. Perplexity on held-out data**

Split your corpus into training (80%) and test (20%). Build order-1, 2, and 3 models on training data. Compute perplexity on test data.

Which order gives the best test perplexity? Does higher order always help, or do you see overfitting?

**Hint:** `compare_orders()` already does this.

---

## Challenge Exercises

**8. Character-level model**

Repeat exercises 1-3, but at the character level instead of the word level. Build a first-order character model and generate 100 characters.

How is it different from the word-level model? Is it more or less coherent?

---

**9. Entropy estimation with different test sets**

Build a model on one corpus (e.g., Shakespeare). Compute its entropy. Then compute its perplexity on a completely different corpus (e.g., news articles).

The perplexity should be much higher (the model is surprised). Why?

---

**10. Estimate vocabulary growth rate**

Plot the number of states (vocabulary) vs. order on a log-log scale. What's the growth rate? Can you fit a power law?

```python
# If states ~ order^alpha, then log(states) = alpha * log(order)
# So the slope of the log-log plot is alpha
```

---

**11. The Shannon redundancy of English**

Shannon estimated that English has about 1-1.5 bits of entropy per character. Using a character-level model, estimate the entropy of English text.

How close are you to Shannon's estimate?

---

## Thought Experiments

**12. Long-range dependence**

Can you construct an English sentence where the next word critically depends on something many steps back?

Example: "The [lots of text] is ..."—where the verb agreement depends on a noun many words earlier.

A Markov chain (even high-order) would struggle with this. Why?

---

**13. The illusion of understanding**

A generated text can be locally plausible (good transitions) while globally nonsensical (no overall structure).

What cognitive tasks require global structure that a Markov model can't capture?

---

**14. From Markov chains to neural networks**

Modern language models (GPT, BERT) are often described as neural Markov chains. But they use distributed representations instead of explicit transition matrices.

What advantages does this provide? What might be lost?

---

**15. Compression and entropy**

The intuition: if you can predict something, you can compress it. A first-order model gets *some* compression; higher orders get more.

Use a standard compression tool (gzip) on your corpus. Compare its compression ratio to what you'd expect from your entropy estimates.

---

## Open-Ended Exploration

**Musical note sequences**

If you have access to a symbolic music file (like MIDI), extract sequences of musical notes. Build a first-order Markov chain and generate a new melody.

Does it sound musical? What orders of chords or melodies would humans find pleasing?

---

**Domain-specific text generation**

Pick a specialized domain (legal documents, medical writing, programming code, tweets) and build a model on it.

Generate samples and compare to the original. What stylistic markers does the model capture?
