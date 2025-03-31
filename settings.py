"""
© Ocado Group
Created on 04/07/2024 at 11:42:01(+01:00).

Django settings for api.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

from codeforlife import set_up_settings
from codeforlife.tasks import CeleryBeat

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

secrets = set_up_settings(BASE_DIR, service_name="contributor")

# pylint: disable-next=wildcard-import,unused-wildcard-import,wrong-import-position
from codeforlife.settings import *

SECRET_KEY = secrets.SECRET_KEY

# GitHub

GH_ORG = "ocadotechnology"
GH_REPO = "codeforlife-workspace"
GH_FILE = "CONTRIBUTING.md"
GH_CLIENT_ID = os.environ["GH_CLIENT_ID"]
GH_CLIENT_SECRET = secrets.GH_CLIENT_SECRET

# Installed Apps
# https://docs.djangoproject.com/en/4.2/ref/settings/#installed-apps

INSTALLED_APPS.remove("codeforlife.user")
INSTALLED_APPS.remove("game")  # TODO: remove after restructure
INSTALLED_APPS.remove("portal")  # TODO: remove after restructure
INSTALLED_APPS.remove("common")  # TODO: remove after restructure

# Auth user model
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#substituting-a-custom-user-model

AUTH_USER_MODEL = "api.contributor"

# Authentication backends
# https://docs.djangoproject.com/en/4.2/ref/settings/#authentication-backends

AUTHENTICATION_BACKENDS = ["api.auth.backends.GitHubBackend"]

# Sessions
# https://docs.djangoproject.com/en/4.2/topics/http/sessions/

SESSION_ENGINE = "api.models.session"

# Celery
# https://docs.celeryq.dev/en/v5.4.0/userguide/configuration.html

CELERY_BEAT_SCHEDULE = {
    "clear-sessions-once-per-day-at-4pm": CeleryBeat(
        task="api.tasks.session.clear",
        schedule=CeleryBeat.crontab(hour=16),
    ),
}
