from es_search import ESDataSearch
from query_ui import QueryUI
import warnings


def main():
    warnings.simplefilter("ignore")
    es_search = ESDataSearch()
    ui = QueryUI(es_search)
    ui.welcome()


main()
