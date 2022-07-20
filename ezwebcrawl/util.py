import os
import requests
import asyncio
from proxybroker import Broker


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

"""Find and show 10 working HTTP(S) proxies."""
async def show_proxies_helper(proxies):
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


def save_proxies(count, filepath, types=['HTTP', 'HTTPS']):
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=types, limit=count),
        save_proxies_helper(proxies, filepath))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)

def load_proxies(filepath):
    proxies = []
    with open(filepath, mode='r', encoding='utf-8') as f:
        for line in f:
            proxies.append(line)
    return proxies

def show_proxies(count, types=['HTTP', 'HTTPS']):
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=types, limit=count),
        show_proxies_helper(proxies))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)