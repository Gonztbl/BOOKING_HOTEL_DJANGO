# --- START OF FILE settings.py (UPDATED) ---

from pathlib import Path
import environ # <== THÊM MỚI
import os      # <== THÊM MỚI

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- KHỞI TẠO DJANGO-ENVIRON ---
env = environ.Env(
    # Thiết lập kiểu dữ liệu và giá trị mặc định
    DEBUG=(bool, False)
)
# Đọc file .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
# --- KẾT THÚC KHỞI TẠO ---


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Đọc SECRET_KEY từ file .env
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# Đọc DEBUG từ file .env
DEBUG = env('DEBUG')

# ALLOWED_HOSTS nên được cấu hình trong .env khi triển khai
# Ví dụ: ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
# ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


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

# Đọc cấu hình database từ file .env
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': env('DB_NAME', default='Hotel'),
        'USER': env('DB_USER', default='sa'),
        'PASSWORD': env('DB_PASSWORD', default='123456'),
        'HOST': env('DB_HOST', default='DESKTOP-T84E9CO'),
        'PORT': env('DB_PORT', default=''),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
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
# --- Static files (CSS, JavaScript, Images tĩnh) ---
STATIC_URL = '/static/'
# BỔ SUNG: Thư mục để Django tìm các file static
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'booking/static'), # Chỉ định rõ thư mục static của app booking
]
# <== BỔ SUNG TOÀN BỘ KHỐI NÀY VÀO FILE SETTINGS.PY ==>

# --- Media files (Ảnh do người dùng upload) ---
# Cấu hình URL và thư mục lưu trữ cho file media

# URL để truy cập các file media trên trình duyệt (ví dụ: /media/ten_anh.jpg)
MEDIA_URL = '/media/'

# Đường dẫn đến thư mục vật lý trên server để lưu các file media
# Django sẽ tự tạo thư mục 'media' ở thư mục gốc của dự án cho bạn.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- PAYOS SETTINGS ---
# Đọc cấu hình PayOS từ file .env
PAYOS_CLIENT_ID = env('PAYOS_CLIENT_ID', default='')
PAYOS_API_KEY = env('PAYOS_API_KEY', default='')
PAYOS_CHECKSUM_KEY = env('PAYOS_CHECKSUM_KEY', default='')