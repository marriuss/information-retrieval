from dataclasses import dataclass


@dataclass
class ParserSettings:
    parsing_functions: dict

    def __post_init__(self):
        self.doc_types = list(self.parsing_functions.keys())

    def get_data_dictionary(self):
        return {doc_type: [] for doc_type in self.doc_types}
