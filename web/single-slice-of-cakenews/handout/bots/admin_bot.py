from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import requests

ADMIN_EMAIL = 'admin@brunnerne.ctf'
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

CAKENEWS_BASE_URL = os.environ.get('CAKENEWS_BASE_URL', 'http://cakenews:5000')
CAKENEWS_API_URL = f'{CAKENEWS_BASE_URL}/api'
REPORT_ENDPOINT = f"{CAKENEWS_BASE_URL}/internal/next-report/admin"

def get_access_token():
    try:
        res = requests.post(
            f"{CAKENEWS_API_URL}/login",
            json={'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD}
        )
        res.raise_for_status()
        return res.json().get('token')
    except requests.exceptions.RequestException as e:
        print(f"Error logging in as admin: {e}")
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
            username: 'BrunnerneAdmin',
            role: 'admin'
        }));
    """
    browser.execute_script(inject_script, token, ADMIN_EMAIL)

    return browser

def login(browser):
    script = """
    (function(email, pwd){
        try{
            const hasToken = !!localStorage.getItem('cakenewsAccessToken');
            const hasProfile = !!localStorage.getItem('cakenewsUserProfile');
            if(hasToken || hasProfile){
                return false;
            }
        }catch(e){/* ignore and continue */}

        const modal = document.querySelector('.login-modal');
        if(!modal) return false;
        const form = modal.querySelector('form');
        let endpoint = window.location.href;
        if(form){
            endpoint = form.getAttribute('action') || endpoint;
        }
        fetch(endpoint, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({email: email, password: pwd})});
        return true;
    })(arguments[0], arguments[1]);
    """
    try:
        return browser.execute_script(script, ADMIN_EMAIL, ADMIN_PASSWORD)
    except Exception:
        return False

def visit_article(browser, article_id):
    browser.get(f'{CAKENEWS_BASE_URL}/article/{article_id}')
    time.sleep(2)
    login(browser)

def poll_for_reports():
    time.sleep(10)
    token = get_access_token()
    if not token:
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
