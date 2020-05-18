"""
Django settings for sermons project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from dotenv import load_dotenv


load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False if os.getenv("DEBUG", "False") == "False" else "True"
DEBUG = False
DEBUG_DATES = False
MODE = "web"
APP_VERSION = 1.0

ALLOWED_HOSTS = ["*", "127.0.0.1:8000", "127.0.0.1", "dailyoffice2019.com", "www.dailyoffice2019.com"]


# Application definition

INSTALLED_APPS = [
    "ckeditor",
    "adminsortable2",
    "django.contrib.admin",
    # "material.admin",
    # "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django_extensions",
    'rest_framework',
    "website",
    # "sermons",
    "churchcal",
    "psalter",
    "bible",
    "mathfilters",
    "meta",
    "office",
    "djrichtextfield",
    "taggit",
    "address",
    "array_tags",
    "django_distill",
    "webpack_loader",
    "robots",
]

if DEBUG:
    INSTALLED_APPS = ["debug_toolbar"] + INSTALLED_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

ROOT_URLCONF = "website.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "office.context_processors.settings",
            ]
        },
    }
]

WSGI_APPLICATION = "website.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_NAME", "dailyoffice2"),
        "USER": os.getenv("POSTGRES_USER", "dailyoffice"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "dailyoffice"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


INTERNAL_IPS = ["127.0.0.1"]
# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = BASE_DIR + "/uploads/"

MEDIA_URL = "/uploads/"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

SHELL_PLUS = "ipython"

JET_DEFAULT_THEME = "light-green"
JET_SIDE_MENU_COMPACT = True
JET_CHANGE_FORM_SIBLING_LINKS = True

JET_THEMES = [
    {
        "theme": "default",  # theme folder name
        "color": "#47bac1",  # color of the theme's button in user menu
        "title": "Default",  # theme title
    },
    {"theme": "green", "color": "#44b78b", "title": "Green"},
    {"theme": "light-green", "color": "#2faa60", "title": "Light Green"},
    {"theme": "light-violet", "color": "#a464c4", "title": "Light Violet"},
    {"theme": "light-blue", "color": "#5EADDE", "title": "Light Blue"},
    {"theme": "light-gray", "color": "#222", "title": "Light Gray"},
]

DJRICHTEXTFIELD_CONFIG = {
    "js": ["//cdn.tinymce.com/4/tinymce.min.js"],
    "init_template": "djrichtextfield/init/tinymce.js",
    "settings": {
        "menubar": True,
        "toolbar": "formatselect | bold italic strikethrough forecolor backcolor permanentpen formatpainter | link image media pageembed | alignleft aligncenter alignright alignjustify  | numlist bullist outdent indent | removeformat | addcomment",
        "width": "100%",
        "height": 800,
    },
}

GOOGLE_API_KEY = "AIzaSyAoETL2PnO843Q98QgumZg756AAHAzhhRw"


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar}

DISTILL_DIR = "{}/../static_export".format(BASE_DIR)

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": False,
        "BUNDLE_DIR_NAME": "office/js/",  # must end with slash
        "STATS_FILE": os.path.join(BASE_DIR, "webpack-stats.json"),
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}

CACHES = {"default": {"BACKEND": "django.core.cache.backends.memcached.MemcachedCache", "LOCATION": "127.0.0.1:11211"}}

SITE_ID = 1

FIRST_BEGINNING_YEAR = 2018
LAST_BEGINNING_YEAR = 2021

FIRST_BEGINNING_YEAR = 2019
LAST_BEGINNING_YEAR = 2019

META_SITE_PROTOCOL = "https"
META_SITE_DOMAIN = "www.dailyoffice2019.com"
META_SITE_TYPE = "website"
META_SITE_NAME = "The Daily Office"
META_DEFAULT_KEYWORDS = [
    "daily office",
    "prayer",
    "divine office",
    "daily prayer",
    "evening prayer",
    "morning prayer",
    "compline",
    "midday prayer",
    "noonday prayer",
    "nones",
    "matins",
    "vespers",
    "evensong",
    "liturgy of the hours",
    "breviary",
    "anglican",
    "episcopal",
    "Anglican Church in North America",
    "ACNA",
    "common prayer",
    "book of common prayer",
    "bcp",
    "2019",
]
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_GOOGLEPLUS_PROPERTIES = True
META_USE_TITLE_TAG = True
META_SITE_TYPE = "website"
META_FB_APPID = "826553607777260"
META_FB_AUTHOR_URL = "https://www.dailyoffice2019.com"
META_TWITTER_AUTHOR = "Daily Office, Book of Common Prayer 2019"
META_TWITTER_SITE = "https://www.dailyoffice2019.com"
META_OG_SECURE_URL_ITEMS = []

ROBOTS_SITEMAP_URLS = ["https://www.dailyoffice2019.com/sitemap.xml"]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
