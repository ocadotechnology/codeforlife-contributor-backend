"""
© Ocado Group
Created on 11/04/2024 at 16:51:46(+01:00).

The entrypoint to our app.
"""

import os

# from codeforlife.app import StandaloneApplication
from django.core.asgi import get_asgi_application
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# TODO: delete this
# pylint: disable-all

import multiprocessing
import typing as t

from django.core.management import call_command
from gunicorn.app.base import BaseApplication  # type: ignore[import-untyped]


# pylint: disable-next=abstract-method
class StandaloneApplication(BaseApplication):
    """A server for an app in a live environment.

    Based off of:
    https://gist.github.com/Kludex/c98ed6b06f5c0f89fd78dd75ef58b424
    https://docs.gunicorn.org/en/stable/custom.html
    """

    def __init__(self, app: t.Callable):
        call_command("migrate", interactive=False)

        self.options = {
            "bind": "0.0.0.0:8080",
            # https://docs.gunicorn.org/en/stable/design.html#how-many-workers
            "workers": 1,
            "worker_class": "uvicorn.workers.UvicornWorker",
        }
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    StandaloneApplication(app=get_asgi_application()).run()
else:
    app = get_wsgi_application()
