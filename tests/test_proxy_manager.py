from ezwebcrawl.proxy_manager import ProxyManager

class TestProxyManager:
   
    @classmethod
    def setup_class(self):
        pass

    @classmethod
    def teardown_class(self):
        pass

    def test_filter_bad_proxies(self):
        proxies = ["http://00.000.000.000:0000","http://00.000.000.000:0001","http://00.000.000.000:0002"]
        pm = ProxyManager.from_list(proxies)
        pm.proxy_feedback(proxies[0], False)
        pm.proxy_feedback(proxies[1], False)
        assert len(pm.recently_failed_proxies) == len(proxies) - 2
        assert pm.get_proxy() == proxies[2]