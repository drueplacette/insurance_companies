from .APIError import APIError

class NoPayerIDError(APIError):
    '''Exception thrown when a payer ID cannot be found in the database'''
    def __init__(self, payer_id):
        self.payer_id   = payer_id
        self.json_error = self.api_error(self.__repr__())

    def __repr__(self):
        return "No such company with payer ID: {}".format(self.payer_id)
