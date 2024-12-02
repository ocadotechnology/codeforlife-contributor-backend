"""
© Ocado Group
Created on 04/07/2024 at 11:42:00(+01:00).

Django settings for api.

Generated by 'django-admin startproject' using Django 3.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# NOTE: Must come before importing CFL settings.
os.environ["SERVICE_NAME"] = "contributor"

# GitHub

GH_ORG = "ocadotechnology"
GH_REPO = "codeforlife-workspace"
GH_FILE = "CONTRIBUTING.md"
GH_CLIENT_ID = os.getenv("GH_CLIENT_ID", "Ov23liBErSabQFqROeMg")
GH_CLIENT_SECRET = os.getenv("GH_CLIENT_SECRET", "replace-me")

# pylint: disable-next=wildcard-import,unused-wildcard-import,wrong-import-position
from codeforlife.settings import *

# Installed Apps
# https://docs.djangoproject.com/en/3.2/ref/settings/#installed-apps

INSTALLED_APPS.remove("codeforlife.user")
INSTALLED_APPS.remove("game")  # TODO: remove after restructure
INSTALLED_APPS.remove("portal")  # TODO: remove after restructure
INSTALLED_APPS.remove("common")  # TODO: remove after restructure

# Auth user model
# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#substituting-a-custom-user-model

AUTH_USER_MODEL = "api.contributor"

# Authentication backends
# https://docs.djangoproject.com/en/3.2/ref/settings/#authentication-backends

AUTHENTICATION_BACKENDS = ["api.auth.backends.GitHubBackend"]

# Sessions
# https://docs.djangoproject.com/en/3.2/topics/http/sessions/

SESSION_ENGINE = "api.models.session"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# TODO: move to cfl package and create helper functions.
# STATIC_ROOT = get_static_root(BASE_DIR)
STATIC_ROOT = os.getenv("STATIC_ROOT", BASE_DIR / "static")
STATIC_URL = os.getenv("STATIC_URL", "/static/")
STATICFILES_DIRS = ["static"]

# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN")
AWS_LOCATION = os.getenv("AWS_LOCATION")
AWS_DEFAULT_ACL = os.getenv("AWS_DEFAULT_ACL")
AWS_S3_ADDRESSING_STYLE = os.getenv("AWS_S3_ADDRESSING_STYLE")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")

if AWS_STORAGE_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = "storages.backends.s3.S3Storage"
    STATICFILES_STORAGE = "storages.backends.s3.S3Storage"
