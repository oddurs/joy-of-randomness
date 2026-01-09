# Chapter 7: What Comes Next?

## Hook

"Given the text of all Shakespeare's plays, what word is most likely to follow 'to be or not to'? What about after 'the'? It turns out you can generate surprisingly convincing pseudo-Shakespeare with nothing more than counting and rolling dice."

This is our gateway into one of the most powerful and elegant ideas in probability: the Markov chain. It's named after Andrey Markov, a Russian mathematician who in 1913 analyzed the sequence of vowels and consonants in Pushkin's poetry. His question was simple: does the next letter depend on the entire history of letters before it, or just the current one?

The answer was surprisingly powerful: if you only know the current word, you can predict the next word's probability distribution almost as well as if you knew everything before. This "short memory" property is the heart of Markov chains, and it appears everywhere—in weather, genetics, games, web rankings, and modern language models.

## First Contact

Let's build a text generator. We'll start with a classic: Shakespeare.

```python
import numpy as np
import re
from collections import defaultdict, Counter

def load_text(filename):
    """Load and preprocess text."""
    with open(filename, 'r') as f:
        text = f.read().lower()
    # Split into words
    words = re.findall(r'\b\w+\b', text)
    return words

def build_transition_matrix_order1(words):
    """
    Build a first-order Markov chain: P(word_i | word_{i-1})
    
    Returns:
        transitions: dict mapping each word to counts of what follows
    """
    transitions = defaultdict(Counter)
    
    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]
        transitions[current_word][next_word] += 1
    
    return transitions

def generate_text_order1(transitions, start_word, length=100):
    """Generate text using first-order Markov chain."""
    words = [start_word]
    
    for _ in range(length - 1):
        current_word = words[-1]
        
        if current_word not in transitions:
            break  # Dead end
        
        # Get probability distribution of next words
        next_words = transitions[current_word]
        candidates = list(next_words.elements())
        next_word = np.random.choice(candidates)
        words.append(next_word)
    
    return ' '.join(words)

# Example usage
words = load_text('shakespeare.txt')  # You'd need this file
transitions = build_transition_matrix_order1(words)
generated = generate_text_order1(transitions, 'to', length=100)
print(generated)
```

Run this on Shakespeare, and you get output like:

> to be the king. he had the good lord, the lord of my hand, and the king of the world, the lord, the king, and the great lord of the king...

It captures something: words that go together in English. "the king" appears, "good lord" appears. But there's no narrative, no long-range coherence. The chain "forgot" where it started.

This is the first-order Markov chain: the next word depends only on the current word. Simple. Powerful. Limited.

## Patterns Emerge

Now let's try higher orders. Instead of just remembering the previous word, remember the previous *two* words:

```python
def build_transition_matrix_order2(words):
    """
    Build a second-order Markov chain: P(word_i | word_{i-2}, word_{i-1})
    
    The state is now a pair of consecutive words.
    """
    transitions = defaultdict(Counter)
    
    for i in range(len(words) - 2):
        current_state = (words[i], words[i + 1])
        next_word = words[i + 2]
        transitions[current_state][next_word] += 1
    
    return transitions

def generate_text_order2(transitions, start_words, length=100):
    """Generate text using second-order Markov chain."""
    state = tuple(start_words)
    words = list(state)
    
    for _ in range(length - 2):
        if state not in transitions:
            break
        
        next_words = transitions[state]
        candidates = list(next_words.elements())
        next_word = np.random.choice(candidates)
        words.append(next_word)
        state = (state[1], next_word)
    
    return ' '.join(words)
```

Output (order 2):

> to be or not to be, and the king did not see the king, and he did love the king...

Better! Phrases like "to be or not" and "the king did" emerge. Longer-range structure appears.

Now try order 3:

> to be or not to be a king, and the lord and the lady of the court, and the king did marry the lady...

Better still! Longer sentences with more coherent grammar. But notice: as we increase the order, we're essentially memorizing more of the original text. By order 5 or 6, we're just reproducing Shakespeare verbatim.

This is the fundamental tradeoff: **higher order = more memory = more structure, but eventually you're just reproducing the training data.**

## The Theory

Let's formalize what's happening.

**The Markov property:**
A process has the Markov property if the future depends only on the present, not the past. Mathematically:

$$P(X_n = x_n | X_{n-1} = x_{n-1}, X_{n-2} = x_{n-2}, \ldots, X_0 = x_0) = P(X_n = x_n | X_{n-1} = x_{n-1})$$

For text, this becomes: the probability of the next word depends only on the current word (or n-gram), not on everything that came before.

**States and transitions:**
In a Markov chain, we have:
- **States**: in our case, words (or n-grams)
- **Transition probabilities**: $P(j | i)$ = probability of moving from state $i$ to state $j$

We can encode all these probabilities in a **transition matrix** $P$, where $P_{ij}$ is the probability of going from state $i$ to state $j$. Each row sums to 1 (it's a stochastic matrix).

For a small example, imagine states are {the, king, queen}:

$$P = \begin{pmatrix}
0.1 & 0.6 & 0.3 \\
0.4 & 0.2 & 0.4 \\
0.5 & 0.3 & 0.2
\end{pmatrix}$$

This says: if you're at "the", you have a 60% chance of "king" next, 30% of "queen", 10% of "the" again.

**Powers of the matrix:**
If we want to know the probability of transitioning from state $i$ to state $j$ in exactly $n$ steps, we compute $P^n$. This is useful for long-range predictions.

**Stationary distribution:**
After many transitions, the probability distribution over states settles into a fixed pattern $\pi$ (the stationary distribution), where:

$$\pi P = \pi$$

In other words, applying one more transition doesn't change the distribution. For text, this represents the long-run frequency of each word. The "start state" gets forgotten—we reach a steady state determined by the transition matrix itself.

## Going Deeper

**Order of a Markov chain:**
A first-order chain remembers 1 step back. A second-order chain remembers 2 steps back. In general, an $n$-th order chain remembers $n$ steps.

The tradeoff is real: with order 1, you have relatively few states (the number of unique words). With order 2, you have (number of unique word pairs). Order $n$ has $(\text{vocab size})^n$ possible states. This grows exponentially! You need exponentially more data to reliably estimate probabilities.

This is why modern neural language models (like GPT) don't build explicit transition matrices. Instead, they learn compressed, dense representations that capture long-range dependencies without building a matrix of size $(\text{vocab})^n$.

**Connection to compression:**
Markov models underlie much of text compression (ZIP, GZIP). The idea: if you can predict the next character well, you need fewer bits to encode it. A first-order model gives rough predictions; higher-order models predict better but require more bits to specify.

**Shannon's experiment:**
Claude Shannon in 1948 asked: how much can we predict English text? He had people guess the next letter, given all previous letters. On average, people got it right about 80% of the time for short texts. This reveals that English has strong structure—a first-order model should do pretty well.

But Shannon also showed: if we allow more history (higher-order), prediction improves. This is why modern language models, which effectively use very high-order context, are so powerful.

## Real Data

Let's apply Markov chains to different texts:

```python
def compute_entropy(transitions, order=1):
    """
    Compute the entropy of a Markov chain.
    Entropy H = -sum over all transitions of P(next|current) * log2(P(next|current))
    
    High entropy = more surprise, less predictable
    Low entropy = more predictable
    """
    total_entropy = 0
    total_transitions = 0
    
    for current_state, next_words in transitions.items():
        total_count = sum(next_words.values())
        for next_word, count in next_words.items():
            prob = count / total_count
            total_entropy -= prob * np.log2(prob)
            total_transitions += count
    
    return total_entropy

# Load different corpora
shakespeare_words = load_text('shakespeare.txt')
news_words = load_text('news_articles.txt')
legal_words = load_text('legal_documents.txt')

# Build chains
shak_trans = build_transition_matrix_order1(shakespeare_words)
news_trans = build_transition_matrix_order1(news_words)
legal_trans = build_transition_matrix_order1(legal_words)

# Compute entropies
shak_entropy = compute_entropy(shak_trans)
news_entropy = compute_entropy(news_trans)
legal_entropy = compute_entropy(legal_trans)

print(f"Shakespeare entropy: {shak_entropy:.3f} bits/word")
print(f"News entropy: {news_entropy:.3f} bits/word")
print(f"Legal entropy: {legal_entropy:.3f} bits/word")
```

What you'd find:
- **Shakespeare**: High entropy (~4-5 bits/word) because of rich vocabulary and varied sentence structures
- **News**: Medium entropy (~3-4 bits/word) because of more repetitive phrasing (proper nouns, formulaic sentences)
- **Legal documents**: Low entropy (~2-3 bits/word) because highly formulaic and repetitive

This makes sense: legal documents use the same phrases over and over. News uses set phrases but more variety. Shakespeare is baroque and varied.

Character-level models (predicting the next character instead of word) have even lower entropy because letters like 'q' are almost always followed by 'u'.

## Rabbit Holes

**Andrey Markov and his obsession with Pushkin**

Markov was a rigorous mathematician at St. Petersburg University. In 1906-1913, late in his career, he became fascinated with analyzing the sequences of vowels and consonants in Alexander Pushkin's novel *Eugene Onegin*. He did this work to demonstrate that the law of large numbers—the foundation of probability—could apply to dependent sequences, not just independent ones.

Ironically, his analysis of Russian literature became more famous than his original theorem. Markov died in 1922, just as probability theory was about to revolutionize the 20th century. He never saw his chains applied to weather, genetics, or the internet.

**Shannon and the birth of information theory**

In 1948, Claude Shannon published "A Mathematical Theory of Communication," which founded the field of information theory. One section analyzed English text using Markov chains. Shannon showed that you can generate increasingly realistic English by training on higher-order chains.

In one famous experiment, he had people read a passage and then guess the next letter. For blocks of 100 letters, people guessed right about 80% of the time—showing that English has massive redundancy. Shannon estimated the entropy of English at about 1-1.5 bits per character.

This work connected probability, linguistics, and the practical challenge of compressing and transmitting information. It's the foundation for everything from ZIP files to cellular networks.

**Markov chains in music generation**

Just as text generators can produce plausible sentences, music generators can produce plausible melodies. By analyzing sequences of musical notes or chords, you can build a Markov chain and generate new compositions "in the style of" a composer.

David Cope, a composer and AI researcher, created EMMY (Experiments in Musical Intelligence), which uses Markov-like models to generate new compositions inspired by classical music. The results are sometimes indistinguishable from human composition—and sometimes obviously mechanical.

This hints at a deep question: how much of artistic style is just pattern, statistically speaking?

## Summary

A Markov chain is a system with short memory: the future depends only on the present, not the past. This simple constraint is surprisingly powerful. By building a transition matrix from data—whether text, weather, genetics, or stock prices—we can simulate, predict, and understand complex systems.

The key insight is that you don't need to remember everything to predict what comes next. A few orders of dependence capture most of the structure. This is why Markov models appear everywhere, and why they remain central to modern machine learning and signal processing.

But there's a limit: as order increases, you need exponentially more data, and you risk memorizing rather than learning. Modern language models (like GPT) solve this by learning distributed representations instead of explicit transition matrices. But conceptually, they're still Markov chains—just with very long effective memory encoded implicitly.

### Exercises

1. **Warm-up:** Build a first-order Markov text generator from a corpus of your choice (you can use Shakespeare, the Bible, or any text file). Generate 100 words starting with a random word. Does it read like plausible language?

2. **Exploration:** Compare first-order, second-order, and third-order models on the same corpus. Generate 50 words from each and describe how the output changes. At what order does it start reproducing the original text too closely?

3. **Challenge:** Implement a function to compute the empirical entropy of a Markov chain (in bits per word or bits per character). Compute entropy for order 1, 2, and 3 models on your corpus. Does entropy decrease with higher order? Why or why not?

4. **Thought experiment:** Modern language models like GPT can remember hundreds of tokens (far longer than any practical Markov chain order). What aspects of language require this long-range memory? Can you think of sentences where the next word depends critically on something many steps back?

5. **Open exploration:** Find a different text corpus (news articles, legal documents, poetry, code). Build a Markov model and generate text. How does the style differ from your first corpus? Can you adjust model order to capture the distinctive style of the text?
