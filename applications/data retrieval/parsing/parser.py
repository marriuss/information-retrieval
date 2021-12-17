
class Parser:
    def __init__(self, settings):
        self._settings = settings
        self._parsing_functions = settings.parsing_functions
        self._data = None
        self._reset_data()

    def try_parse_page(self, page, doc_type, url, groups):
        try:
            parsing_function = self._parsing_functions[doc_type]
            record = parsing_function(page, url, groups)
            if record is not None:
                self._data[doc_type].append(record)
        except Exception as ex:
            return str(ex)

    def get_data(self):
        data = dict(self._data)
        self._reset_data()
        return data

    def _reset_data(self):
        self._data = self._settings.get_data_dictionary()

