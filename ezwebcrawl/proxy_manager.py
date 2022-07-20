class ProxyManager:
    # Proxy dictionary:
    # dict[key = proxy url] = tuple of (positive_feedback, negative_feedback, delta_feedback)
    def __init__(self, proxy_file_path):
        self.proxy_file_path = proxy_file_path
        proxies = self.load_proxies_from_file(proxy_file_path)
        self.set_proxies(proxies)

    def set_proxies(self, proxies):
        self.proxy_dictionary = {}
        for proxy in proxies:
            self.proxy_dictionary[proxy] = (0, 0, 0)
        self.recently_failed_proxies = []

    def get_filtered_proxy_dictionary(self, excluded_queue):
        filtered_dictionary = dict()
        # Iterate over all the items in dictionary
        for (key, value) in self.proxy_dictionary.items():
            # Check if item satisfies the given condition then add to new dict
            if key not in excluded_queue:
                filtered_dictionary[key] = value
        return filtered_dictionary

    def get_proxy(self):
        if self.proxy_dictionary is None or self.proxy_dictionary == {}:
            self.set_proxies(self.load_proxies_from_file(self.proxy_file_path))
        
        filtered_proxy_dictionary = self.get_filtered_proxy_dictionary(self.recently_failed_proxies)
        # Maximize the delta
        best_proxy = max(filtered_proxy_dictionary.items(), key=lambda x: x[1][2])[0]
        return best_proxy

    def proxy_feedback(self, proxy, was_good):
        print(f"Dictionary before: {self.proxy_dictionary}")
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
        print(f"Dictionary after: {self.proxy_dictionary}")


    def load_proxies_from_file(self, filepath):
        proxies = []
        with open(filepath, mode='r', encoding='utf-8') as f:
            for line in f:
                proxies.append(line)
        return proxies