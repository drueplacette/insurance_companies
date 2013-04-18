class APIError(Exception):
    '''Base Exception class for the Insurance Company Search API'''
    def api_error(self, message):
        '''JSON wrapper function for errors returned via JSON API'''
        return {'error': {'message':message, 'type':self._get_error_name()}}

    def _get_error_name(self):
        return str(self.__class__).split('.')[-1].split('\'')[0]
