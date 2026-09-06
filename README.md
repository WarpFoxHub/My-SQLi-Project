# PortSwigger Lab Helper

A small tool for automating lab tasks from the PortSwigger Web Security Academy. It's being written as I progress through the course — the code evolves along with my skill level.

## Status
Blind extraction, DBMS fingerprinting, and UNION-based column recon refactored into classes. Table/column name enumeration via information_schema still manual (diff-based output) — next step is automating that.

## What's already available
- SQL injection: login bypass via query commenting
- SQL injection: server response comparison (diff-based detection)
- SQL injection: blind extraction — boolean-based, error-based, and time-based, unified in one class (`BlindInj`) with per-DBMS payload variants (Oracle, MySQL, Microsoft SQL, PostgreSQL)
- SQL injection: DBMS fingerprinting via time-based payloads, unified in one class (`DbmsVerifyTimeBased`) — tries URL param injection first, falls back to cookie-based
- SQL injection: error-based extraction via type casting
- SQL injection: UNION-based recon — column count and type detection (`UnionTableRecon`), plus automated table and column name enumeration via `InformationSchema` (diff-based, per-DBMS UNION payloads, returns results as a list instead of manual reading)

## Status
Blind extraction, DBMS fingerprinting, UNION-based column recon, and information_schema table/column enumeration all refactored into classes. `cast_inj` still a hardcoded, lab-specific script — next step is generalizing it the same way.

## Next up
Generalizing `cast_inj` into a reusable class (parameterized table/column, per-DBMS payload variants) instead of a hardcoded username/password lookup.
## Launch
The lab URL is passed as an argument (not hardcoded in the code) —
in PortSwigger, it's personal and temporary for each session.