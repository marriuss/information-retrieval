from dataclasses import dataclass


@dataclass(frozen=True)
class IndexBody:

    settings: dict
    mappings: dict

    def generate_body(self):
        return \
            {
                "settings": self.settings,
                "mappings": self.mappings
            }