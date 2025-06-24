"""
© Ocado Group
Created on 11/04/2024 at 16:51:46(+01:00).

The entrypoint to our app.
"""

from codeforlife.server import Server

server = Server()

# pylint: disable=wrong-import-position
from django.conf import settings
from django.contrib.sites.models import Site

Site.objects.get_or_create(
    domain=settings.SERVICE_DOMAIN,
    defaults={"name": settings.SERVICE_DOMAIN},
)

server.run()
