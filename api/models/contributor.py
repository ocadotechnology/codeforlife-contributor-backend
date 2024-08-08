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

    pk: int
    id = models.IntegerField(
        primary_key=True, help_text=_("The contributor's GitHub user-ID.")
    )
    email = models.EmailField(_("email"))
    name = models.TextField(_("name"))
    location = models.TextField(_("location"), null=True)
    html_url = models.TextField(_("html url"))
    avatar_url = models.TextField(_("avatar url"))
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    class Meta(TypedModelMeta):
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")

    def __str__(self):
        return f"{self.name} <{self.email}>"

    @property
    def last_agreement_signature(self):
        """The last agreement that this contributor signed."""
        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from .agreement_signature import AgreementSignature

        return (
            AgreementSignature.objects.filter(contributor=self)
            .order_by("signed_at")
            .last()
        )
