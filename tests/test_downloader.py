import pytest
import os
from ezwebcrawl.downloader import Downloader
from ezwebcrawl.util import find_proxies


class TestDownloader:
    temp_path = os.path.join(os.path.dirname(__file__), "temp")

    @classmethod
    def setup_class(cls):
        cls.proxy_file_location = os.path.join(TestDownloader.temp_path, "proxies.txt")
        if not os.path.exists(cls.proxy_file_location):
            find_proxies(10, cls.proxy_file_location, ['HTTP'])

    @classmethod
    def teardown_class(cls):
        os.remove(cls.proxy_file_location)

    @pytest.mark.asyncio
    async def test_download_wikpedia_using_proxy(self):
        url = "https://www.wikipedia.org/"
        file_name = os.path.join(TestDownloader.temp_path, "wikipedia.html")
        dl = Downloader(self.proxy_file_location)
        await dl.download_pages([url],[file_name])
        assert os.path.exists(file_name)

        # Clean up
        os.remove(file_name)
