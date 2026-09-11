#!/usr/bin/env python3
"""Runnable walkthrough of every result in finite-observation-calculus.

Run with:  python3 demo.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from fractions import Fraction

from foc import linalg as la
from foc import instruments as ins
from foc import schedule
from foc import summaries
from foc import forgetting
from foc import geometry
from foc import confidence
from foc import ambiguity
from foc import certificate
from foc import crossdomain
from foc import modelrun
from foc import train
from foc import transformer
from foc import truncate
from foc import regime
from foc import router
from foc import internal
from foc import corrective


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

    # 11. Empirical probe-audit protocol (finite-sample certification)
    hdr("11. Empirical probe-audit protocol (margin + sample budget)")
    for margin in (Fraction(2), Fraction(5)):
        print(f"  margin t={margin}, n=100, threshold K=10:")
        for r in ambiguity.certify_audit(margin, 100, 10):
            print(f"    {r['feature']:22} {r['model']:11} sep {r['sep_declared']}/{r['sep_full']}"
                  f"  {r['verdict']:14} certified={r['certified']} min_n={r['min_samples']}")
    print()

    # 12. Machine-checkable certificates (build / verify / tamper)
    hdr("12. Machine-checkable certificates")
    P0 = la.mat([[1, 0], [0, 0]])
    P1 = la.mat([[0, 0], [0, 1]])
    h = Fraction(1, 2)
    Qp = la.mat([[h, h], [h, h]])
    Qm = la.mat([[h, -h], [-h, h]])
    cert = certificate.build_certificate(ambiguity.X, [P0, P1], [P0, P1, Qp, Qm])
    print("  label:", cert["label"], "| witness:", cert["witness"])
    print("  verify:", certificate.verify_certificate(cert))
    tampered = dict(cert)
    tampered["label"] = "separated"
    print("  tampered label -> verify:", certificate.verify_certificate(tampered))
    print("  wire round-trip verify:", certificate.verify_wire(certificate.to_wire(cert)))
    print()

    # 13. Cross-domain exact-witness zoo
    hdr("13. Cross-domain exact-witness zoo")
    c = crossdomain.causal_observational_equivalence()
    print("  causal: same observational law?", c["same_observational_law"],
          "| P(Z|do X=1): chain", c["chain_P_Z_given_do_X1"], "fork", c["fork_P_Z_given_do_X1"])
    cf = crossdomain.conformal_marginal_vs_conditional()
    print("  conformal: marginal", cf["marginal_coverage"], "(ok?", cf["marginal_ok"],
          ") | conditional stratum-1", cf["conditional_coverage_stratum1"])
    pid = crossdomain.partial_identification()
    print("  partial ID: E[Y] in", pid["identified_set"],
          "| inside ambiguous?", pid["inside_is_ambiguous"],
          "| outside infeasible?", pid["outside_is_infeasible"])
    print()

    # 14. A controlled model run (exact)
    hdr("14. A controlled model run of the probe audit (exact)")
    print(f"  {'feature':14} {'sep loc/joint':14} {'verdict':16} ground truth")
    for r in modelrun.model_run():
        print(f"  {r['feature']:14} {str(r['sep_local']) + '/' + str(r['sep_joint']):14}"
              f" {r['verdict']:16} {r['ground_truth']} (correct={r['correct']})")
    print()

    # 15. A trained model in pure rationals
    hdr("15. A trained model in pure rationals (exact)")
    for task in ("linear", "quadratic"):
        res = train.trained_audit(task)
        tr = res["trained"]
        print(f"  task={task}: LS (a,c)={tr['ls']}  loss={tr['loss_ls']}")
        for row in res["rows"]:
            print(f"    {row['feature']:16} sep {row['sep_local']}/{row['sep_joint']}"
                  f"  -> {row['verdict']:16} (correct={row['correct']})")
    print()

    # 16. A genuine transformer, trained without floats
    hdr("16. A genuine transformer, trained without floats")
    hist = transformer.train_exact(transformer.TOY_DATA, steps=2)
    print("  squared-normalized attention + ReLU MLP + residual; exact rational gradients")
    for i, (ws, l) in enumerate(hist):
        print(f"    step {i}: loss={float(l):.6g}  max denom bits={max(w.denominator.bit_length() for w in ws)}")
    print("  weights all rational?", all(isinstance(w, Fraction) for w in hist[-1][0]))
    print()

    # 17. Certified precision: truncation bounded by the margin
    hdr("17. Certified precision: truncation bounded by the margin")
    ct = truncate.certified_truncation(steps=2)
    print(f"  exact weights: {ct['exact_bits']} denom bits;"
          f"  separation D={float(ct['separation']):.4f};  margin t={float(ct['margin']):.4f}")
    print(f"  {'grid':>5} {'bits':>5} {'separation':>12} {'rate-two':>9}  verdict")
    for r in ct["rows"]:
        if r["degenerate"]:
            print(f"  {r['grid']:>5} {r['bits']:>5} {'degenerate':>12} {'-':>9}  no")
        else:
            print(f"  {r['grid']:>5} {r['bits']:>5} {float(r['separation']):>12.4f}"
                  f" {str(r['rate_two_ok']):>9}  {'yes' if r['verdict_ok'] else 'no'}")
    print()

    # 18. Regime composition: transformers as certified nodes
    hdr("18. Regime composition: per-regime precision + routing")
    rl = regime.routing_laws()
    print("  routing on the same experts: hard (sum of maps) vs soft (recombination)")
    print("    hard =", fmt_matrix(rl["hard"]))
    print("    soft =", fmt_matrix(rl["soft"]), "differ?", rl["differ"])
    rp = regime.regime_precision([Fraction(1, 4), Fraction(3, 10), Fraction(2, 5), Fraction(12, 25)])
    print("  per-regime precision (coarsest certified grid):")
    for row in rp["per_regime"]:
        print(f"    margin={float(row['margin']):.3f}  grid={row['grid']}  bits={row['bits']}")
    print(f"  modular bits={rp['modular_bits']}  monolithic bits={rp['monolithic_bits']}"
          f"  saving={rp['saving']}")
    print()

    # 19. A certified router (and routing theorems)
    hdr("19. A certified router (and routing theorems)")
    rr = router.router_report()
    print("  certified routing (margin t=1/2):")
    for r in rr["routes"]:
        print(f"    x={r['x']}  route={r['route']}  margin={r['margin']}  certified={r['certified']}")
    print("  router precision:", rr["router_precision"])
    print("  routing type matters (hard != soft)?")
    print("    orthogonal experts, classical input :", rr["type_orthogonal_classical"], "(immaterial)")
    print("    orthogonal experts, coherent input  :", rr["type_orthogonal_coherent"])
    print("    overlapping experts, classical input:", rr["type_overlapping_classical"])
    rrep = router.replacement_report()
    print("  replacement criterion (hard for soft):")
    print("    counting downstream (reads I) -> valid :", rrep["counts_valid"])
    print("    Z-reading downstream          -> valid :", rrep["reads_Z_valid"])
    print("    colliding witness (|+>,|->)            :", rrep["witness"])
    print()

    # 20. Internal certification: self-consistency and closed growth
    hdr("20. Internal certification: self-consistency + closed growth")
    ir = internal.internal_report()
    print("  self-consistency (fixed point of own replacement criterion):")
    print("    stable node   (orthogonal experts, classical):", ir["stable"])
    print("    unstable node (overlapping experts, coherent):", ir["unstable"])
    print("    instability witness (|+>,|->)                 :", ir["witness"])
    print("  closed growth (invisible sector shrinks as nodes compose):")
    print("    local node:", ir["annihilator_local_node"],
          " pairs node:", ir["annihilator_pairs_node"],
          " composed:", ir["annihilator_composed"])
    print()

    # 21. The corrective loop (localizing an external failure)
    hdr("21. The corrective loop: localizing an external failure")
    cvr = corrective.corrective_report()
    print("  annihilator filter (which node can see the failing feature):")
    print("    failing 2-body Z(x)Z ->", cvr["localize_2body"])
    print("    failing 1-body Z(x)I ->", cvr["localize_1body"])
    print("  edge blame (what the failing downstream reads):")
    print("    reads Z ->", cvr["blame_Z"], " reads I ->", cvr["blame_I"])
    c = cvr["correction"]
    print(f"  correction re-certified: invisible dim {c['annihilator_before']} -> {c['annihilator_after']}"
          f"  refinement_safe={c['refinement_safe']}  verdict={c['verdict_holds']}  accepted={c['accepted']}")
    print()


if __name__ == "__main__":
    main()
