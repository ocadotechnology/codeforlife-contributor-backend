"""
© Ocado Group
Created on 08/07/2024 at 10:48:44(+01:00).
"""

import typing as t

from django.db import models
from .contributor import Contributor
from django.utils.translation import gettext_lazy as _

if t.TYPE_CHECKING:
    from django_stubs_ext.db.models import TypedModelMeta # pragma: no cover
else:
    TypedModelMeta = object



class AgreementSignature(models.Model):
    """Signature of a contributor signing the agreement"""

    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    agreement_id = models.CharField(max_length=40)
    signed_at = models.DateTimeField()

    class Meta(TypedModelMeta):
        unique_together = ["contributor", "agreement_id"]
        verbose_name = _("agreement_signature")
        verbose_name_plural = _("agreement_signatures")

    def __str__(self):
        cont = f"Contributor {self.contributor} signed"
        repo = f"{self.agreement_id[:7]} at {self.signed_at}"
        return f"{cont} {repo}"
