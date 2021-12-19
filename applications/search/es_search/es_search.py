from applications.es_connection import ESConnection
from elasticsearch_dsl import Search, Q


class ESDataSearch(ESConnection):

    def __init__(self):
        super(ESDataSearch, self).__init__()

    def search(self, query_dict=None):
        if self._connected():
            index = query_dict["index"]
            if self._es.indices.exists(index):
                s = Search(using=self._es, index=index)
                if query_dict is not None:
                    size = query_dict["size"]
                    query_relations = query_dict["queries"]
                    relations = {"must": [], "should": []}
                    for relation, queries in query_relations.items():
                        for query in queries:
                            field = query["field"]
                            q = query["query"]
                            operator = query["operator"]
                            query_match = Q("match",
                                            **{field: {
                                                "query": q,
                                                "operator": operator,
                                                "boost": 1.3,
                                            }})
                            query_match_phase = Q("match_phrase",
                                                  **{field: {
                                                      "query": q,
                                                      "boost": 1.7
                                                  }})
                            query_fuzzy = Q("fuzzy",
                                            **{field: {
                                                "value": q,
                                                "prefix_length": 2,
                                                "boost": 1.0
                                            }})
                            q_list = [query_match, query_match_phase, query_fuzzy]
                            relations[relation].extend(
                                [Q("bool", should=q_list)] if relation == "must"
                                else q_list
                            )
                    q = Q("bool",
                          must=relations["must"],
                          should=relations["should"]
                          )

                    s = s.query(q)
                    s = s[:size]
                    results = None
                    try:
                        results = s.execute()
                        print("\nResults amount:", results.hits.total["value"])
                    except Exception as ex:
                        print(str(ex))
                    return results

    def get_indices(self):
        if self._connected():
            return self._es.indices.get_alias().keys()
        return None

    def get_fields(self, index):
        if self._connected():
            return self._es.indices.get_mapping(index=index)[index]["mappings"]["properties"].keys()
        return None
