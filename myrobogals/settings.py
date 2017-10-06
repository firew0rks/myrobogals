import os
from ConfigParser import RawConfigParser # import configparser py3

ROBOGALS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = RawConfigParser()
config.read(ROBOGALS_DIR + '/settings.ini')

DEBUG = config.getboolean('debug', 'DEBUG')

SECRET_KEY = config.get('secrets', 'SECRET_KEY')

API_SECRET = config.get('secrets', 'API_SECRET')

ADMINS = tuple(config.items('admin'))

MANAGERS = tuple(config.items('manager'))

ALLOWED_HOSTS = list(tuple(config.get('debug', 'INTERNAL_IPS').split()))

DATABASES = {
	'default': {
		'ENGINE': config.get('database', 'DATABASE_ENGINE'),
		'NAME': ROBOGALS_DIR + '/' + config.get('database', 'DATABASE_NAME'),
	}
}

USE_TZ = True
TIME_ZONE = 'Etc/UTC'
DATE_FORMAT = 'D j M y'
DATE_FORMAT_LONG = 'l j F Y'
TIME_FORMAT = 'g:i a'
DATETIME_FORMAT = 'g:i a, D j M y'
DATETIME_FORMAT_LONG = 'g:i a, l j F Y'

LANGUAGES = (
	('en', 'English'),
	('nl', 'Dutch'),
	('ja', 'Japanese'),
)

LANGUAGE_CODE = 'en'

SITE_ID = 1

USE_I18N = True

# Logs users out within a day
SESSION_COOKIE_AGE = 86400
SESSION_SAVE_EVERY_REQUEST = True


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ROBOGALS_DIR + config.get('media', 'MEDIA_ROOT')

# URL that handles the media in "rgmedia"
# Put a trailing slash if there is a path component (optional in other cases).
# The default '/rgmedia' will work when using the Django dev server and debug = True
MEDIA_URL = config.get('media', 'MEDIA_URL')

# Path and URL for where the static files are being served from
# e.g. my.robogals.org/{STATIC_URL}/path-to-file
STATIC_URL = '/static/'

# Location to all of the individual apps that have static files
STATICFILES_DIRS = [
	os.path.join(ROBOGALS_DIR, "static"),
	os.path.join(ROBOGALS_DIR, "myrobogals/rgprofile/static"),
	os.path.join(ROBOGALS_DIR, "myrobogals/rgmain/static"),
	os.path.join(ROBOGALS_DIR, "myrobogals/rgwiki/static"),
]

# Where collectstatic will store all the static files when 'python manage.py collectstatic' is ran
STATIC_ROOT = ROBOGALS_DIR + '/staticfiles'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			ROBOGALS_DIR + '/templates',
			ROBOGALS_DIR + 'myrobogals/rgmain/templates',
			ROBOGALS_DIR + 'myrobogals/rgteaching/templates',
			ROBOGALS_DIR + 'myrobogals/rgwiki/templates',
			ROBOGALS_DIR + '/rgtemplates'
		],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.contrib.auth.context_processors.auth',
				'django.template.context_processors.debug',
				'django.template.context_processors.i18n',
				'django.template.context_processors.media',
				'django.template.context_processors.static',
				'django.template.context_processors.tz',
				'django.template.context_processors.request',
				'django.contrib.messages.context_processors.messages'
			],
		},
	},
]

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'myrobogals.rgmain.middleware.TimezoneMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
)

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'myrobogals.urls'
LOGIN_URL = '/login/'

TINYMCE_JS_URL = MEDIA_URL + '/js/tiny_mce/tiny_mce.js'
TINYMCE_DEFAULT_CONFIG = {
	'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,formatselect,fontselect,fontsizeselect",
	'theme_advanced_buttons2' : "bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,forecolor",
	'theme_advanced_buttons3' : "hr,removeformat,visualaid,|,sub,sup,|,charmap",
	'theme_advanced_toolbar_location' : "top",
	'theme_advanced_toolbar_align' : "left",
	'theme_advanced_statusbar_location' : "bottom",
	'theme_advanced_resizing' : False,
	'width' : 585,
	'height' : 500,
	'theme' : "advanced",
	'relative_urls': False,
}
TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = False
TINYMCE_FILEBROWSER = False

LOCALE_PATHS = (
	ROBOGALS_DIR + '/rgtemplates/locale',
	ROBOGALS_DIR + '/myrobogals/locale',
)

FIXTURE_DIRS = (
	ROBOGALS_DIR + '/myrobogals/fixtures',
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.admin',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.staticfiles',
	'myrobogals.rgmain',
	'myrobogals.rgprofile',
	'myrobogals.rgchapter',
	'myrobogals.rgteaching',
	'myrobogals.rgmessages',
	'myrobogals.rgweb',
	'myrobogals.filters',
	'myrobogals.rgforums',
	'myrobogals.rgconf',
	'myrobogals.rgreport',
	'myrobogals.rgwiki',
	'tinymce',
	'widget_tweaks',
	'markdownx',
)

AUTH_USER_MODEL = 'rgprofile.User'

GENDERS = (
	(0, '---'),
	(1, 'Male'),
	(2, 'Female'),
	(3, 'Other'),
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Directory for uploaded profile images
PROFILE_IMAGE_UPLOAD_DIR = 'profilepics/'

# Maximum size for uploaded images in kilobytes
PROFILE_IMAGE_MAX_SIZE = 512

# The default profile image for users who haven't uploaded one yet
PROFILE_IMAGE_DEFAULT = 'profilepics/default.png'

# Used to debug emails without STMP servers set up on local machine
if DEBUG:
	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
