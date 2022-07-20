import asyncio
import pytest
import os
from ezwebcrawl import downloader

# Example
@pytest.mark.asyncio
async def test_download_anything():
    dl = downloader.Downloader("proxies.txt")
    assert await dl.get_pages_async(["https://www.wikipedia.org/"],["wiki.html"])
    assert os.path.exists("wiki.html")



# Personal tests
async def main():
    dl = downloader.Downloader("proxies.txt")
    await dl.get_pages_async(["https://www.wikipedia.org/"],["wiki.html"])

if __name__ == '__main__':
    asyncio.run(main())
    