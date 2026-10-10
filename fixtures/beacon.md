# Beacon reader

Annotations are stored locally after every change and restored on restart. All primary controls have a keyboard path and meaningful accessible labels. Reading content requires a live network request on every opening.

## Constraint declaration

- OFFLINE: FAIL — opening reading content requires a live request.
- ACCESS: PASS — primary controls are keyboard reachable and explicitly labelled.
- RECOVERY: PASS — annotations are persisted locally and restored after restart.
