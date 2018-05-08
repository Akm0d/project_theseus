import os

''' SERVER SETTINGS '''


class Config(object):
    """
    TEMPLATES_AUTO_RELOAD specifies whether Flask should check for modifications to templates and
    reload them automatically
    """
    TEMPLATES_AUTO_RELOAD = True

    '''
    TRUSTED_PROXIES defines a set of regular expressions used for finding a user's IP address if the WebApp instance
    is behind a proxy. If you are running a CTF and users are on the same network as you, you may choose to remove
    some proxies from the list.

    WebApp only uses IP addresses for cursory tracking purposes. It is ill-advised to do anything complicated based
    solely on IP addresses.
    '''
    TRUSTED_PROXIES = [
        '^127\.0\.0\.1$',
        # Remove the following proxies if you do not trust the local network
        # For example if you are running a CTF on your laptop and the teams are all on the same network
        '^::1$',
        '^fc00:',
        '^10\.',
        '^172\.(1[6-9]|2[0-9]|3[0-1])\.',
        '^192\.168\.'
    ]

    '''
    CACHE_TYPE specifies how WebApp should cache configuration values. If CACHE_TYPE is set to 'redis', WebApp will make use
    of the REDIS_URL specified in environment variables. You can also choose to hardcode the REDIS_URL here.

    It is important that you specify some sort of cache as WebApp uses it to store values received from the database.

    CACHE_REDIS_URL is the URL to connect to Redis server.
    Example: redis://user:password@localhost:6379

    http://pythonhosted.org/Flask-Caching/#configuring-flask-caching
    '''
    CACHE_REDIS_URL = os.environ.get('REDIS_URL')
    if CACHE_REDIS_URL:
        CACHE_TYPE = 'redis'
    else:
        CACHE_TYPE = 'simple'

    '''
    UPDATE_CHECK specifies whether or not WebApp will check whether or not there is a new version of WebApp
    '''
    UPDATE_CHECK = True
