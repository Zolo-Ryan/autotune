"""
Django settings for autotune project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import logging
import os
from pathlib import Path

import coloredlogs
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG")

# ALLOWED_HOSTS = []

# Open AI key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Number of examples to generate in each iteration
LLM_GENERATION_NUM_SAMPLES = os.getenv("LLM_GENERATION_NUM_SAMPLES")

# Size for batching tasks
MAX_BATCH_SIZE = os.getenv("MAX_BATCH_SIZE")

# Redis Configuration
REDIS_URL = os.getenv("REDIS_URL")

# Celery Configuration
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_MAX_RETRIES = os.getenv("CELERY_MAX_RETRIES")
CELERY_TIMEZONE = "UTC"

# HuggingFace token
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

HUGGING_FACE_USERNAME = os.getenv("HUGGING_FACE_USERNAME")

MINIO_BASE_URL = os.getenv("MINIO_BASE_URL")

MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")

MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

MINIO_SECURE_CONN = os.getenv("MINIO_SECURE_CONN") == "True"

MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
    "rest_framework",
    "workflow",
    "workflowV2",
]

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

ROOT_URLCONF = "autotune.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "autotune.wsgi.application"
ASGI_APPLICATION = "autotune.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/autotune"
)

DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "../staticfiles")

STATICFILES_DIRS = [
    os.path.join(
        BASE_DIR, "staticfiles"
    ),  # Adjust this path if your static files are located elsewhere
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}


ALLOWED_HOSTS = ["*"]

CORS_ALLOWED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

CORS_ORIGIN_WHITELIST = (
    "localhost:8000",
    "localhost",
)

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]

level_styles = {
    "info": {"color": "green"},  # Info logs are green
    "warning": {"color": "yellow"},
    "error": {"color": "red"},
    "critical": {"color": "red", "bold": True},  # Critical logs in bold red
}

coloredlogs.install(
    level="INFO",
    logger=logging.getLogger(),  # Root logger
    fmt="%(levelname)s - %(name)s - %(asctime)s - %(message)s",
    level_styles=level_styles,  # Apply custom level styles
)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
    },
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)",
        },
        "colored": {
            "format": "%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],  # Add both file and console handlers
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
