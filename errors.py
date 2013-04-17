'''Exception classes for better JSON errors'''

class APIError(Exception):
    '''Base Exception class for the Insurance Company Search API'''
    @classmethod
    def api_error(cls, message):
        '''JSON wrapper function for errors returned via JSON API'''
        return {"error": message}

class NoCompanyNameError(APIError):
    '''Exception thrown when a company cannot be found in the database'''
    def __init__(self, company):
        self.company    = company
        self.json_error = self.api_error(self.__repr__())

    def __repr__(self):
        return "No such company with name: {}".format(self.company)

class NoPayerIDError(APIError):
    '''Exception thrown when a payer ID cannot be found in the database'''
    def __init__(self, payer_id):
        self.payer_id   = payer_id
        self.json_error = self.api_error(self.__repr__())

    def __repr__(self):
        return "No such company with payer ID: {}".format(self.payer_id)
