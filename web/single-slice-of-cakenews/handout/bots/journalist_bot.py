from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import requests

JOURNALIST_EMAIL = '0xjeppe@cakenews.ctf'
JOURNALIST_PASSWORD = os.environ.get('JOURNALIST_PASSWORD')

CAKENEWS_BASE_URL = os.environ.get('CAKENEWS_BASE_URL', 'http://cakenews:5000')
CAKENEWS_API_URL = f'{CAKENEWS_BASE_URL}/api'
REPORT_ENDPOINT = f"{CAKENEWS_BASE_URL}/internal/next-report/journalist"

def get_access_token():
    try:
        res = requests.post(
            f"{CAKENEWS_API_URL}/login",
            json={'email': JOURNALIST_EMAIL, 'password': JOURNALIST_PASSWORD}
        )
        res.raise_for_status()
        return res.json().get('token')
    except requests.exceptions.RequestException as e:
        print(f"Error logging in as journalist: {e}")
        return None

def setup_browser(token):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(options=chrome_options)

    browser.get(f'{CAKENEWS_BASE_URL}/')

    inject_script = """
        localStorage.setItem('cakenewsAccessToken', arguments[0]);
        localStorage.setItem('cakenewsUserProfile', JSON.stringify({
            email: arguments[1],
            username: '0xjeppe',
            role: 'journalist'
        }));
    """
    browser.execute_script(inject_script, token, JOURNALIST_EMAIL)

    return browser
    
def visit_article(browser, article_id):
    print(f"Journalist bot visiting article: {article_id}")
    browser.get(f'{CAKENEWS_BASE_URL}/article/{article_id}')
    time.sleep(2)

def poll_for_reports():
    time.sleep(10)
    
    token = get_access_token()
    if not token:
        print("Could not get access token. Retrying in 10 seconds.")
        time.sleep(10)
        poll_for_reports()
        return

    browser = setup_browser(token)
    try:
        while True:
            try:
                res = requests.get(REPORT_ENDPOINT, timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    article_id = data.get('article_id')
                    if article_id:
                        visit_article(browser, article_id)
            except requests.exceptions.RequestException as e:
                print("Error polling reports:", e)
            time.sleep(10)
    finally:
        browser.quit()

if __name__ == '__main__':
    poll_for_reports()
