"""
© Ocado Group
Created on 02/07/2024 at 15:12:59(+01:00).
"""

import typing as t

from django.db import models
from django.utils.translation import gettext_lazy as _

if t.TYPE_CHECKING:
    from django_stubs_ext.db.models import TypedModelMeta
else:
    TypedModelMeta = object


class Fruit(models.Model):
    """A piece of fruit."""

    name = models.CharField(_("name"), max_length=50)
    is_citrus = models.BooleanField(_("is citrus"))
    expires_on = models.DateField(_("expires on"))

    class Meta(TypedModelMeta):
        verbose_name = _("fruit")
        verbose_name_plural = _("fruits")

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return isinstance(other, Fruit) and self.expires_on < other.expires_on
