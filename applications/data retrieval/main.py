import time

from methods import (
    open_es_connection,
    get_scraper,
    add_data_to_index,
    save_progress
)

# scraping parameters
TIME_OUT = 300
PAGES_LIMIT = 50
ITERATIONS = 10


def main():
    """
    Entry point of scraping, parsing and indexing.
    """
    es = open_es_connection()
    scraper = get_scraper(es)

    try:
        i = 0
        while i < ITERATIONS:
            print(f"Iteration: {i + 1}.")
            scraper.crawl_site(PAGES_LIMIT)
            if scraper.scraping_end():
                print("There is nothing more to parse!")
                break
            parsed_data = scraper.get_data()
            add_data_to_index(es, parsed_data)
            save_progress(scraper)
            i += 1
            if i < ITERATIONS:
                time.sleep(TIME_OUT)

    except Exception as ex:
        print(str(ex))

    finally:
        es.close_connection()


if __name__ == "__main__":
    main()
