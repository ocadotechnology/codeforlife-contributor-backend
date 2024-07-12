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
    """A repository that a contributor has contributed to."""

    contributor_id: int
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)

    gh_id = models.IntegerField(
        _("GitHub ID"),
        help_text=_("Github ID of the repo a contributor has contributed to."),
    )
    points = models.IntegerField(
        _("points"),
        default=0,
        help_text=_("Story points the contributor closed for this repository."),
    )

    class Meta(TypedModelMeta):
        unique_together = ["contributor", "gh_id"]
        verbose_name = _("repository")
        verbose_name_plural = _("repositories")

    def __str__(self):
        return f"{self.contributor.pk}:{self.gh_id}"
