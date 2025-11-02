# Single Slice Of CakeNews

This XSS-challenge is based on an actual bug I found and reported on a major Danish website. It showcases how session-management via localStorage can be dangerous if 1) user-input is not sanitized and validated and 2) if there is no Content-Security Policy (CSP) headers set. This allows an attacker to leak a victim's access-token and hijack their session.

It also showcases how XSS can be utilized for phishing-attacks - and how this can be leveraged to exploit Single Sign On-systems, where stealing credentials for one application opens up access to other applications using the same SSO-platform.

Lastly it explores how to bypass Cross-Origin Resource Sharing (CORS) when exfiltrating data through injected phishing.
