# Pareto Cabinet

Procurement shortlists often hide trade-offs inside one invented total score. Pareto Cabinet keeps the trade-offs visible. Validators inspect a public artifact against a frozen public brief and return one ordered binary penalty per constraint. The contract then computes dominance without an LLM: an artifact enters the frontier when no existing specimen is at least as good on every constraint and better on one.

## What is novel here

This is not ranking, voting, or “AI chooses the winner.” Several incompatible candidates may remain in the cabinet because each preserves a different advantage. Semantic inspection is consensus-bound; frontier mutation is deterministic.

The brief digest is frozen when the assay opens and rechecked during every insertion. Artifact bytes receive their own digest and cannot be submitted again from another wallet. A newly inserted specimen can deterministically eclipse earlier frontier members, but the historic candidate record remains queryable.

## Cabinet procedure

1. `open_assay` fetches and freezes a public HTTPS brief plus two to five constraints.
2. `insert_candidate` refetches the brief and artifact, obtains the exact penalty vector, and updates the frontier.
3. `get_candidate` preserves provenance, digest, vector, and current status.
4. `seal_assay` closes any assay with at least three evaluated specimens.

## Evidence drawers

- `contracts/contract.py` — mechanism and state invariants
- `fixtures/` — public, auditable fixture texts
- `tests/` — dominance, integrity, and UI checks
- `scripts/` — deployment, live exercise, source verification
- `evidence/` — finalized transaction and browser records

Fixture artifacts are operator-controlled demonstrations. They are disclosed as such and are not claimed to be independent vendors or external evaluations.
