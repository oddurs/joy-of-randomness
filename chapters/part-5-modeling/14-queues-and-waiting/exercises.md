# Chapter 14 Exercises: Queues and Waiting

## Warm-up Exercises

**1. Simulate an M/M/1 queue**

Use `simulations.py` to simulate an M/M/1 queue with:
- λ = 0.8 (arrival rate)
- μ = 1.0 (service rate)
- t_max = 1000 (simulation time)

Compute:
- Average queue length from simulation
- Theoretical average queue length: L = ρ/(1-ρ)
- How close are they?

Also plot the queue length over time and the distribution of wait times.

---

**2. Verify Little's Law**

Little's Law states: L = λW

Run the simulation above. Compute:
- Average queue length L (from simulation or theory)
- Average wait time W (from simulation)
- λ × W (should equal L)

Does Little's Law hold?

---

**3. Queue length distribution**

For the M/M/1 queue with λ=0.8, μ=1.0:

Theory predicts: P(n customers) = (1-ρ)ρ^n

Run a long simulation and collect queue lengths at regular time intervals (e.g., every 100 time units). Histogram the queue lengths. Does it match the theoretical distribution?

---

**4. Effect of utilization on wait time**

Fix μ = 1.0. Vary λ from 0.1 to 0.95 (so ρ goes from 0.1 to 0.95).

For each λ:
- Compute theoretical average wait time: W = 1/(μ(1-ρ))
- Plot W vs. ρ

Describe what you see. How does wait time behave as you approach capacity?

---

## Exploration Exercises

**5. Adding a server**

Compare M/M/1 and M/M/2 (two servers):
- Both handle the same total traffic: λ = 0.8
- Service rate per server: μ = 1.0

Run simulations of both. Compare:
- Average queue length
- Average wait time
- Probability a customer has to wait (for M/M/2, this is more complex)

How much better is the 2-server system?

---

**6. One queue vs. two separate queues**

Scenario: λ = 0.8 total, split equally between two baristas.

Compare:
- M/M/2: one queue feeding two servers (λ=0.8 per queue, μ=1.0 per server)
- Two independent M/M/1: each handles λ=0.4, μ=1.0

Which has lower average wait time? Why?

(This is the supermarket checkout dilemma: one line or multiple lines per register?)

---

**7. Non-exponential service times**

Modify the simulation to use deterministic service times instead of exponential:
- All customers take exactly 1 minute to serve

Keep λ = 0.8, μ = 1.0 (same average as before).

Compare average queue length to the exponential M/M/1 queue with the same λ and μ.

Which has longer waits? Why does variability matter?

---

**8. Bursty arrivals**

Instead of Poisson arrivals, use bursty arrivals:
- Most of the time, no arrivals
- But occasionally, 5 customers arrive together

Keep the same average arrival rate as M/M/1 (λ = 0.8).

Compare queue length and wait times to Poisson arrivals. Does burstiness affect queueing?

---

## Challenge Exercises

**9. Priority queue**

Implement a priority queue where:
- 20% of customers are high-priority
- 80% are low-priority
- High-priority customers go to the front of the line

Compare to a non-priority M/M/1 queue with the same λ and μ.

Measure:
- Average wait for high-priority customers
- Average wait for low-priority customers
- Overall average wait

What's the cost of prioritizing 20% of customers?

---

**10. Load-dependent service**

In some systems, service rate depends on queue length:
- If queue is short, server works fast
- If queue is long, server gets stressed and slows down (or rushes and makes errors)

Model: μ = μ₀ / (1 + αn) where n is queue length.

How does this feedback affect stability and waiting times?

---

**11. Customer impatience**

Customers don't wait forever. If the queue is too long, they balk (leave without joining).

Model: probability of joining = 1 / (1 + α × queue_length)

Vary α (patience):
- α = 0: customers always join
- Large α: customers leave if queue is long

How does impatience affect queue dynamics?

---

**12. M/M/c queue analysis**

Implement M/M/c for c = 1, 2, 3, 4, 5 servers.

For each, measure average wait time with λ = 0.8, μ = 1.0.

Plot average wait vs. number of servers. Is there a point of diminishing returns?

---

## Thought Experiments

**13. Capacity planning**

You're a manager. Demand is λ = 0.8 customers per minute. You can hire servers at cost C per server.

Each customer that waits > 5 minutes creates a dissatisfaction cost of $1.

How many servers should you hire? (There's a tradeoff between labor cost and customer satisfaction.)

---

**14. The supermarket paradox**

In the supermarket, you must choose:

**Option A**: One line feeding 3 registers
**Option B**: Three separate lines, one per register

Both have the same total service capacity. Which should you choose for customer satisfaction? Why?

(Hint: think about balancing.)

---

**15. Internet congestion**

A link can transmit packets at rate μ = 100 Mbps. Packets arrive at rate λ.

For λ = 50, 70, 90, 99 Mbps:
- Compute average queue length
- Compute average packet delay
- Compute buffer size needed (for a queue that holds 95% of packets without dropping)

What happens as λ → μ?

---

## Open-Ended Exploration

**Network of queues**

Model a two-stage queueing system:
- Stage 1: one server, serves customers
- Stage 2: one server, processes the output from Stage 1

This could model a manufacturing line: worker A assembles, worker B packages.

Vary the service rates and arrival rate. How does bottleneck location affect the overall system?

---

**Real data: call center**

If you can find or generate realistic call center data (inter-arrival times, service durations):

1. Estimate λ and μ
2. Compute theoretical queue statistics
3. Simulate an M/M/1 queue with those parameters
4. Compare to actual data

What does the model capture? What does it miss?

---

**Erlang B formula**

In a phone system with c lines and λ arrivals per unit time, the blocking probability (chance that a call is rejected) is given by the **Erlang B formula**.

Implement the Erlang B formula and explore:
- How many lines are needed to keep blocking probability below 1%?
- How does this compare to queueing (where customers wait instead of being blocked)?
