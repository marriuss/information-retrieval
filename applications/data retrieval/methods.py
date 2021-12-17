import os
import pickle
import json
from datetime import datetime

from parsing import ParserSettings, Parser
from scraping import ScraperSettings, WebScraper
from storing import ESDataStoring, IndexBody

from settings import URL, IGNORED_URL_PATTERNS, PARSED_URL_PATTERNS, PARSING_FUNCTIONS

# paths constants
DATA_DIR = "data"
SETTINGS_DIR = "settings"
PARSER_DATA_DIR = "parsed_data"
INDICES_SETTINGS_DIR = "indices_settings"
SCRAPER_FILE = "scraper"


def new_progress():
    settings = ScraperSettings(url=URL, parsed_url_patterns=PARSED_URL_PATTERNS,
                               ignored_url_patterns=IGNORED_URL_PATTERNS)
    parser = Parser(ParserSettings(PARSING_FUNCTIONS))
    return WebScraper(settings, parser)


def update_scraper(scraper):
    settings = ScraperSettings(url=URL, parsed_url_patterns=PARSED_URL_PATTERNS,
                               ignored_url_patterns=IGNORED_URL_PATTERNS)
    parser = Parser(ParserSettings(PARSING_FUNCTIONS))
    scraper.update(settings, parser)


def load_progress():
    with open(f"{DATA_DIR}/{SCRAPER_FILE}", "rb") as f:
        return pickle.load(f)


def save_progress(scraper_data):
    with open(f"{DATA_DIR}/{SCRAPER_FILE}", "wb") as f:
        pickle.dump(scraper_data, f)


def load_data(file_name):
    with open(f"{DATA_DIR}/{PARSER_DATA_DIR}/{file_name}", "rb") as f:
        return pickle.load(f)


def save_data(data):
    date = datetime.now().strftime("%d-%m-%Y %H.%M.%S")
    with open(f"{DATA_DIR}/{PARSER_DATA_DIR}/{date}", "wb") as f:
        pickle.dump(data, f)


def add_data_to_index(es, data):
    result = es.try_add_data(data)
    if result is not None:
        save_data(result)


def load_indices():
    try:
        indices_settings = {}
        for root, folders, _ in os.walk(f"{SETTINGS_DIR}/{INDICES_SETTINGS_DIR}"):
            for index_name in folders:
                path = f"{root}/{index_name}"
                for file in os.listdir(path):
                    with open(f"{path}/{file}") as f:
                        match file:
                            case "settings.json":
                                settings = json.load(f)
                            case "mappings.json":
                                mappings = json.load(f)
                            case _:
                                pass
                indices_settings[index_name] = IndexBody(settings=settings, mappings=mappings)
        return indices_settings
    except Exception as ex:
        print(str(ex))
        return None


def get_scraper(es):
    if not os.path.exists(f"{DATA_DIR}/{SCRAPER_FILE}"):
        scraper = new_progress()
    else:
        scraper = load_progress()
        parsed_data = os.listdir(f"{DATA_DIR}/{PARSER_DATA_DIR}")
        if len(parsed_data) != 0:
            for file_name in parsed_data:
                data = load_data(file_name)
                print(data)
                os.remove(f"{DATA_DIR}/{PARSER_DATA_DIR}/{file_name}")
                add_data_to_index(es, data)
        # update_scraper(scraper)
    return scraper


def open_es_connection():
    indices = load_indices()
    return ESDataStoring(indices)
