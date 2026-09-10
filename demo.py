#!/usr/bin/env python3
"""Runnable walkthrough of every result in finite-observation-calculus.

Run with:  python3 demo.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from fractions import Fraction

from foc import instruments as ins
from foc import schedule
from foc import summaries
from foc import forgetting
from foc import geometry
from foc import confidence
from foc import ambiguity


def fmt_matrix(m):
    if m is None:
        return "zero-probability"
    return "/".join(",".join(str(x) for x in row) for row in m)


def fmt_poly(p):
    return f"1 + ({p['uv']})uv + ({p['u2v2']})u2v2"


def hdr(t):
    print("\n" + "=" * 68)
    print(t)
    print("=" * 68)


def main():
    # 1. Behavioral vs mechanistic equivalence
    hdr("1. Behavioral vs. mechanistic equivalence (Z/X)")
    p_zx, p_xz = schedule.zx_counterexample(ins.rho_0())
    print("record (Z, X)     Z then X     X then Z")
    for key in [("0", "+"), ("0", "-"), ("1", "+"), ("1", "-")]:
        print(f"  {str(key):12} {str(p_zx.get(key, 0)):>10} {str(p_xz.get(key, 0)):>10}")
    z, x = ins.z_instrument(), ins.x_instrument()
    print("record-discarded channels equal?",
          schedule.record_discarded_equal(z, x, ins.rho_0()))
    print("recorded maps equal?",
          schedule.recorded_equal(z, x, ins.rho_0()))

    # 2. Two kinds of ambiguity
    hdr("2. The two-kinds-of-ambiguity taxonomy")
    t1 = geometry.type1_obstruction()
    print("Kind 1 (factorization obstruction):")
    print("  flat   point law:", fmt_poly(t1["flat_point_poly"]))
    print("  conf   point law:", fmt_poly(t1["conf_point_poly"]))
    print("  identical complete point law?", t1["same_point_law"])
    print("  shared q1 =", t1["q1"], " shared q2 =", t1["q2"])
    print("  targets flat/conf =", t1["targets"][0], "vs", t1["targets"][1],
          " gap =", t1["target_gap"])
    t2 = geometry.type2_obstruction()
    print("Kind 2 (channel-limited):")
    print("  delta_flat =", t2["delta_flat"], " delta_conf =", t2["delta_conf"])
    print("  same single-mark q1?", t2["q1_equal"], " q1 =", t2["q1"])
    print("  point laws differ?", t2["point_law_differs"])
    print("  q2_flat =", t2["q2_flat"], " q2_conf =", t2["q2_conf"],
          " gap =", t2["q2_gap"], " split by richer channel?", t2["q2_splits"])

    # 3. Minimal summaries
    hdr("3. Question-relative minimal summaries (Z then X, rho = I/2)")
    for state, hists in summaries.zthenx_classes(ins.rho_mixed()):
        print(f"  residual state {fmt_matrix(state)}  <-  {sorted(hists)}")
    w0p, w1p = summaries.summary_loses_weights()
    print("summary 's=+' loses history weights:", w0p, "vs", w1p)

    # 4. Forgetting is not recombination
    hdr("4. Forgetting is not recombination (coarse-graining vs coherent sum)")
    zex = forgetting.z_example()
    print("  sum of branches (forget)      ->", fmt_matrix(zex["forgotten"]))
    print("  sum of amplitudes (recombine) ->", fmt_matrix(zex["recombined"]))
    print("  differ?", zex["differ"], "| recombined == identity?", zex["recombined_is_identity"])
    w = forgetting.impossibility_witness()
    print("  coarse merges |+> and |-> ->", fmt_matrix(w["coarse_state"]),
          "(equal?", w["coarse_merges"], ")")
    print("  fine feedback: |+> ->", fmt_matrix(w["fine_plus"]))
    print("                 |-> ->", fmt_matrix(w["fine_minus"]))
    print("  no coarse-only replacement exists?", w["no_replacement"])

    # 5. Marginal vs conditional confidence
    hdr("5. Marginal vs. conditional confidence")
    m = confidence.marginal_vs_conditional()
    print(f"  n={m['n']}, p={m['p']}, singleton guess={m['singleton_guess']}")
    print(f"  P(report singleton) = {m['prob_singleton']}")
    print(f"  unconditional coverage = {m['unconditional_coverage']} "
          f"(>= 19/20? {m['unconditional_coverage_ok']})")
    print(f"  conditional error given singleton = {m['conditional_error_given_singleton']}")
    low, high = confidence.clopper_pearson(2, 4, Fraction(1, 20))
    print(f"  Clopper-Pearson 95% interval (k=2, n=4): [{low}, {high}]")

    # 6. Separation budget under distortion
    hdr("6. Separation budgets under distortion")
    print(f"{'case':18} {'D':>8} {'e':>10} {'D_e':>8} {'slack':>10} {'score':>8}  cert")
    for r in confidence.bv_table():
        print(f"{r['name']:18} {str(r['D']):>8} {str(r['e']):>10} {str(r['D_e']):>8} "
              f"{str(r['slack']):>10} {str(r['score']):>8}  {'yes' if r['sufficient'] else 'no'}")
    print()

    # 7. The general dichotomy: annihilator classification and locality
    hdr("7. The general dichotomy (annihilator / locality)")
    qc = ambiguity.qubit_coherence()
    print("  qubit coherence X:  dim invisible (Z only) =", qc["dim_accessible"],
          "-> (Z, X) =", qc["dim_completed"])
    print("  classify X:  open rules ->", qc["class_open"],
          "| X forbidden ->", qc["class_closed"])
    loc = ambiguity.two_qubit_locality()
    print("  two qubits:  local one-body access leaves dim", loc["dim_local"],
          "invisible (= two-body correlations); joint access ->", loc["dim_joint"])
    print("  distortion e=d/2 collapses separation d:",
          ambiguity.collapses(Fraction(1, 4), Fraction(1, 8)))
    print()

    # 8. Probe audit (LLM-style)
    hdr("8. Probe audit (LLM-style): which features are readable?")
    print(f"  {'feature':24} {'model':12} {'verdict':16} action")
    for r in ambiguity.llm_probe_audit():
        print(f"  {r['feature']:24} {r['model']:12} {r['verdict']:16} {r['action']}")
    print()

    # 9. Symmetry of an ambiguity: continuous / discrete / accidental
    hdr("9. Is the ambiguity a symmetry? (linear symmetry algebra a(L))")
    print(f"  {'law map L':26} {'dim a(L)':>8}  kind")
    for name, dim, kind in ambiguity.symmetry_examples():
        print(f"  {name:26} {dim:>8}  {kind}")
    print()

    # 10. Nonlinear symmetry: declared generators and the rank-one theorem
    hdr("10. Nonlinear symmetry (declared generators)")
    growth = ambiguity.symmetry_growth()
    print("  L=x^2+y^2: degree-filtered polynomial symmetry dim (sections of ker DL)")
    print("   d   :", " ".join(f"{d:>3}" for d, _ in growth))
    print("   dim :", " ".join(f"{v:>3}" for _, v in growth), " = d(d+1)/2 (grows -> ill-posed)")
    grid = [(Fraction(i), Fraction(j)) for i in range(6) for j in range(6)]
    jac3 = lambda t: [[3 * t[0] ** 2, 3 * t[1] ** 2]]
    print("  L=x^3+y^3: dim a^(1) =", ambiguity.polynomial_symmetry_dim(jac3, 1, grid),
          " dim a^(2) =", ambiguity.polynomial_symmetry_dim(jac3, 2, grid),
          "(no linear; quadratic symmetry)")
    print()


if __name__ == "__main__":
    main()
