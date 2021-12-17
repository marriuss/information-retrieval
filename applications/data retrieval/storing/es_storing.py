from applications.es_connection import ESConnection


class ESDataStoring(ESConnection):

    def __init__(self, indices):
        super(ESDataStoring, self).__init__()
        self._INDICES = indices
        if self._connected():
            for index in self._INDICES.keys():
                if not self._index_exists(index):
                    self._create_index(index)

    def try_add_data(self, data):
        result = True
        if not self._connected():
            return data
        errors = {key: [] for key in data.keys()}
        for index, value in data.items():
            for document in value:
                try:
                    self._es.index(index=index, doc_type="_doc", body=document)
                except Exception as ex:
                    print(str(ex))
                    result = False
                    errors[index].append(document)
        return None if result else errors

    def _create_index(self, name):
        try:
            body = self._INDICES[name].generate_body()
            self._es.indices.create(index=name, body=body)
        except Exception as ex:
            print(str(ex))

    def _index_exists(self, index):
        return self._es.indices.exists(index=index)
