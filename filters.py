'''Defines extra filters for use with the API server'''

def urlencode_filter(config):
    '''Decodes urlencoded strings'''
    regexp = r'.+'

    def to_python(match):
        return match.replace('+', ' ')

    def to_url(string):
        return string.repace(' ', '+')

    return regexp, to_python, to_url

def uppercase_filter(config):
    '''Decodes urlencoded strings'''
    regexp = r'.+'

    def to_python(match):
        return match.upper()

    def to_url(string):
        return string

    return regexp, to_python, to_url
