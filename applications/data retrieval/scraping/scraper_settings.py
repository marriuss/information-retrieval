import re
from dataclasses import dataclass


@dataclass
class ScraperSettings:

    url: str
    parsed_url_patterns: dict
    ignored_url_patterns: list

    def __post_init__(self):
        self.parsed_url_patterns = {doc_type: re.compile(url) for doc_type, url in self.parsed_url_patterns.items()}
        self.ignored_url_patterns = [re.compile(url) for url in self.ignored_url_patterns]