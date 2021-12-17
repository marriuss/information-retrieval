### Project structure:

#### Data retrieval (`data retrieval`):
1) `data`: 
   * `parsed_data`: data, retrieved while parsing and that isn't indexed yet
   * `scraper`: binary file, that contains the `Scarper` object
2) `parsing`: 
   * class `Parser`
   * class `ParserSettings`
3) `scraping`:
   * class `Scraper`
   * class `ScraperSettings`
4) `storing`:
   * class `ESDataStoring` (derived from `ESConnection`)
   * class `IndexBody`
5) `settings`: data, used as settings for scraping, parsing and storing:
   * `indices_settings`: a set of directories, each of which represents one index and contains JSON-files with settings and mappings for the index
   * `parser_settings`: parser settings, should return a dictionary, in which keys are names of indices and values are functions, that parse a page, specific for the index
   * `scraper_settings`: scraper settings, should return the first URL to scape and a list of URL-patterns to ignore or to parse while scraping
6) `main.py`: an entry point for scraping, parsing and storing
7) `methods.py`: additional methods, which are used in main function

#### Elascticsearch connection (`es_connection`): class `ESConnection`

#### Search (`search`):
1) `es_search`: class `ESDataSearch`
2) `query_ui`: class `QueryUI`
3) `main.py`: an entry point for search



