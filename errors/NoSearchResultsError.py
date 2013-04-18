from .APIError import APIError

class NoSearchResultsError(APIError):
    '''Exception thrown when a company cannot be found in the database'''
    def __init__(self, search):
        self.search    = search
        self.json_error = self.api_error(self.__repr__())

    def __repr__(self):
        return "No results for search term: {}".format(self.search)
