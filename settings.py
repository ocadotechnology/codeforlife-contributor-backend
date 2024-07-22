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

from pathlib import Path

# pylint: disable-next=wildcard-import,unused-wildcard-import
from codeforlife.settings import *

# Github
GH_ORG = "ocadotechnology"
GH_REPO =  "codeforlife-workspace"
GH_FILE = "CONTRIBUTING.md"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

DATABASES = get_databases(BASE_DIR)
STATIC_ROOT = get_static_root(BASE_DIR)
