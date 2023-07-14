# Adding time delta for SimpleJWT
from datetime import timedelta
from pathlib import Path
from decouple import config
import os
import dotenv

dotenv.load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "10.0.2.2",
    "localhost",
    "127.0.0.1",
    "django-api-backend.azurewebsites.net",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    
    #! ==== Adding corsheaders =====
    'corsheaders',
    
    #! rest_framework and Simple_JWT
    'rest_framework',
    'rest_framework_simplejwt',
    
    #!local
    'users',
    
    #! === Income and Category ===
    'Income_Category',
    'Income',
    
    #! === Subscription (Order and Product)===
    'order.apps.OrderConfig',
    'product.apps.ProductConfig',
    
    #! === Expenses and Category ===
    'Expenses',
    'Expenses_Category',
    
    
    ## === Carries all the major functionality of the project
    'Core',
    
    ## === Budget Limitter ===
    'Limit',
    
    ## === # ToDO List ===
    'Todo',
    
]

MIDDLEWARE = [
    # Also add corsheaders.middleware here ##NOTE: Should be kept as high as possible in Middleware
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"templates"],
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

WSGI_APPLICATION = 'backend.wsgi.application'



## Adding Media
MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# === SQL DATABASE
 
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': config("DATABASE_NAME"),
#         'USER': config("DATABASE_USER"),
#         'PASSWORD': config("DATABASE_PASSWORD"),
#         'HOST': config("DATABASE_HOST"),
#         'PORT': config("DATABASE_PORT"),
#     }
# }



# === SQLITE DATABASE
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

#*  === Postgres Database ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DBNAME"),
        'USER': os.getenv("DBUSER"),
        'PASSWORD': os.getenv("DBPASS"),
        'HOST': os.getenv("DBHOST"),
        'PORT': os.getenv("DBPORT"),
        'OPTIONS': {
            # 'sslmode': 'require',
            # 'sslrootcert': os.path.join(BASE_DIR,'DigiCertGlobalRootCA.crt.pem'),
        }
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT =  BASE_DIR / 'staticfiles'

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ===Adding custom user model and helps control the fieldset =====
AUTH_USER_MODEL = 'users.myUser'


# == Email Configuration ===
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' 
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# === SENDGRID CREDENTIALS ===
EMAIL_HOST_PASSWORD = config('API_KEY')
DEFAULT_FROM_EMAIL = config('EMAIL_FROM')



# Added during the project

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    
    # ==== To disable the browseable API ====
    #'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',)
}


# ========== Simple JWT's behavior settings ===========

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1,minutes=20),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",
}



# === Setting the life of the Reset Password Token ===
PASSWORD_RESET_TIMEOUT = 500 #for 500 seconds

# ==== Adding the origins to allow the domains =====
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWED_ORIGINS = [
    
]

STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")
STRIPE_PRIVATE_KEY = os.environ.get("STRIPE_PRIVATE_KEY")
STRIPE_WEBHOOK_SECERET = os.environ.get("STRIPE_WEBHOOK_SECERET")