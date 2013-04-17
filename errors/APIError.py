class APIError(Exception):
    '''Base Exception class for the Insurance Company Search API'''
    @classmethod
    def api_error(cls, message):
        '''JSON wrapper function for errors returned via JSON API'''
        return {"error": message}
