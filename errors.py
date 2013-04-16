'''Exception classes for better JSON errors'''

class APIError(Exception):
    def api_error(message):
        '''JSON wrapper function for errors returned via JSON API'''
        return {"errors": message}

class NoSuchCompanyError(APIError):
    def __init__(self, company):
        self.company = company

    def __repr__(self):
        return self.api_error("No such company: {}".format(self.company))

class NoSearchResultsError(APIError):
    def __init__(self, search):
        self.search = search

    def __repr__(self):
        return self.api_error("No search results for: {}".format(self.search))
