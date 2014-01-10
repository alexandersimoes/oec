# -*- coding: utf-8 -*-
import os
from werkzeug.contrib.cache import RedisCache
from redis import Redis, ConnectionError

'''
    Used for finding environment variables through configuration
    if a default is not given, the site will raise an exception
'''
def get_env_variable(var_name, default=-1):
    try:
        return os.environ[var_name]
    except KeyError:
        if default != -1:
            return default
        error_msg = "Set the %s os.environment variable" % var_name
        raise Exception(error_msg)

''' Base directory of where the site is held '''
basedir = os.path.abspath(os.path.dirname(__file__))

''' CSRF (cross site forgery) for signing POST requests to server '''
CSRF_EN = True

''' Secret key should be set in environment var '''
SECRET_KEY = get_env_variable("OEC_SECRET_KEY", "default-dataviva.mg-secr3t")

''' Default debugging to True '''
DEBUG = True
SQLALCHEMY_ECHO = True

''' 
    Details for connecting to the database, credentials set as environment
    variables.
'''
SQLALCHEMY_DATABASE_URI = "mysql://{0}:{1}@{2}/{3}".format(
    get_env_variable("OEC_DB_USER", "root"), 
    get_env_variable("OEC_DB_PW", ""), 
    get_env_variable("OEC_DB_HOST", "localhost"),
    get_env_variable("OEC_DB_NAME", "oec"))

''' If user prefers to connect via socket set env var '''
if "OEC_DB_SOCKET" in os.environ:
    SQLALCHEMY_DATABASE_URI += "?unix_socket=" + get_env_variable("OEC_DB_SOCKET")

''' If an env var for production is set turn off all debugging support '''
if "OEC_PRODUCTION" in os.environ:
    SQLALCHEMY_ECHO = False
    DEBUG = False

''' Available languages '''
LANGUAGES = {
    'ar': u'العربية',
    'de': u'Deutsch',
    'el': u'Ελληνικά',
    'en': u'English',
    'es': u'Español',
    'fr': u'français',
    'he': u'עברית',
    'hi': u'हिंदी',
    'it': u'italiano',
    'ja': u'日本語',
    'ko': u'한국어',
    'nl': u'Nederlands',
    'ru': u'Pyccĸий',
    'pt': u'Português',
    'tr': u'Tϋrkçe',
    'zh_cn': u'中文'
}

''' 
    Setup redis caching connection to be used throughout the site. Credentials
    are set in their respective env vars.
'''
REDIS = Redis(host=get_env_variable("OEC_REDIS_HOST", "localhost"), 
         port=get_env_variable("OEC_REDIS_PORT", 6379), 
         password=get_env_variable("OEC_REDIS_PW", None))
REDIS_CACHE = RedisCache(host=get_env_variable("OEC_REDIS_HOST", "localhost"), 
         port=get_env_variable("OEC_REDIS_PORT", 6379), 
         password=get_env_variable("OEC_REDIS_PW", None), default_timeout=2591999)
try:
    REDIS.client_list()
except ConnectionError:
    REDIS, REDIS_CACHE = [None]*2