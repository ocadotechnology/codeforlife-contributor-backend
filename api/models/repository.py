"""
© Ocado Group
Created on 05/07/2024 at 16:39:14(+01:00).
"""

import typing as t

from django.db import models
from django.utils.translation import gettext_lazy as _

from .contributor import Contributor

if t.TYPE_CHECKING:
    from django_stubs_ext.db.models import TypedModelMeta  # pragma: no cover
else:
    TypedModelMeta = object


class Repository(models.Model):
    """A repository to contribute to"""

    id = models.IntegerField(primary_key=True)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    NAME_CHOICES = [("portal", "portal"), ("rr", "rr")]
    name = models.TextField(choices=NAME_CHOICES)
    points = models.IntegerField(default=0)

    class Meta(TypedModelMeta):
        unique_together = ["contributor", "name"]
        verbose_name = _("repository")
        verbose_name_plural = _("repositories")

    def __str__(self):
        return self.name
