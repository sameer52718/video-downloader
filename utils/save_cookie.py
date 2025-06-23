import time

def save_cookies_to_file(cookies, filename="cookies.txt"):
    with open(filename, 'w') as f:
        f.write("# Netscape HTTP Cookie File\n")
        for cookie in cookies:
            domain = cookie['domain']
            flag = 'TRUE' if domain.startswith('.') else 'FALSE'
            path = cookie['path']
            secure = 'TRUE' if cookie['secure'] else 'FALSE'
            expiry = str(cookie.get('expiry', int(time.time()) + 3600))
            name = cookie['name']
            value = cookie['value']
            f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n")
