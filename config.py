# -*- coding: utf-8 -*-
import os

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
SQLALCHEMY_DATABASE_URI = "mysql://{0}:{1}@{2}/{3}?charset=utf8".format(
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
    'el': u'ελληνικά',
    'en': u'English',
    'es': u'Español',
    'fr': u'Français',
    'he': u'עברית',
    'hi': u'हिन्दी',
    'it': u'Italiano',
    'ja': u'日本語',
    'ko': u'한국어',
    'mn': u'Монгол',
    'nl': u'Nederlands',
    'ru': u'Pyccĸий',
    'pt': u'Português',
    'tr': u'Tϋrkçe',
    'vi': u'Tiếng Việt',
    'zh': u'简化中国'
}

''' 
    Setup filesystem caching used only for profile views. If directory 
    evironment variable not set, defaults to null.
'''
if get_env_variable("CACHE_DIR", None):
    CACHE_TYPE="filesystem"
    CACHE_DIR=get_env_variable("CACHE_DIR")
else:
    CACHE_TYPE="null"
CACHE_DEFAULT_TIMEOUT=2592000 # 30 days
CACHE_THRESHOLD=4200

FACEBOOK_ID = get_env_variable("OEC_FACEBOOK_ID",0)
