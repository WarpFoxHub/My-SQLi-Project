# PortSwigger Lab Helper

A small tool for automating lab tasks from the PortSwigger Web Security Academy. It's being written as I progress through the course — the code evolves along with my skill level.

## Status
All core SQL injection techniques (blind extraction, DBMS fingerprinting, UNION-based recon, cast-based extraction) now refactored into reusable classes. No more single-lab hardcoded scripts.

## What's already available
- SQL injection: login bypass via query commenting
- SQL injection: server response comparison (diff-based detection)
- SQL injection: blind extraction — boolean-based, error-based, and time-based, unified in one class (`BlindInj`) with per-DBMS payload variants (Oracle, MySQL, Microsoft SQL, PostgreSQL)
- SQL injection: DBMS fingerprinting via time-based payloads, unified in one class (`DbmsVerifyTimeBased`) — tries URL param injection first, falls back to cookie-based
- SQL injection: error-based extraction via type casting, unified in one class (`CastInj`) with per-DBMS payload and regex-extraction variants (Oracle, MySQL, Microsoft SQL, PostgreSQL)
- SQL injection: UNION-based recon — column count and type detection (`UnionTableRecon`), plus automated table and column name enumeration via `InformationSchema`

## Launch
The lab URL is passed as an argument (not hardcoded in the code) —
in PortSwigger, it's personal and temporary for each session.
Depending on the topic you are covering, create an instance of the required class, pass the laboratory assignment arguments to it, and run the script.