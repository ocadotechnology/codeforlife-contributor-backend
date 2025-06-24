"""
© Ocado Group
Created on 11/04/2024 at 16:51:46(+01:00).

The entrypoint to our app.
"""

from codeforlife.server import Server as _Server


# pylint: disable-next=abstract-method,missing-class-docstring
class Server(_Server):
    def load_config(self):
        self.options["forwarded_allow_ips"] = "*"
        return super().load_config()


server = Server()

# pylint: disable=wrong-import-position
from django.conf import settings
from django.contrib.sites.models import Site

Site.objects.get_or_create(
    domain=settings.SERVICE_DOMAIN,
    defaults={"name": settings.SERVICE_DOMAIN},
)

server.run()
