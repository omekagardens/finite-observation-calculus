# 14 — A machine-checkable certificate toolkit

`docs/08` §4 gives the classification and `docs/11` §5 says the exact label is
*structurally* decidable. This note turns that into an artifact: each verdict
carries an **exact certificate** that a verifier re-checks *without re-running the
analysis*.

## 1. The certificate

A certificate is a record:

- `label` $\in$ {separated, channel-limited, law-surviving};
- `delta` — the feature difference;
- `accessible`, `completed` — spanning sets of the accessible ($E$) and completed
  ($E^\*$) effects;
- `witness` — for the resolvable labels, an effect with
  $\operatorname{Tr}(\Delta E) \neq 0$.

## 2. What each label certifies

| label | witness | verifier checks |
|---|---|---|
| **separated** | $E \in$ `accessible` | $\operatorname{Tr}(\Delta E) \neq 0$ |
| **channel-limited** | $E \in$ `completed` | $\Delta \perp$ `accessible` **and** $\operatorname{Tr}(\Delta E) \neq 0$ |
| **law-surviving** | none | $\Delta \perp$ `completed` |

plus the nesting consistency $A_E \supseteq A_{E^\*}$ (invisible to the completed
span ⇒ invisible to the accessible span). Verification is exact (`Fraction`) and
costs $O(\#\text{effects})$; it needs only the certificate.

## 3. Wire form

`to_wire` / `from_wire` / `verify_wire` encode the certificate with rationals as
strings, JSON-serializable — the upstream QR-01 wire style. A claim can be shipped
as JSON and independently verified by anyone.

## 4. What the certificate's shape shows

The `law-surviving` certificate is a **universal** ("every accessible effect is
invisible"); the `separated` / `channel-limited` certificates are **existential**
("one witness experiment differs"). This is exactly the certifiable-content
structure of `docs/11` §3, now baked into the artifact: *a witness proves a
difference; only the full algebra proves an identity.*

## 5. Status

Engineering, not new mathematics — the contribution is making the exact witnesses
**machine-checkable and portable** (QR-01 style). Implemented in
`foc.certificate` (`build_certificate`, `verify_certificate`, `to_wire`,
`from_wire`, `verify_wire`) and exercised in demo section 12.

**Back to** [README](../README.md).
