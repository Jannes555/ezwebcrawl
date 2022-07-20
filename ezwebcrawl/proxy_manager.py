import logging
from typing import Dict, List, Tuple

class ProxyManager:
    """Keeps track of the current proxies and how well they're performing."""

    @classmethod
    def from_file(cls, file_path: str):
        return ProxyManager(file_path = file_path)

    @classmethod
    def from_list(cls, proxies_list: List[str]):
        return ProxyManager(proxies_list = proxies_list)


    def __init__(self, *args, **kwargs):
        self.initial_proxy_list = kwargs.get("proxies_list",[])
        self.proxy_file_path = kwargs.get("file_path", "")

        # Set the proxies
        if self.initial_proxy_list != []:
            self.set_proxies(self.initial_proxy_list)
        if self.proxy_file_path != "":
            self.set_proxies(self.load_proxies_from_file(self.proxy_file_path))

    def set_proxies(self, proxies: List[str]):
        # Proxy dictionary:
        # dict[key = proxy url] = tuple of (positive_feedback, negative_feedback, delta_feedback)
        self.proxy_dictionary: Dict[str, Tuple[int, int, int]] = {}
        for proxy in proxies:
            self.proxy_dictionary[proxy] = (0, 0, 0)
        self.recently_failed_proxies: List[str] = []

    def get_filtered_proxy_dictionary(self, excluded_list: List[str]) -> Dict[str, Tuple[int, int, int]]:
        filtered_dictionary = dict()
        # Iterate over all the items in dictionary
        for (key, value) in self.proxy_dictionary.items():
            # Check if item satisfies the given condition then add to new dict
            if key not in excluded_list:
                filtered_dictionary[key] = value
        return filtered_dictionary

    def get_proxy(self) -> str:
        # Filter out recently failed proxies
        filtered_proxy_dictionary = self.get_filtered_proxy_dictionary(self.recently_failed_proxies)

        # Maximize the delta
        best_proxy = max(filtered_proxy_dictionary.items(), key=lambda x: x[1][2])[0]
        
        return best_proxy

    def proxy_feedback(self, proxy, was_good):
        logging.debug(f"Dictionary before: {self.proxy_dictionary}")
        current = self.proxy_dictionary[proxy]
        if was_good:
            new = (current[0] + 1, current[1], current[0] + 1 - current[1])
        else:
            new = (current[0], current[1] + 1, current[0] - current[1] - 1)
            self.recently_failed_proxies.append(proxy)
            max_length = len(self.proxy_dictionary) - 2
            if len(self.recently_failed_proxies) > max_length:
                self.recently_failed_proxies.remove(self.recently_failed_proxies[max_length - 1])
        self.proxy_dictionary[proxy] = new
        logging.debug(f"Dictionary after: {self.proxy_dictionary}")


    def load_proxies_from_file(self, path: str) -> List[str]:
        """
            Expects a file in this format:\r\n
            http://35.230.142.201:8080\r\n
            http://5.161.105.105:80\r\n
            ...
        """
        proxies = []
        with open(path, mode='r', encoding='utf-8') as f:
            for line in f:
                proxies.append(line)
        return proxies