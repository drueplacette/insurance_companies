'''Exception classes for better JSON errors'''

class APIError(Exception):
    '''Base Exception class for the Insurance Company Search API'''
    @classmethod
    def api_error(cls, message):
        '''JSON wrapper function for errors returned via JSON API'''
        return {"error": message}

class NoSuchCompanyError(APIError):
    '''Exception thrown when a company cannot be found in the database'''
    def __init__(self, company):
        self.company    = company
        self.json_error = self.api_error(self.__repr__())

    def __repr__(self):
        return "No such company: {}".format(self.company)
