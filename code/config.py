from code.__version__ import VERSION


class Config:
    VERSION = VERSION

    #SECRET_KEY = os.environ.get('SECRET_KEY', None)
    SECRET_KEY = 'not use'


    # Supported types with rules
    CCT_OBSERVABLE_TYPES = {
        'ip': {},
        'user': {}
    }

    CTR_HEADERS = {
        'User-Agent': ('SecureX Threat Response Integrations '
                       '<tr-integrations-support@cisco.com>')
    }