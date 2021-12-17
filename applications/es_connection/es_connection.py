from elasticsearch import Elasticsearch


class ESConnection:

    def __init__(self):
        self._es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def close_connection(self):
        if self._connected():
            self._es.transport.close()

    def _connected(self):
        return self._es.ping()