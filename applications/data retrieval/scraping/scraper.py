import time
from random import randint, choice
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin


class WebScraper:

    def __init__(self, settings, parsed):
        self._url = None
        self._parsed_url_patterns = None
        self._ignored_url_patterns = None
        self._parser = None
        self._proxies_list = None
        self.update(settings, parsed)
        self._DOMAIN = self._get_domain(self._url)
        self._visited = set([])
        self._url_frontier = {self._url}
        self._error_pages = {"parse errors": []}
        self._errors = []

    def update(self, settings, parser):
        self._set_settings(settings)
        self._set_parser(parser)
        self._set_proxies_list()

    def crawl_site(self, pages_limit):
        i = 0
        while self._url_frontier and i < pages_limit:
            self._wait()
            i += 1
            url = list(self._url_frontier)[0]
            print(url)
            response = self._get_request(url)
            self._url_frontier.remove(url)
            code = response.status_code
            if code != 200:
                self._error_pages.setdefault(code, [])
                self._error_pages[code].append(url)
                self._errors.append(f"HTTP request to page {url}: code {code}.")
                continue
            self._visited.add(url)
            page = BeautifulSoup(response.content, 'html.parser')
            new_urls = set([l for l in self._get_page_urls(url, page) if l not in self._visited])
            page_info = self._get_page_parsing_info(url)
            if page_info:
                self._parse_page_data(page, page_info, url)
            self._url_frontier = set.union(self._url_frontier, new_urls)

    def get_data(self):
        return self._parser.get_data()

    def scraping_end(self):
        return len(self._url_frontier) == 0

    def print_url_frontier(self):
        print(self._url_frontier)

    def _set_settings(self, settings):
        self._url = settings.url
        self._parsed_url_patterns = settings.parsed_url_patterns
        self._ignored_url_patterns = settings.ignored_url_patterns

    def _set_parser(self, parser):
        self._parser = parser

    def _set_proxies_list(self):
        self._proxies_list = self._get_proxies_list()

    @staticmethod
    def _get_domain(url):
        return urlparse(url).netloc

    def print_error_pages(self):
        print("Errors:")
        for key, values in self._error_pages.items():
            print(key, ":", values)

    def _get_page_urls(self, page_url, page):
        links = [l.attrs.get("href") for l in page.find_all("a")]
        urls = set([])
        for l in links:
            if l is None:
                continue
            components = urlparse(l)
            if not components.netloc:
                l = urljoin(page_url, l)
            if self._valid(l):
                urls.add(l)
        return urls

    def _ignored_url(self, url):
        for pattern in self._ignored_url_patterns:
            match = pattern.match(url)
            if match is not None:
                return True
        return False

    def _valid(self, url):
        domain = self._get_domain(url)
        return self._DOMAIN == domain and not self._ignored_url(url)

    def _get_page_parsing_info(self, url):
        for doc_type, pattern in self._parsed_url_patterns.items():
            match = pattern.match(url)
            if match is not None:
                return doc_type, match.groups()
        return None

    def _get_request(self, url):
        response = None
        while response is None:
            headers, proxies = self._get_random_setup()
            try:
                response = requests.get(url, headers=headers, proxies=proxies)
            except Exception:
                self._proxies_list.remove(proxies["https"])
        return response

    def _parse_page_data(self, page, page_info, url):
        page_type, groups = page_info
        result = self._parser.try_parse_page(page, page_type, url, groups)
        if result is not None:
            self._errors.append(result)
            self._error_pages["parse errors"].append(url)

    def _get_random_setup(self):
        headers = choice(HEADERS_LIST)
        if not self._proxies_list:
            proxies = {}
        else:
            proxy = choice(self._proxies_list)
            proxies = {"http": proxy, "https": proxy}
        return headers, proxies

    @staticmethod
    def _get_proxies_list():
        from lxml.html import fromstring
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr')[:100]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
        return list(proxies)

    @staticmethod
    def _wait():
        waiting_time = randint(2, 8)
        time.sleep(waiting_time)


HEADERS_LIST = [
    # Firefox 77 Mac
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Firefox 77 Windows
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Chrome 83 Mac
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    },
    # Chrome 83 Windows
    {
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    },
]
