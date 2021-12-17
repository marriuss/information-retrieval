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

                    def get_queries(relation):
                        queries = []
                        for query in query_relations[relation]:
                            field = query["field"]
                            q = query["query"]
                            operator = query["operator"]
                            queries.append(Q("match",
                                             **{field: {
                                                    "query": q,
                                                    "prefix_length": 2,
                                                    "fuzziness": "AUTO",
                                                    "operator": operator
                                             }}))
                        return queries

                    q = Q("bool",
                          must=get_queries("must"),
                          should=get_queries("should"),
                          must_not=get_queries("must_not")
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

