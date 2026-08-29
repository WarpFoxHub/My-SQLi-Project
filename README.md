# PortSwigger Lab Helper

A small tool for automating lab tasks from the PortSwigger Web Security Academy. It's being written as I progress through the course — the code evolves along with my skill level.

## Status
Early stage. Working code for specific labs, hardcoded in places. See commit history — I'll refactor as I cover new topics.

## What's already available
- SQL injection: login bypass via query commenting
- SQL injection: server response comparison (diff-based detection)

## Stack
Python, requests, BeautifulSoup

## Launch
The lab URL is passed as an argument (not hardcoded in the code) —
in PortSwigger, it's personal and temporary for each session.