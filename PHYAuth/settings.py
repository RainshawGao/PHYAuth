"""
Django settings for PHYAuth project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import environ
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

DEBUG = env("DEBUG", cast=bool, default=True)
print(DEBUG)
if DEBUG:
    from .dev import *
else:
    from .prod import *

ALLOWED_HOSTS = ['*']

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'oidc_provider'
]

LOCAL_APPS = [
    'app.users.apps.UsersConfig',
    'app.pku_iaaa.apps.PkuIaaaConfig',
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
    'oidc_provider.middleware.SessionManagementMiddleware',
]

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
            ],
            'builtins': [
                'django.templatetags.static',
                'django.templatetags.i18n'
            ],
        },
    },
]

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

SUB_PATH = '/'

LOGIN_REDIRECT_URL = SUB_PATH
LOGIN_URL = SUB_PATH + 'login'
LOGOUT_REDIRECT_URL = SUB_PATH

SESSION_COOKIE_PATH = LANGUAGE_COOKIE_PATH = CSRF_COOKIE_PATH = SUB_PATH

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'assets'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    './static/'
]

OIDC_USERINFO = 'users.oidc_provider_settings.userinfo'
OIDC_EXTRA_SCOPE_CLAIMS = 'users.oidc_provider_settings.CustomScopeClaims'
OIDC_SESSION_MANAGEMENT_ENABLE = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOCALE_PATHS = [
    BASE_DIR / 'tpa_translation' / 'oidc_provider',
    BASE_DIR / 'templates' / 'locale',
]

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "app.pku_iaaa.auth_backends.AuthenticationBackend",
]

SESSION_COOKIE_AGE = 86400
