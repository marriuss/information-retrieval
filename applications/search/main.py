from es_search import ESDataSearch
from query_ui import QueryUI
import warnings


def main():
    """
    Entry point of search.
    """
    warnings.simplefilter("ignore")
    es_search = ESDataSearch()
    ui = QueryUI(es_search)
    ui.welcome()


if __name__ == "__main__":
    main()
