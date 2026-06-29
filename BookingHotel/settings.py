# --- START OF FILE settings.py (UPDATED) ---

from pathlib import Path
import environ
import os
import pymysql
pymysql.install_as_MySQLdb()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- KHỞI TẠO DJANGO-ENVIRON ---
env = environ.Env(
    DEBUG=(bool, False)
)
# Đọc file .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
# --- KẾT THÚC KHỞI TẠO ---


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=False)

# ALLOWED_HOSTS configuration
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS.extend(['127.0.0.1', 'localhost', '.onrender.com'])
    ALLOWED_HOSTS = list(set([host.strip(' "\'') for host in ALLOWED_HOSTS if host.strip()]))

# CSRF configuration for production (required when behind a proxy/HTTPS)
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=['https://*.onrender.com'])
if not CSRF_TRUSTED_ORIGINS or CSRF_TRUSTED_ORIGINS == ['']:
    CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']
else:
    CSRF_TRUSTED_ORIGINS.extend(['https://*.onrender.com'])
    CSRF_TRUSTED_ORIGINS = list(set([origin.strip(' "\'') for origin in CSRF_TRUSTED_ORIGINS if origin.strip()]))

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'booking',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BookingHotel.urls'

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

WSGI_APPLICATION = 'BookingHotel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# === TIDB MYSQL DATABASE CONFIGURATION ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bookinghotel',
        'USER': '3q3Yfgwt9qwz5pZ.root',
        'PASSWORD': 'fTgvHBRiVRym2Za1',
        'HOST': 'gateway01.ap-northeast-1.prod.aws.tidbcloud.com',
        'PORT': '4000',
        'OPTIONS': {
            'ssl': {
                'ca': os.path.join(BASE_DIR, 'isrgrootx1.pem')  # ví dụ: 'certs/ca.pem'
            }
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# STATICFILES_DIRS
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'booking/static'),
]

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Media files (Ảnh do người dùng upload) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- PAYOS SETTINGS ---
PAYOS_CLIENT_ID = env('PAYOS_CLIENT_ID', default='')
PAYOS_API_KEY = env('PAYOS_API_KEY', default='')
PAYOS_CHECKSUM_KEY = env('PAYOS_CHECKSUM_KEY', default='')

# === PRODUCTION SETTINGS ===
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
