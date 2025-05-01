"""
© Ocado Group
Created on 02/07/2024 at 11:58:24(+01:00).
"""

from django.apps import AppConfig


# pylint: disable-next=missing-class-docstring
class SrcConfig(AppConfig):
    name = "src"

    def ready(self):
        # pylint: disable-next=import-outside-toplevel,unused-import
        from . import signals
