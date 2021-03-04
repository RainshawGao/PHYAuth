"""
Django settings for PHYAuth project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import sys
from configparser import RawConfigParser
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_DIR = BASE_DIR / 'config'
CONFIG = RawConfigParser()
CONFIG.read(CONFIG_DIR / 'config.ini', encoding='utf-8')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

DEBUG = CONFIG.getboolean('DJANGO', 'DEBUG')

SECRET_KEY = CONFIG.get('DJANGO', 'SECRET_KEY')

ALLOWED_HOSTS = ['*']

# Application definition

DJANGO_APPS = [
    'django.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'oidc_provider',
    'django_celery_results',
    'django_celery_beat',
    'django_bootstrap_breadcrumbs',
    'guardian',
]
if DEBUG:
    THIRD_PARTY_APPS.append('debug_toolbar')
    INTERNAL_IPS = ['192.168.255.198']

LOCAL_APPS = [
    'app.users.apps.UsersConfig',
    'app.pku_iaaa.apps.PkuIaaaConfig',
    'app.portal.apps.PortalConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEBUG:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'PHYAuth.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.portal.context_processors.top_link',
            ],
            'builtins': [
                'django.templatetags.static',
                'django.templatetags.i18n'
            ],
        },
    },
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'PHYAuth.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DOMAIN = CONFIG.get("DJANGO", "DOMAIN")
SUBPATH = CONFIG.get("DJANGO", "SUBPATH")
if SUBPATH != '/' and not SUBPATH.endswith('/'):
    SUBPATH += '/'

LOGIN_REDIRECT_URL = SUBPATH
LOGIN_URL = SUBPATH + 'login'
LOGOUT_REDIRECT_URL = SUBPATH

LANGUAGE_COOKIE_PATH = SUBPATH

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'assets'
if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
        './static/'
    ]
else:
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASE_MAP = {
    'sqlite': 'django.db.backends.sqlite3',
    'mysql': 'django.db.backends.mysql',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'oracle': 'django.db.backends.oracle',
}

if CONFIG['DATABASE']['engine'] == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': DATABASE_MAP[CONFIG['DATABASE']['ENGINE']],
            'NAME': BASE_DIR / 'db.sqlite3',
            'OPTIONS': {
                'timeout': 20,
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': DATABASE_MAP[CONFIG['DATABASE']['ENGINE']],
            'NAME': CONFIG['DATABASE']['NAME'],
            'USER': CONFIG['DATABASE']['USER'],
            'PASSWORD': CONFIG['DATABASE']['PASSWORD'],
            'HOST': CONFIG['DATABASE']['HOST'],
            'PORT': CONFIG['DATABASE']['PORT'],
        }
    }

if CONFIG.get('REDIS', 'PWD') != '':
    REDIS_ADDRESS = ':{}@{}:{}'.format(CONFIG.get('REDIS', 'PWD'),
                                       CONFIG.get('REDIS', 'HOST'),
                                       CONFIG.get('REDIS', 'PORT'))
else:
    REDIS_ADDRESS = '{}:{}'.format(CONFIG.get('REDIS', 'HOST'),
                                   CONFIG.get('REDIS', 'PORT'))
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}/{}".format(REDIS_ADDRESS, CONFIG.get('REDIS', 'NUM')),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Redis Cache 过期设置
REDIS_TIMEOUT = 7 * 24 * 60 * 60
CUBES_REDIS_TIMEOUT = 60 * 60
NEVER_REDIS_TIMEOUT = 365 * 24 * 60 * 60

SESSION_COOKIE_AGE = 86400
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_PATH = SUBPATH
SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_PATH = SUBPATH

OIDC_USERINFO = 'app.users.oidc_scope_claims.userinfo'
OIDC_EXTRA_SCOPE_CLAIMS = 'app.users.oidc_scope_claims.CustomScopeClaims'

ADMINS = CONFIG.get('DJANGO', 'ADMINS')
ADMINS = [tuple(ADMINS.split())]

EMAIL_SUBJECT_PREFIX = CONFIG.get('EMAIL', 'SUBJECT_PREFIX')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = CONFIG.getboolean('EMAIL', 'USE_SSL')
EMAIL_HOST = CONFIG.get('EMAIL', 'HOST')
EMAIL_PORT = CONFIG.getint('EMAIL', 'PORT')
EMAIL_HOST_USER = CONFIG.get('EMAIL', 'USER')
EMAIL_HOST_PASSWORD = CONFIG.get('EMAIL', 'PASSWORD')
SERVER_EMAIL = EMAIL_FROM = CONFIG.get('EMAIL', 'FROM')
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOCALE_PATHS = [
    BASE_DIR / 'tpa_translation' / 'oidc_provider',
    BASE_DIR / 'tpa_translation' / 'django_celery_beat',
    BASE_DIR / 'tpa_translation' / 'django_celery_results',
    BASE_DIR / 'templates' / 'locale',
]

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]

GUARDIAN_MONKEY_PATCH = False
GUARDIAN_RAISE_403 = True

# Broker配置，使用Redis作为消息中间件
CELERY_BROKER_URL = 'amqp://{}:{}@{}:{}/{}'.format(
    CONFIG.get('RABBIT_MQ', 'USER'),
    CONFIG.get('RABBIT_MQ', 'PASSWORD'),
    CONFIG.get('RABBIT_MQ', 'HOST'),
    CONFIG.get('RABBIT_MQ', 'PORT'),
    CONFIG.get('RABBIT_MQ', 'NAME'),
)
# Celery 配置
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_WORKER_MAX_TASKS_PER_CHILD = 100000  # 每个worker执行10w个任务就会被销毁，可防止内存泄露

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
