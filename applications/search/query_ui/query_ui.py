import re


class QueryUI:

    def __init__(self, es_search):
        self._es_search = es_search

    def welcome(self):
        while True:
            ans = input("\nChoose an option (exit, search). ").strip()
            match ans:
                case "search":
                    query = self._make_query()
                    if query is not None:
                        results = self._es_search.search(query)
                        self._show_results(results)
                case "exit":
                    return
                case _:
                    continue

    def _make_query(self):
        index = self._choose_index()
        if index is not None:
            queries = self._get_queries(index)
            size = self._choose_size()
            return {"index": index, "queries": queries, "size": size}
        return None

    @staticmethod
    def _choose_size():
        size = ""
        while not isinstance(size, int):
            size = input("\nType a number of results to show: ").strip()
            try:
                size = int(size)
                if 0 >= size >= 1000:
                    size = ""
            except ValueError:
                pass
        return size

    def _get_queries(self, index):
        available_fields = self._es_search.get_fields(index)
        if available_fields is None:
            print("\nES server is not connected.")
            return None
        print(f"\nIndex {index} contains the following fields:")
        print(*available_fields, sep=", ")
        fields = []
        while not fields:
            print("\nType all of them you need:")
            input_fields = re.sub(r'(\s){2,}', ' ', input().strip()).split(' ')
            fields = [x for x in input_fields if x in available_fields]
        queries = {"must": [], "must_not": [], "should": []}
        for f in fields:
            print(f'\nOptions for the field "{f}".')
            q = input(f'\nType your query: ').strip()
            relation = ""
            while relation not in ["must", "should", "must_not"]:
                relation = input(f'Choose a relation (must/should/must_not): ').strip()
            ans = ""
            while ans not in ["y", "n"]:
                ans = input(f'Do you need an exact match with the query? (y/n): ').strip()
            operator = "AND" if ans == "y" else "OR"
            queries[relation].append({"field": f, "query": q, "operator": operator})
        return queries

    def _choose_index(self):
        available_indices = self._es_search.get_indices()
        if available_indices is None:
            print("\nES server is not connected.")
            return None
        print("\nAvailable indices to search in:")
        print(*available_indices, sep=", ")
        index = ""
        while index not in available_indices:
            print("\nType the one of them you need:")
            index = input().strip()
            if index == "exit":
                return
        return index

    @staticmethod
    def _show_results(results):
        print("\nYour results:")
        if results is not None:
            if not results:
                print("No results.")
            for i, hit in enumerate(results):
                print(f"({i + 1}) Match score: {hit.meta.score}. URL: {hit.url}")
        else:
            print("Illegal query.")
