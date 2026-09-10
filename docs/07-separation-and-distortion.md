# 07 — Separation budgets under distortion

How many samples does it take to tell two hypotheses apart, and what happens when the observations are systematically distorted? Both have exact answers here.

## 1. A deterministic separation certificate

Fix two hypothesis classes whose laws are separated by an exact distance $D$, and a fixed acquisition budget of $n$ samples with grid denominator $m$. For a target significance $\alpha = 1/20$ (four tails of $1/80$ each), a **sufficient** certificate for distinguishing them is

$$\text{slack} = D - \frac{2}{m} > 0
\quad\text{and}\quad
n \cdot \text{slack}^2 \ge 10 .$$

With $n = 65{,}536$ and $m = 256$, this reads

$$\text{slack} = D - \frac{2}{256}, \qquad \text{score} = 65{,}536 \cdot \text{slack}^2, \qquad \text{sufficient} \iff \text{slack} > 0 \text{ and } \text{score} \ge 10 .$$

When the certificate holds, the procedure reports the correct hypothesis as a **singleton** with probability $\ge 19/20$, and the probability that a reported singleton is wrong is $\le 1/20$.

## 2. Distortion erodes the margin — at rate two

Suppose the *actual* observed law is a distortion of the ideal law, bounded by $\|r - q_{\text{true}}\|_\infty \le e$. The **distorted separation** is exactly

$$D_e = \max(D - 2e,\; 0) .$$

The factor of two is the headline: a uniform distortion bound $e$ consumes the separation margin $D$ at **twice** its own size. Intuitively, two hypotheses can each drift toward the other by $e$, closing $2e$ of the gap.

## 3. The exact census

With $n = 65{,}536$, $m = 256$, and the ideal class distances $D$ below, the certificate resolves as:

| Case | error $e$ | $D_e$ | slack | score | Certificate |
|---|---:|---:|---:|---:|---|
| uniform / zero | $0$ | $3/64$ | $5/128$ | $100$ | yes |
| uniform / quarter | $3/256$ | $3/128$ | $1/64$ | $16$ | yes |
| uniform / contact | $3/128$ | $0$ | $-1/128$ | $4$ | no (collision) |
| half / zero | $0$ | $1/48$ | $5/384$ | $100/9$ | yes |
| half / quarter | $1/192$ | $1/96$ | $1/384$ | $4/9$ | no (budget fails) |
| half / contact | $1/96$ | $0$ | $-1/128$ | $4$ | no (collision) |
| one / zero | $0$ | $0$ | $-1/128$ | $4$ | no (inherited collision) |
| two / zero | $0$ | $0$ | $-1/128$ | $4$ | no (inherited collision) |

Here $e$ runs over $\{0, D/4, D/2\}$, and the "one"/"two" rows are broad classes with $D = 0$ (genuine observationally-identical classes, not a budget failure).

Three **different** failure reasons appear, and they must not be conflated:

1. **Collision** ($D_e = 0$): the two classes genuinely share an actual record law. *No* budget can separate them. This is the factorization-obstruction kind from [03](03-ambiguity-taxonomy.md).
2. **Budget failure** (slack $> 0$ but score $< 10$): the classes are separated, but the fixed budget is too small to certify it with the required confidence.
3. **Grid failure** (slack $\le 0$): the separation is smaller than the grid resolution $2/m$.

## 4. What this means in practice

- **Sample complexity is exact here, not asymptotic.** The $n \cdot \text{slack}^2 \ge 10$ test is a closed-form, deterministic decision about whether a fixed budget suffices — directly usable for "how much data do I need to tell two candidate models apart?"
- **Shift eats distinguishability at rate two.** Under enough label noise or distribution shift, two models that are distinguishable in-distribution become *literally* indistinguishable. The margin between two hypotheses is twice as sensitive to uniform distortion as either hypothesis is alone.
- **A failed budget is not an impossibility.** Only the collision rows ($D_e = 0$) are genuine obstructions. The others are "insufficient resources," which is a different, fixable thing. Keeping these apart is the whole point of the taxonomy.

## 5. The honest boundary

The distortion bound $e$ is an **input**, not an output — this calculus does not tell you how to *measure* $e$; it tells you what happens *given* a justified bound on it. Estimating a valid $e$ from production records is a separate, harder problem, and must not be silently assumed away.

---

**Back to** [README](../README.md).
