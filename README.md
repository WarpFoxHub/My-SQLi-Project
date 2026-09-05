# PortSwigger Lab Helper

A small tool for automating lab tasks from the PortSwigger Web Security Academy. It's being written as I progress through the course — the code evolves along with my skill level.

## Status
Blind extraction, DBMS fingerprinting, and UNION-based column recon refactored into classes. Table/column name enumeration via information_schema still manual (diff-based output) — next step is automating that.
## What's already available
- SQL injection: login bypass via query commenting
- SQL injection: server response comparison (diff-based detection)
- SQL injection: blind extraction — boolean-based, error-based, and time-based, unified in one class (`blind_inj`) with per-DBMS payload variants (Oracle, MySQL, Microsoft SQL, PostgreSQL)
- SQL injection: DBMS fingerprinting via time-based payloads, unified in one class (`dbms_verify_time_based`) — tries URL param injection first, falls back to cookie-based
- SQL injection: error-based extraction via type casting
- SQL injection: UNION-based recon — column count and type detection (`union_table_recon`), `information_schema` enumeration of tables and columns

## Stack
Python, requests, BeautifulSoup, difflib, re, string, urllib.parse

## Next up
Automating table and column name enumeration — parsing information_schema results into structured output instead of reading a diff manually.

## Launch
The lab URL is passed as an argument (not hardcoded in the code) —
in PortSwigger, it's personal and temporary for each session.