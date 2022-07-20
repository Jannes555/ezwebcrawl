import os
import requests


def download_page_with_session(url, session_url):
    session = requests.Session()
    # HEAD requests ask for *just* the headers, which is all you need to grab the session cookie
    session.head(session_url)
    sessionid = session.cookies.get("sessionid")

    url = f"{url}&sessionid={sessionid}"

    response = session.get(
        url=url,
        headers={
            'Referer': session_url
        }
    )
    return response.text

async def show_proxies_helper(proxies):
    """Find and show 10 working HTTP(S) proxies."""
    while True:
        proxy = await proxies.get()
        if proxy is None:
            break
        print('Found proxy: %s' % proxy)


async def save_proxies_helper(proxies, filepath):
    """Save proxies to a file."""
    with open(filepath, 'w') as f:
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            proto = 'https' if 'HTTPS' in proxy.types else 'http'
            row = '%s://%s:%d\n' % (proto, proxy.host, proxy.port)
            f.write(row)


def find_proxies(count: int, filepath: str, types=['HTTP', 'HTTPS']):
    """Creates file like this:\r\n
    http://35.230.142.201:8080\r\n
    http://5.161.105.105:80\r\n
    ...
    """
    with open(filepath, 'w') as f:
        f.write("""http://35.230.142.201:8080
http://5.161.105.105:80
http://46.53.191.60:3128
http://157.100.12.138:999
http://14.140.131.82:3128
http://144.202.61.154:8888
http://171.244.170.205:8080
http://121.156.109.108:8080
http://123.56.175.31:3128
http://8.219.97.248:80""")
    return # Temp hardcoded proxies until I've added an automated way

def load_proxies(filepath):
    proxies = []
    with open(filepath, mode='r', encoding='utf-8') as f:
        for line in f:
            proxies.append(line)
    return proxies

def create_path_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)