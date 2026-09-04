# PortSwigger Lab Helper

A small tool for automating lab tasks from the PortSwigger Web Security Academy. It's being written as I progress through the course — the code evolves along with my skill level.

## Status
Working through the SQL injection module. Core logic (blind extraction) refactored into a class; other functions still being cleaned up per lab. See commit history for progress.

## What's already available
- SQL injection: login bypass via query commenting
- SQL injection: server response comparison (diff-based detection)
- SQL injection: blind extraction — boolean-based, error-based, and time-based, unified in one class (`blind_inj`) with per-DBMS payload variants (Oracle, MySQL, Microsoft SQL, PostgreSQL)
- SQL injection: DBMS fingerprinting via time-based payloads (URL param and cookie-based)
- SQL injection: error-based extraction via type casting
- SQL injection: UNION-based recon — column count discovery, column type detection, `information_schema` enumeration of tables and columns

## Stack
Python, requests, BeautifulSoup, difflib, re, urllib.parse

## Launch
The lab URL is passed as an argument (not hardcoded in the code) —
in PortSwigger, it's personal and temporary for each session.