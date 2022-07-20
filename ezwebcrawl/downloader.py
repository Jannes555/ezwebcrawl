import asyncio
import aiohttp
import logging
from typing import Any, List, Optional, Tuple

from .proxy_manager import ProxyManager

class Downloader:
    def __init__(self, proxy_file_path: str):
        self.proxy_file_path = proxy_file_path
        self.proxy_manager = ProxyManager.from_file(proxy_file_path)

    async def download_pages(self, urls: List[str], output_paths: List[str], decode = True):
        """Downloads the pages in urls and saves them to the files in output_paths.
        Use decode = False for non-text content (e.g. images)
        """
        tasks = [self.__fetch(url, output_path, decode) for url, output_path in zip(urls, output_paths)]
        for task in asyncio.as_completed(tasks):
            url, content = await task
            logging.debug(f'Done! url: {url}; content: {content}')


    async def __fetch(self, url: str, output_path: str, decode = True) -> Tuple[str, Any]:
        retries: int = 10
        response: Optional[bytes] = None
        for i in range(retries):
            proxy_url = self.proxy_manager.get_proxy()
            logging.debug(f"Try {i} with proxy {proxy_url}")
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, proxy=proxy_url, timeout=15) as resp:
                        response = await resp.read()

                        if response is None:
                            logging.debug("Response is none, continuing")
                            self.proxy_manager.proxy_feedback(proxy_url, False)
                            continue

                        response_length = len(response)
                        logging.debug(f"Resp length: {response_length}")
                        if response_length < 800:
                            self.proxy_manager.proxy_feedback(proxy_url, False)
                            continue
                        if decode:
                            with open(output_path, mode='w', encoding="utf-8") as f:
                                f.write(response.decode())
                        else:
                            with open(output_path, mode='wb') as f:
                                f.write(response)
                        self.proxy_manager.proxy_feedback(proxy_url, True)
            except Exception as e:
                logging.debug(f'Attempt {i}: Error. url: {url}; error: {e}')
                self.proxy_manager.proxy_feedback(proxy_url, False)
                continue
            if response is not None:
                return (url, response)
        return (url,"") # Couldn't download the page within the nr of retries