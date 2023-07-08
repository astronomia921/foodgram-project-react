import re
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('secret_key', default='123dvvdsvnsidj21')

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    os.getenv('web_url'),
    os.getenv('web_name')
]

CSRF_TRUSTED_ORIGINS = [os.getenv('web_url'), os.getenv('web_name')]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'djoser',
    "debug_toolbar",

    'api.apps.ApiConfig',

    'apps.users.apps.UsersConfig',
    'apps.ingredients.apps.IngredientsConfig',
    'apps.tags.apps.TagsConfig',
    'apps.foodgram.apps.FoodgramConfig',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodgram_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodgram_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'django'),
        'USER': os.getenv('POSTGRES_USER', 'django_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', '5432')
    }
}

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'backend_static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PAGINATOR_PAGE = 10

MAX_LENGTH_NAME = 200

MAX_LENGTH_UNIT = 50

MAX_LENGTH_TAG = 50

MAX_LENGTH_HEX = 7

MAX_LENGTH_SLUG = 50

MAX_LENGTH_DIGITS = 6

MAX_DECIMAL_PLACES = 2

LENGTH_HEADER = 20

MAX_LENGTH_USERNAME = 150

MAX_LENGTH_EMAIL = 254

REGEX_USER = re.compile(r'^[\w.@+-]+\Z')

REGEX_VALIDATORS = '^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'

FILE_PATH = 'foodgram-project-react/backend/foodgram_backend/data/ingredients.json'

#  'foodgram-project-react/data/ingredients.json'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.PageNumberPagination'),
    'PAGE_SIZE': PAGINATOR_PAGE,

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'],
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
    ]
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False,
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_URL': 'users/set_password/{uid}/{token}',
    'SERIALIZERS': {
        'user_create': 'api.users.users_serializers.UserCreateSerializer',
        'user': 'api.users.users_serializers.CustomUserSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
        'current_user': 'api.users.users_serializers.CustomUserSerializer',
        'set_password': 'djoser.serializers.SetPasswordSerializer',
        'set_password_retype': (
            'djoser.serializers.SetPasswordRetypeSerializer'),
        'token': 'djoser.serializers.TokenSerializer',
        'token_create': 'djoser.serializers.TokenCreateSerializer',
    },
    'PERMISSIONS': {
        'user': ('rest_framework.permissions.IsAuthenticated',),
        'user_list': ('rest_framework.permissions.AllowAny',)
    }
}

AUTH_USER_MODEL = 'users.User'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
