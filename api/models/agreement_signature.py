"""
© Ocado Group
Created on 08/07/2024 at 10:48:44(+01:00).
"""

import typing as t

from django.db import models
from django.utils.translation import gettext_lazy as _

from .contributor import Contributor

if t.TYPE_CHECKING:
    from django_stubs_ext.db.models import TypedModelMeta  # pragma: no cover
else:
    TypedModelMeta = object


class AgreementSignature(models.Model):
    """Signature of a contributor signing the agreement"""

    contributor_id: int
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)

    agreement_id = models.CharField(_("agreement id"), max_length=40)
    signed_at = models.DateTimeField(_("signed at"))

    class Meta(TypedModelMeta):
        unique_together = ["contributor", "agreement_id"]
        verbose_name = _("agreement signature")
        verbose_name_plural = _("agreement signatures")

    def __str__(self):
        cont = f"Contributor {self.contributor} signed"
        repo = f"{self.agreement_id[:7]} at {self.signed_at}"
        return f"{cont} {repo}"
