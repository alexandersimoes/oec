# Django settings for atlas project.

# In order to set up the site on your local machine
# the marked lines need to be edited with your own settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
  ('Alexander Simoes', 'simoes@mit.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'atlas',
    'USER': 'user_name_here', # NEED TO EDIT
    'PASSWORD': 'some_password_here', # NEED TO EDIT
    'HOST': '',
    'PORT': '',
  }
}

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en'
SITE_ID = 1
USE_I18N = True
DEFAULT_CHARSET = "utf-8"
LOCALE_PATHS = (
  '/full/path/atlas_economic_complexity/django_files/locale/', # NEED TO EDIT
)
TEMPLATE_CONTEXT_PROCESSORS = (
  "django.contrib.auth.context_processors.auth",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.static",
  "django.contrib.messages.context_processors.messages",
  "atlas.context_processors.supported_langs",
)
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/media/'
STATICFILES_DIRS = (
  '/full/path/atlas_economic_complexity/media/', # NEED TO EDIT
)
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
SECRET_KEY = 'you_secret_key' # NEED TO EDIT
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.locale.LocaleMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  # Uncomment the next line for simple clickjacking protection:
  # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'atlas.urls'
WSGI_APPLICATION = 'atlas.wsgi.application'

TEMPLATE_DIRS = (
  '/full/path/atlas_economic_complexity/html/', # NEED TO EDIT
)

INSTALLED_APPS = (
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django.contrib.humanize',
  'observatory',
  'blog'
)