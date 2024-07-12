"""
© Ocado Group
Created on 05/07/2024 at 16:18:48(+01:00).
"""

import typing as t

from django.db import models
from django.utils.translation import gettext_lazy as _

if t.TYPE_CHECKING:
    from django_stubs_ext.db.models import TypedModelMeta  # pragma: no cover
else:
    TypedModelMeta = object


class Contributor(models.Model):
    """A contributor that contributes to a repo"""

    id = models.IntegerField(
        primary_key=True, help_text=_("The contributor's GitHub user-ID.")
    )
    email = models.EmailField(_("email"))
    name = models.TextField(_("name"))
    location = models.TextField(_("location"))
    html_url = models.TextField(_("html url"))
    avatar_url = models.TextField(_("avatar url"))

    class Meta(TypedModelMeta):
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")

    def __str__(self):
        return f"{self.name} <{self.email}>"
