import requests
import pickle
from bs4 import BeautifulSoup
from datetime import datetime

INITIAL_LOGIN_COOKIE = ""
COOKIE_PATH = ""
AUTHENTICITY_TOKEN = ""
CLIENT_ID = ""
EMAIL = ""
PASSWORD = ""

def get_authenticity_token():
    r = requests.get("https://id.jobcan.jp/users/sign_in?app_key=atd")
    soup = BeautifulSoup(r.text, "html.parser")
    element = soup.find("input", {"name": "authenticity_token"})
    return element.get("value")

def info():
    session = requests.Session()
    with open(COOKIE_PATH, "rb") as f:
        session.cookies.update(pickle.load(f))
    r = session.get("https://ssl.jobcan.jp/employee/")
    soup = BeautifulSoup(r.text, "html.parser")
    element = soup.find("input", {"name": "token"})
    print(element)
    return element.get("value")

def work(status, token):
    adit_item = "DEF" if status == "start" else "work_end"
    
    session = requests.Session()
    with open(COOKIE_PATH, "rb") as f:
        session.cookies.update(pickle.load(f))
    
    params = {
        "is_yakin": 0,
        "adit_item": adit_item,
        "notice": "",
        "token": token,
        "adit_group_id": 2,
        "_": ""
    }

    r = session.post("https://ssl.jobcan.jp/employee/index/adit", data=params)
    print(r.text)

def login():
    session = requests.session()
    params = {
        "utf8": "&#x2713;",
        "authenticity_token": AUTHENTICITY_TOKEN,
        "user[email]": EMAIL,
        "user[password]": PASSWORD,
        "user[client_code]": "",
        "app_key": "atd",
        "redirect_uri": "https://ssl.jobcan.jp/jbcoauth/callback",
        "commit": "\u30ED\u30B0\u30A4\u30F3",
    }
    r = session.post("https://id.jobcan.jp/users/sign_in", data=params, headers={
        # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "cookie": INITIAL_LOGIN_COOKIE
    })
    print("Login", r.status_code)

    with open("cookie", "wb") as f:
        pickle.dump(session.cookies, f)

if __name__ == "__main__":
    # get_authenticity_token()
    login()
    token = info()
    print(token)

    hour = datetime.now().hour
    if 8 <= hour <= 10:
        work("start", token)
    else:
        work("end", token)
