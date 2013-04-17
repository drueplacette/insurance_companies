'''Defines a bottle.py filter for upcasing inputs passed in via URL'''

def uppercase_filter(config):
    '''Converts lowercase inputs to uppercase'''
    regexp = r'.+'

    def to_python(match):
        return match.upper()

    def to_url(string):
        return string

    return regexp, to_python, to_url
