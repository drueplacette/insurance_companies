from .APIError import APIError

class NoCompanyNameError(APIError):
    '''Exception thrown when a company cannot be found in the database'''
    def __init__(self, company):
        self.company    = company
        self.json_error = self.api_error(self.__repr__())

    def __repr__(self):
        return "No such company with name: {}".format(self.company)
