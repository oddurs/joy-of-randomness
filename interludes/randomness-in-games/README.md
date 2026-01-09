# Interlude: Randomness in Games

## Metadata
- **Type**: Interlude (optional detour)
- **Topics**: Game theory, probability in strategy, random outcomes in competition, game design
- **Key Concepts**: Nash equilibrium, mixed strategies, luck vs skill, game balance, information asymmetry
- **Difficulty**: Intermediate (requires Chapter 2–3 understanding)

---

## Why Games Need Randomness

Picture a game with no randomness. Chess, for instance. If both players play optimally, the outcome is predetermined. Either white wins, black wins, or it's a draw—and the same result happens every game.

Now picture poker. You don't know your opponent's cards. The deck is shuffled randomly. You have to make decisions under uncertainty. Over a hundred hands, the better player wins. Over one hand, anyone might.

Randomness is what makes games interesting.

Not just interesting—it's essential to game design. Randomness serves multiple purposes:

1. **Unpredictability**: You don't know what will happen, so every decision matters.
2. **Replayability**: The same game feels different each time.
3. **Fairness**: Random chance can level the playing field.
4. **Tension**: Uncertainty creates drama.
5. **Strategy**: Knowing what *might* happen requires probabilistic thinking.

The question isn't whether games should have randomness. It's how much, and where.

## Matching Pennies and Mixed Strategies

Two players reveal a coin simultaneously. Both show either heads or tails.

- **Player A** wins if both show the same.
- **Player B** wins if they differ.

What should each player do?

```python
import numpy as np
import matplotlib.pyplot as plt

# Strategy 1: Always show heads
# Opponent learns this and always shows tails → A loses every game
strategy_always_heads = [1, 0, 1, 0, 1, 0]  # 1 = heads, 0 = tails

# Strategy 2: Alternate heads-tails
# Opponent learns this and shows tails-heads → A loses every game
strategy_alternate = [1, 0, 1, 0, 1, 0]

# Strategy 3: Flip a fair coin each time
np.random.seed(42)
num_games = 100
strategy_random = np.random.randint(0, 2, num_games)  # 50% heads, 50% tails

print("Strategy 1 (always heads) - opponent responds with all tails:")
print(f"  Win rate: {sum(strategy_always_heads[i] == strategy_always_heads[i] for i in range(len(strategy_always_heads)))}")
print(f"  Opponent's best response: always show tails")

print("\nStrategy 3 (random 50-50):")
print(f"  In 100 games: {sum(strategy_random)} heads, {100 - sum(strategy_random)} tails")
print(f"  Against any deterministic opponent, expected win rate: 50%")
print(f"  Against random opponent, expected win rate: 50%")

# The key insight: randomness protects you from exploitation
```

If Player A always shows heads, Player B learns this and always shows tails. A loses forever.

But if A randomizes—flipping a fair coin—then B has no way to do better than 50-50.

This is the heart of game theory: **randomness is a defense against exploitation**.

## Patterns Emerge: Nash Equilibrium and Mixed Strategies

Here's where game theory gets interesting. In 1950, John Nash proved that every game has at least one equilibrium: a strategy profile where no player wants to unilaterally change.

Sometimes the equilibrium is pure—always do one thing. Sometimes it's mixed—randomize.

**Rock, Paper, Scissors:**

```python
# Rock-Paper-Scissors payoff matrix (from Player A's perspective)
# Rows: A's choice, Columns: B's choice
payoff_A = np.array([
    [0, -1, 1],   # A plays Rock
    [1, 0, -1],   # A plays Paper
    [-1, 1, 0]    # A plays Scissors
])

# If A always plays Rock, B learns and always plays Paper
print("If A always plays Rock:")
print(f"  B responds with Paper and wins every game")

# What if A randomizes?
# A plays 1/3 Rock, 1/3 Paper, 1/3 Scissors
# What's B's best response?

# Against uniform A:
# - If B plays Rock: expected payoff = -1/3 (1 * 0 + 1 * (-1) + 1 * 1) / 3 = -1/3
# - If B plays Paper: expected payoff = -1/3
# - If B plays Scissors: expected payoff = -1/3

# B gets the same expected payoff no matter what!
# So B is indifferent. B might as well randomize too.

print("\nIf A plays 1/3-1/3-1/3 (uniform mixed strategy):")
print(f"  B's expected payoff is the same (-1/3) regardless of B's strategy")
print(f"  B is indifferent, so B might as well also play 1/3-1/3-1/3")
print(f"  Expected outcome: 0-0 draw")

# This is Nash equilibrium in Rock-Paper-Scissors:
# Both players randomize uniformly. No one can improve by deviating.

def simulate_rps(num_games, p_a_strategy, p_b_strategy):
    """Simulate Rock-Paper-Scissors."""
    choices = {'R': 0, 'P': 1, 'S': 2}
    wins_a = 0
    
    for _ in range(num_games):
        a_choice = np.random.choice(['R', 'P', 'S'], p=p_a_strategy)
        b_choice = np.random.choice(['R', 'P', 'S'], p=p_b_strategy)
        
        a_idx = choices[a_choice]
        b_idx = choices[b_choice]
        
        # Determine winner
        if a_choice == b_choice:
            pass  # Draw
        elif (a_choice == 'R' and b_choice == 'S') or \
             (a_choice == 'P' and b_choice == 'R') or \
             (a_choice == 'S' and b_choice == 'P'):
            wins_a += 1
    
    return wins_a

# Nash equilibrium: both play 1/3-1/3-1/3
uniform = [1/3, 1/3, 1/3]
wins = simulate_rps(1000, uniform, uniform)
print(f"\nNash equilibrium (1000 games): A wins {wins}, B wins {1000-wins}, draws {wins * 0 + (1000 - 2*wins)}")
print(f"(Close to equal, as expected)")

# What if one player deviates?
biased_strategy = [0.5, 0.25, 0.25]  # Play Rock more often
wins = simulate_rps(1000, uniform, biased_strategy)
print(f"\nA plays uniform, B plays [0.5, 0.25, 0.25]: A wins {wins}")
print(f"(A does better, because B is predictable)")
```

The key insight: **in a symmetric game with no pure Nash equilibrium, the equilibrium often involves randomization**. Both players mix their strategies, making themselves unpredictable.

---

Let's formalize this. Suppose a game is symmetric (both players have the same options and payoffs). Neither pure strategy (always do one thing) is stable.

The mixed strategy Nash equilibrium is the probability distribution that makes your opponent indifferent.

**Poker Example (Simplified):**

Two players, antes are in. Each is dealt either Strong or Weak.

```python
# Simplified poker: heads-up, one decision point
# Both players have antes, now deciding whether to fold or go all-in

# Payoff matrix (from first player's perspective)
# Rows: P1's action (F=fold, A=all-in)
# Columns: P2's action (F=fold, A=all-in)

# If P1 has Strong hand:
payoff_strong = np.array([
    [0, -1],   # P1 folds: ante lost (0) vs. wins 1 if P2 folds
    [1, 1]     # P1 all-ins: wins 1 if P2 folds, wins 1 if P2 all-ins (strong wins)
])

# If P1 has Weak hand:
payoff_weak = np.array([
    [0, -1],   # P1 folds: ante lost
    [1, -2]    # P1 all-ins: wins 1 if P2 folds, loses 2 if P2 all-ins
])

# Strategy: sometimes bluff with weak hand, sometimes fold with strong hand
# (Counter-intuitive? That's the point!)

print("P1 optimal strategy:")
print(f"  With Strong hand: always all-in (payoff = 1 regardless)")
print(f"  With Weak hand: mix between fold and all-in")

# Find the mix for weak hand that makes P2 indifferent
# If P1 goes all-in with probability p when holding weak:
# P2's expected payoff from folding: 0 (ante won)
# P2's expected payoff from all-in: depends on whether P1 is bluffing

# For P2 to be indifferent: P1's bluff frequency must be calibrated
# Such that P2's expected value from calling = expected value from folding

print("\nKey poker insight:")
print("  - Always raise with strong hands")
print("  - Occasionally bluff with weak hands")
print("  - The bluffing frequency keeps opponents from exploiting you")
```

This is why poker is a battle of probabilities. Expert players don't just play their cards—they adjust their mixing frequency based on:

- How many people are at the table
- Stack sizes
- Position
- The community cards
- Opponent tendencies

The goal: be unpredictable enough that opponents can't exploit you, but not so random that you lose optimality.

---

## Going Deeper: Skill vs. Luck in Games

Here's a question that divides the gaming world: Is poker a game of skill or luck?

The answer is yes—it's both.

```python
# Measuring skill vs. luck
# Over a single hand: luck dominates
# Over many hands: skill dominates

def evaluate_game(num_hands, skill_player_edge, variance):
    """
    Simulate a game over many hands.
    
    skill_player_edge: probability the better player wins (vs 50% baseline)
    variance: randomness per hand (higher = more luck)
    """
    
    better_player_wins = 0
    
    for _ in range(num_hands):
        # Skill advantage + luck
        luck_factor = np.random.normal(0, variance)
        outcome = (np.random.random() < skill_player_edge + luck_factor)
        
        if outcome:
            better_player_wins += 1
    
    win_rate = better_player_wins / num_hands
    confidence = (win_rate - 0.5) / (2 * np.sqrt(variance**2 / num_hands))
    
    return win_rate, confidence

# Scenario 1: Poker (moderate skill, moderate luck)
skill_edge = 0.55  # 5% skill edge
variance = 0.3

for num_hands in [10, 100, 1000, 10000]:
    wr, conf = evaluate_game(num_hands, skill_edge, variance)
    print(f"After {num_hands:5d} hands: {wr:.1%} win rate (confidence: {conf:.2f}σ)")

print("\nAfter 10 hands: luck often dominates")
print("After 10,000 hands: skill overwhelms luck")

# Why? Variance shrinks as 1/√n
# Skill edge grows as √n
# Eventually skill wins out

# This is why casinos ban professional poker players:
# Over enough hands, skill becomes deterministic
```

The relationship is quantifiable. In poker:

- **Per hand**: luck dominates. Anyone can win a single hand.
- **Over a session**: skill and luck are comparable. A bad streak can hurt.
- **Over a year**: skill overwhelms luck. The best players consistently win.

This is why poker has legal protection as "a game of skill" in some jurisdictions. Once you play enough hands, the better player will win most of the time.

Compare to roulette:

- **Per spin**: pure luck. No amount of skill helps.
- **Over 100 spins**: still luck. Everyone loses (due to house edge).
- **Over a year**: still pure luck with a guaranteed loss.

The distinction matters legally, morally, and personally.

```python
# The house edge in roulette vs. skill in poker
import numpy as np

# Roulette: 18 red, 18 black, 2 green
# If you bet on red: 18/38 = 47.4% win rate (2.6% house edge)
roulette_expected_return = 18/38 - 1/2  # Loss per $1 bet
print(f"Roulette: Expected loss per $1: {-roulette_expected_return:.3f}")

# Poker: depends on skill
# Average player against slightly better player: 51% win rate
# Average player against professional: 40% win rate
poker_skill_edge = 0.51
print(f"Poker (average vs slightly better): {poker_skill_edge:.1%} win rate")
print(f"Poker (average vs professional): 40% win rate")

print("\nRoulette is mathematically unbeatable.")
print("Poker rewards skill consistently.")
```

---

## Real Data: Video Game Design and Difficulty

Video games face a unique randomness challenge: they want to be fun, fair, and consistently challenging.

Too much randomness: players feel like they lack control.
Too little randomness: the game becomes predictable and boring.

**Enemy AI and Difficulty:**

```python
# Balancing difficulty through randomness

class EnemyAI:
    def __init__(self, difficulty):
        """
        difficulty: 0.0 (easy) to 1.0 (hard)
        """
        self.difficulty = difficulty
    
    def make_decision(self, player_position, own_position):
        """
        Make a decision: move toward player, or move randomly.
        Higher difficulty = more likely to move toward player.
        """
        # With probability `difficulty`, make optimal move
        if np.random.random() < self.difficulty:
            return self.move_toward_player(player_position, own_position)
        else:
            # With probability `1 - difficulty`, move randomly
            return self.move_random()
    
    def move_toward_player(self, player_pos, own_pos):
        return f"Move from {own_pos} toward {player_pos}"
    
    def move_random(self):
        return f"Move randomly"

# Simulate difficulty levels
print("Easy (difficulty=0.3):")
easy_ai = EnemyAI(0.3)
for _ in range(5):
    print(f"  {easy_ai.make_decision(10, 5)}")

print("\nHard (difficulty=0.9):")
hard_ai = EnemyAI(0.9)
for _ in range(5):
    print(f"  {hard_ai.make_decision(10, 5)}")

# This is how many games balance difficulty:
# - Easy: mostly random moves (player feels skillful)
# - Medium: mix of optimal and random (competitive)
# - Hard: mostly optimal moves with occasional surprises (challenging)
```

**Loot and Reward Randomness:**

Roguelike games (Hades, The Binding of Isaac) use randomness to create replayability.

```python
# Loot table design
# Each enemy drops a random item from a weighted distribution

class LootTable:
    def __init__(self):
        self.items = {
            'common': 50,      # 50% chance
            'uncommon': 30,    # 30% chance
            'rare': 15,        # 15% chance
            'legendary': 5     # 5% chance
        }
    
    def roll(self, num_drops=1):
        """Simulate loot drops."""
        items = list(self.items.keys())
        weights = list(self.items.values())
        
        drops = np.random.choice(items, size=num_drops, p=np.array(weights)/100)
        return drops

loot = LootTable()

# Single enemy
print("Single enemy drops:")
print(f"  {loot.roll(1)[0]}")

# After 100 enemies
drops_100 = loot.roll(100)
print(f"\n100 enemies drop:")
for item in loot.items:
    count = sum(drops_100 == item)
    expected = loot.items[item]
    print(f"  {item}: {count} (expected {expected})")

print("\nKey design insight:")
print("- Common drops feel frequent and satisfying")
print("- Rare drops create exciting moments")
print("- Over many runs, the probabilities balance gameplay")
```

Games carefully tune these probabilities. Too many rares, and everything feels cheap. Too few, and progression feels grindy.

**Procedural Generation:**

Some games use randomness to generate worlds.

```python
# Simple procedural dungeon: random room layout

def generate_dungeon(width, height, room_probability=0.6):
    """Generate a dungeon with random room placement."""
    dungeon = np.random.random((height, width)) < room_probability
    return dungeon.astype(int)

# Visualize
dungeon = generate_dungeon(10, 10)
print("Procedurally generated dungeon:")
for row in dungeon:
    print(''.join(['█' if cell else ' ' for cell in row]))

# Each time you play, a different dungeon
# But it follows the same ruleset, so it feels coherent
```

The challenge: randomness must feel **inevitable** (not manipulated) and **fair** (not frustrating).

---

## Going Deeper: Information and Bluffing

</details>

## Information Asymmetry: The Power of Secretsat uncertainty creates strategic depth.

**Bluffing in Poker:**

Without randomness, bluffing is impossible. If you always bluff with bad hands and fold good hands, opponents learn and exploit you.

But if you *sometimes* bluff and *sometimes* fold, you're unpredictable. This uncertainty forces opponents to think probabilistically.

```python
# Calculating bluff frequency
# You have weak hand, opponent raises

# Opponent will call if:
# Expected value of calling > Expected value of folding

# EV(call) = P(you bluffing) * (pot) + P(you have strong hand) * (-bet)
# EV(fold) = 0

# For opponent to be indifferent:
# P(bluff) * pot = P(strong) * bet

# If pot = bet (standard), then:
# P(bluff) / P(strong) = 1
# You should bluff as often as you bet for value!

print("Poker bluff frequency:")
print("You should bluff just as often as you bet for value")
print("This makes opponent indifferent between calling and folding")

# Example:
# You have strong hand 10% of the time (always bet)
# To balance: bluff 10% of the time
# Opponent's EV from calling: 0 (indifferent)
# Opponent's EV from folding: 0

print("\nIf you bet strong hands 10% of the time:")
print("  Optimal bluff frequency: 10% (of remaining hands)")
print("  Opponent is indifferent between calling and folding")
```

This principle—randomizing your play to make opponents indifferent—is the deepest insight from game theory.

---

## The Philosophical Perspective

## The Philosophical Perspective: Uncertainty as Agencysomething that *happens to us*. We roll dice and hope for lucky outcomes.

But in games, randomness is something we *deploy strategically*.

A poker player isn't hoping randomness helps them. They're using randomness to become unpredictable. They're turning uncertainty into an advantage.

This inverts the usual relationship. Randomness stops being noise and becomes a tool.

It's also why games are beautiful. The marriage of perfect information (chess) and hidden information (poker), determinism (roulette) and strategy (blackjack), pure luck (dice) and skill (professional gaming)—they reveal different aspects of how randomness and strategy interact.

```python
# Categorizing games by randomness

games = {
    'Chess': {
        'luck': 0,
        'skill': 100,
        'hidden_info': 0,
        'description': 'Perfect information, no randomness'
    },
    'Poker': {
        'luck': 30,
        'skill': 70,
        'hidden_info': 100,
        'description': 'Hidden cards, skill dominates long-term'
    },
    'Blackjack': {
        'luck': 40,
        'skill': 60,
        'hidden_info': 0,
        'description': 'Card randomness, some strategy'
    },
    'Dice Game': {
        'luck': 100,
        'skill': 0,
        'hidden_info': 0,
        'description': 'Pure chance, no decision-making'
    },
}

for game, stats in games.items():
    print(f"{game}:")
    print(f"  Luck: {stats['luck']}%")
    print(f"  Skill: {stats['skill']}%")
    print(f"  Hidden info: {stats['hidden_info']}%")
    print(f"  Description: {stats['description']}\n")
```

---

## Conclusion: The Joy of Uncertainty

Games teach us something profound: uncertainty isn't always bad.

In a deterministic world—where everything is known and predictable—there's no decision to make. You just execute the predetermined answer. It's sterile.

But in a world with randomness? Every decision matters. Your choice might fail, or it might succeed beyond your hopes. You have agency and uncertainty simultaneously.

That's what makes games compelling. And it's what makes them such powerful tools for thinking about probability.

When you play poker, you're practicing Bayesian reasoning. When you roll dice, you're experiencing variance. When you bluff, you're deploying game theory.

Games are randomness made tangible. And they're infinitely more interesting than a world without it.


---

**Explore Next:** [Interlude: Noise as Music](../noise-as-music/README.md) · [Interlude: Randomness in Cryptography](../randomness-in-cryptography/README.md)