# Django Settings for Glorious Space - The Developer's Crown Jewel
# A Masterpiece Configuration for Excellence

import os
import sys
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add apps directory to Python path
sys.path.insert(0, os.path.join(BASE_DIR.parent, 'apps'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='glorious-space-dev-key-change-in-production-2024')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,0.0.0.0,*.ngrok.io,*.herokuapp.com').split(',')

if 'CODESPACE_NAME' in os.environ:
    codespace_name = config("CODESPACE_NAME")
    codespace_domain = config("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")
    CSRF_TRUSTED_ORIGINS = [f'https://{codespace_name}-8000.{codespace_domain}']

# Application definition - The Crown Jewels of Our Kingdom
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    # REST Framework for API Excellence
    'rest_framework',
    'rest_framework.authtoken',
    
    # CORS for Cross-Origin Resource Sharing
    'corsheaders',
    
    # Channels for WebSocket Magic
    'channels',
    
    # Django Extensions for Developer Productivity
    'django_extensions',
    
    # Admin Interface Enhancement
    'jazzmin',
    
    # OAuth and Social Authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    
    # Browser reload for development
    'django_browser_reload',
]

LOCAL_APPS = [
    # Our Magnificent Applications
    'users',
    'api',
    'core',
]

# Site Framework
SITE_ID = 1

# Middleware - The Guardians of Our Kingdom
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

X_FRAME_OPTIONS = "ALLOW-FROM preview.app.github.dev"

ROOT_URLCONF = "my_project.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'templates' / 'core',
            BASE_DIR / 'templates' / 'users',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = "my_project.wsgi.application"
ASGI_APPLICATION = 'my_project.asgi.application'

# Database Configuration - The Vault of Our Treasures
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation - Fortress Security
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

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Internationalization - Global Excellence
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images) - The Crown Jewels Display
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files - User Generated Masterpieces
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration - API Excellence
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS Configuration - Cross-Origin Excellence
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = DEBUG

# Session Configuration
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_COOKIE_NAME = 'glorious_sessionid'
SESSION_SAVE_EVERY_REQUEST = True

# Allauth Configuration - Social Authentication
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SESSION_REMEMBER = True

# Social Account Providers
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user:email',
            'read:user',
        ],
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
}

# Jazzmin Admin Configuration - Beautiful Admin Interface
JAZZMIN_SETTINGS = {
    "site_title": "Glorious Space Admin",
    "site_header": "Glorious Space",
    "site_brand": "Glorious Space",
    "welcome_sign": "Welcome to Glorious Space Admin - Your Developer Kingdom",
    "copyright": "Glorious Space - The Developer's Crown Jewel",
    "search_model": ["auth.User", "users.User"],
    
    # Icons
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "users.User": "fas fa-user-circle",
        "core": "fas fa-home",
        "api": "fas fa-code",
    },
    
    "show_sidebar": True,
    "navigation_expanded": True,
    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
}

# Custom Settings for Glorious Space
GLORIOUS_SPACE_VERSION = '1.0.0'
GLORIOUS_SPACE_TAGLINE = 'The Developer\'s Crown Jewel'
GLORIOUS_SPACE_DESCRIPTION = 'A magnificent platform where developers craft digital masterpieces with AI assistance.'

# Feature Flags
FEATURES = {
    'AI_CHAT': True,
    'CANVAS_PLAYGROUND': True,
    'PROJECT_SHOWCASE': True,
    'DEVELOPER_COMMUNITY': True,
}

print("🏰 Glorious Space Kingdom Initialized - The Developer's Crown Jewel Awaits! ✨")


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
