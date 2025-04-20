from pathlib import Path
import os

# Make imports optional for development
try:
    import dj_database_url
    HAVE_DJ_DATABASE_URL = True
except ImportError:
    HAVE_DJ_DATABASE_URL = False

try:
    import whitenoise
    HAVE_WHITENOISE = True
except ImportError:
    HAVE_WHITENOISE = False

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-p3x)s!#!s1!ky1@4l1a4y_z9&_4=jt+ztz5bix&o*+)lc+gd)0')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# Updated to include PythonAnywhere and Render domains
ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    '.pythonanywhere.com', 
    '.ngrok-free.app',
    '.onrender.com'
] + os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'crop_recommendation',
    'users',
    'community',  # Add the community app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
]

if HAVE_WHITENOISE:
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware') 

MIDDLEWARE += [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Security settings for production
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    
    # Only use these settings if not running locally
    if not any(host in ['localhost', '127.0.0.1'] for host in ALLOWED_HOSTS):
        SECURE_SSL_REDIRECT = True
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True
    
    SECURE_HSTS_PRELOAD = True

ROOT_URLCONF = 'model.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'model/templates', 
            'home/templates',
            'crop_recommendation/templates',
            'users/templates',
            'community/templates',  # Add community templates
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # Add media context processor
            ],
        },
    },
]

WSGI_APPLICATION = 'model.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Use DATABASE_URL environment variable if available and dj_database_url is installed
if HAVE_DJ_DATABASE_URL:
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        DATABASES['default'] = dj_database_url.parse(database_url)

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Media files (Images uploaded by users)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Set this to True to allow serving media files even in production
SERVE_MEDIA_IN_PRODUCTION = True

# For production environments like Render.com
if not DEBUG:
    # Ensure media files persist across deployments by using a persistent directory
    if os.environ.get('RENDER', False):
        MEDIA_ROOT = '/opt/render/project/data/media'
        # Create directory if it doesn't exist
        os.makedirs(MEDIA_ROOT, exist_ok=True)

# Whitenoise settings for serving static files in production
if HAVE_WHITENOISE:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    WHITENOISE_AUTOREFRESH = True
    WHITENOISE_USE_FINDERS = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URL
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'homepage'
