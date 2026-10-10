# Requirement matrix

| Review requirement | Implementation | Proof |
|---|---|---|
| Frozen authoritative input | Brief fetched, digested, and rechecked | `test_specification_is_frozen_and_rechecked` |
| Consensus-bound semantics | Exact ordered penalty vector and artifact digest | `test_every_semantic_driver_is_consensus_bound` |
| Deterministic state transition | Contract-only Pareto dominance | `test_pareto_rule_is_deterministic_and_not_total_score` |
| Replay safety | Per-assay artifact digest guard | `test_duplicate_digest_cannot_mutate_frontier` + live run |
| Complete lifecycle | Open, three insertions, inspect, seal | Browser demo + live evidence |
| Public usable frontend | Wallet writes, finalized receipts, live reads | Surface tests + browser QA |
