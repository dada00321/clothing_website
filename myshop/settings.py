import os
from braintree import Configuration, Environment

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ehm)git78+a-s&gq9fb-j)c9_5itz46!3v5qzs4cj(#^z^_u2a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	"shop.apps.ShopConfig",
	"cart.apps.CartConfig",
	"orders.apps.OrdersConfig",
    "payment.apps.PaymentConfig",
    "coupons.apps.CouponsConfig",
    "rosetta",
    "django.contrib.postgres",
    "search.apps.SearchConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myshop.urls'

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
                "cart.context_processors.cart",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

WSGI_APPLICATION = 'myshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'clothes2u',
        'USER': 'dada00321',
        'PASSWORD': 'Lzp1314520',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

TIME_ZONE = "Asia/Taipei"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGE_CODE = "zh-hant"

LANGUAGES = (
    ("en", "English"),
    ("zh-hant", "Traditional Chinese"),
    ("zh-hans", "Simplified Chinese"),
    ("ja", "Japanese"),
)

# 設定我們的語言檔案所放的路徑
# 此例採用 Two Scoops 的結構， locale 放在：
#     {專案路徑}/locale
# 因設定檔路徑如下，所以 -3 將設定檔路徑前移為 {專案路徑}/ 作為 ROOT_DIR
#     {專案路徑}/config/settings/{設定檔}.py

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale/"),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
#STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
CART_SESSION_ID = "cart"

# 設定本機 SMTP ("管理員" email)
# P.S. 需要開啟"允許低安全性應用程式"
#      否則無法使用此處設定的信箱寄信
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX@gmail.com"
EMAIL_HOST_PASSWORD = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
EMAIL_PORT = 678
EMAIL_USE_TLS = True

# 設定第三方支付模組 Braintree
BRAINTREE_MERCHANT_ID = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # Merchant ID
BRAINTREE_PUBLIC_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # Public key
BRAINTREE_PRIVATE_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # Private key

#Environment.Production
Configuration.configure(
    Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)
