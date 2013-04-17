'''Defines a bottle.py filter for decoding (and encoding) strings for URLs'''

def urlencode_filter(config):
    '''Decodes urlencoded strings'''
    regexp = r'.+'

    def to_python(match):
        return match.replace('+', ' ')

    def to_url(string):
        return string.repace(' ', '+')

    return regexp, to_python, to_url
