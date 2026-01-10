# Chapter 14: Queues and Waiting

## Metadata

```yaml
Part: 5 - Modeling
Topics: Queueing theory, service systems, arrival processes, traffic intensity
Key Concepts: M/M/1 queues, Little's Law, waiting time distributions, queue length
```

---

## Why You Wait Even When There's Enough Capacity

You're in line at the coffee shop. There's one barista, and customers arrive randomly. Sometimes there's no line; sometimes it's out the door.

Even when the barista is fast enough *on average*, you still wait.

Why?

The answer is randomness. Arrivals cluster. Service times vary. These fluctuations create temporary overloads, and queues form.

This chapter explores queueing theory—a branch of probability that explains why waiting is inevitable in any system with random demand.

---

## First Contact: The M/M/1 Queue

The simplest queue has:
- **One server** (the barista)
- **Random arrivals**: customers arrive according to a Poisson process with rate λ (average arrivals per unit time)
- **Random service**: each service takes exponential time with rate μ (average services per unit time)

This is called the **M/M/1 queue** (Markovian arrivals, Markovian service, 1 server).

### Simulate It

```python
# Simulate an M/M/1 queue
arrivals = poisson_process(lambda=0.8, t_max=1000)  # 0.8 customers/minute
services = exponential(mu=1.0, n=len(arrivals))      # average 1 minute service

queue_length = []
current_time = 0
while queue_not_empty or more_arrivals:
    # Process arrivals and departures
    # Track queue length
    queue_length.append(current_queue)
```

Run this and plot queue length over time. You'll see:
- Queue length fluctuates: sometimes 0, sometimes 10+
- Average queue length is well-defined (despite fluctuations)
- The queue occasionally gets large, but eventually drains

### The Key Parameters

**Utilization**: $\rho = \frac{\lambda}{\mu}$

This is the fraction of time the server is busy. If $\rho < 1$, customers arrive slower than the server can handle (on average). If $\rho = 1$, they arrive at the same rate the server handles them. If $\rho > 1$, the queue grows without bound.

Think of it like a bathtub:
- Water flows in at rate λ
- Water drains at rate μ
- If λ < μ, the tub stabilizes at some level
- If λ > μ, the tub overflows

---

## Patterns Emerge

### What Happens at Different Utilization Levels

**ρ = 0.5** (server is busy half the time):
- Average queue length: small
- Occasional wait, but usually quick
- System feels responsive

**ρ = 0.8** (server is busy 80% of the time):
- Average queue length increases dramatically
- Frequent waits
- System feels slow

**ρ → 1** (approaching capacity):
- Average queue length explodes to infinity
- Waits become very long
- System becomes unstable

This is the central insight: **capacity isn't just about average throughput—it's about stability.**

### Why Not Just Increase Capacity?

If we know λ and μ, why not set μ to be much larger than λ?

**In practice**: you can't. Capacity costs money. But you can't set it arbitrarily high. Queueing theory tells us: to get acceptable waiting times, you need slack. A server at 90% utilization feels very different from one at 70%.

---

## The Theory

### Poisson Arrivals and Exponential Service

A **Poisson process** with rate λ models random arrivals:
- Probability of exactly k arrivals in time interval [0, t]: $P(N(t) = k) = \frac{e^{-\lambda t} (\lambda t)^k}{k!}$
- Arrivals are memoryless: the time until the next arrival is exponential with rate λ
- Average inter-arrival time: 1/λ

**Exponential service times** with rate μ:
- Service time has pdf: $f(t) = \mu e^{-\mu t}$
- Average service time: 1/μ
- Also memoryless: remaining service time is independent of how long the customer has been in service

### Stationary Distribution

For M/M/1 with ρ = λ/μ < 1, there exists a stationary (long-run) distribution of queue lengths:

$$P(N = n) = (1 - \rho) \rho^n \quad \text{for } n = 0, 1, 2, \ldots$$

This means:
- Probability the queue is empty: $P(N=0) = 1 - \rho$
- Probability there are n customers: geometric distribution with parameter ρ
- Average queue length: $L = \frac{\rho}{1-\rho}$

Notice: as ρ → 1, average queue length → ∞. This explains why queues explode near capacity.

### Little's Law

**Little's Law** is one of the most general results in queueing theory:

$$L = \lambda W$$

where:
- L = average number of customers in the system
- λ = arrival rate
- W = average time a customer spends in the system

In other words: **the average queue length equals the arrival rate times the average wait time.**

This holds for any queue, any arrival process, any service process. It's a conservation law.

Example: If customers arrive at 0.8 per minute and spend on average 5 minutes in the system, then on average there are 0.8 × 5 = 4 customers in the system.

### Waiting Time Distribution

The average wait in an M/M/1 queue is:

$$W = \frac{1}{\mu(1-\rho)}$$

And the probability a customer waits more than time t is:

$$P(W > t) = \rho e^{-\mu(1-\rho)t}$$

So waits follow an exponential distribution (shifted by the service time).

---

## Going Deeper

### Multiple Servers: M/M/c Queues

What if the coffee shop adds another barista? Now we have c servers.

With c servers, the stability condition becomes: $\rho = \frac{\lambda}{c \mu} < 1$.

The stationary distribution is more complex, but the intuition is the same: having multiple servers dramatically reduces waiting times.

**Key insight**: one server at 50% utilization is not the same as two servers at 25% utilization each. Adding parallelism helps.

### Non-Exponential Service: M/G/1 Queues

Real service times aren't exponential. They might be:
- Deterministic (always 5 minutes)
- Highly variable (some tasks quick, some long)
- Bimodal (two different job types)

For M/G/1 (Poisson arrivals, General service, 1 server), the average wait is:

$$W = \frac{\rho}{2\mu(1-\rho)} \left(1 + C_s^2\right)$$

where $C_s^2$ is the squared coefficient of variation of service times.

**Important**: if service times have high variability, waiting times increase, even with the same average service rate. Variability in the system makes things worse.

### Priority Queues

Suppose some customers are high-priority. Should they jump the line?

Queueing theory says: yes, prioritizing high-value (or time-sensitive) customers reduces their wait. But it increases wait for low-priority customers.

The tradeoff depends on costs.

### Networks of Queues

Many systems aren't single queues—they're networks. Customers move from queue to queue.

Example: a factory with multiple machines, or a hospital with waiting areas, triage, diagnosis, treatment.

**Jackson networks** extend queueing theory to networks of queues. Key result: if the network is "well-behaved," the system decomposes into independent M/M/1-like queues, and the stationary distribution is a product of individual queue distributions.

This is a remarkable result: the network solution is often simpler than expected.

---

## Real Data: Where Queues Appear

### Call Centers

Call center data reveals:
- Arrivals follow roughly a Poisson process (with daily and weekly patterns)
- Service times are variable but approximately exponential
- Call routing algorithms optimize for both customer wait time and agent utilization
- Real call centers operate at high utilization (70-80%) because customer wait is valued less than agent efficiency

### Traffic Flow

Cars on a highway form a queueing system:
- Vehicles arrive at a toll booth or bottleneck
- Service time is the time to pass through
- Arrivals are Poisson-like; service times are relatively fixed
- During rush hour, utilization spikes, creating congestion

Queueing theory explains why a small bottleneck creates a large traffic jam: the queue is buffering the mismatch between supply and demand.

### Internet Packets

Packets arriving at a router form a queue:
- Arrivals follow a Poisson process (aggregate traffic)
- Service time is the transmission time (related to packet size and link speed)
- If arrival rate exceeds service rate, the buffer fills, and packets are dropped (lost)

This is why network performance degrades gracefully until the system saturates, then collapses.

### Supermarket Checkout

One queue or multiple? Queueing theory says: **one queue feeding multiple registers is better** than separate queues per register.

Why? Because with one queue, you balance load across registers. With separate queues, some registers have long lines while others are idle.

The configuration matters: average capacity, but also how it's structured.

---

## Rabbit Holes

### Agner Krarup Erlang: The Birth of Queueing Theory

In 1909, Erlang (a Danish mathematician) worked for the Copenhagen telephone exchange. He wondered: how many telephone lines do we need to handle demand?

He modeled arrivals as Poisson and derived the **Erlang B formula** for blocking probability in a phone system. This was the first application of queueing theory and launched the field.

### Queueing in Computer Science

In computer systems, queueing appears everywhere:
- CPU scheduling: processes wait for the processor
- Memory: requests queue for cache/memory access
- Networks: packets queue in routers and NICs
- Disk I/O: requests queue for disk access

Understanding queueing helps system designers optimize for latency and throughput.

### The Psychology of Waiting

Queueing theory tells us how long we'll wait. But psychology tells us how long it *feels* like we wait.

Disney is famous for psychological tricks:
- Visible progress (progress bars, distance markers)
- Distraction (decorations, animations)
- Uncertainty reduction (posted wait times)

The DMV feels slow partly because of uncertainty and invisibility. Queueing theory is cold math; psychology is the lived experience.

---

## Summary

Queues form because of randomness. Even with adequate average capacity, random fluctuations in arrivals and service times create temporary bottlenecks.

**Key insights:**

1. **Utilization matters**: a system at 90% utilization is fundamentally different from one at 70%, even though both are "mostly full."

2. **Slack is essential**: to keep waiting times reasonable, you need extra capacity beyond the minimum average.

3. **Little's Law connects** average queue length, arrival rate, and wait time—a universal principle.

4. **Variability makes things worse**: high variance in service times increases waiting, even with the same average.

5. **Structure matters**: how you organize queues (single vs. multiple, priority rules, routing) affects outcomes.

Queueing theory is everywhere: roads, phone systems, hospitals, supermarkets, the internet. Understanding it helps explain why waiting is universal and how to design systems that wait less.

---

## Exercises

See [exercises.md](exercises.md) for 15 progressive exercises covering:
- Warm-up: Simulate M/M/1, verify stationary distribution
- Exploration: Waiting time vs. utilization, adding servers, non-exponential service
- Challenge: Multiple queues, priority routing, network effects
- Thought experiments: Designing systems for fairness vs. efficiency, psychological factors
