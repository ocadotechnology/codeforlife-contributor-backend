"""
© Ocado Group
Created on 08/07/2024 at 10:48:44(+01:00).
"""

from django.db import models

from .contributor import Contributor


class AgreementSignature(models.Model):
    """Signature of a contributor signing the agreement"""

    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    agreement_id = models.CharField(max_length=40)
    signed_at = models.DateTimeField()

    class Meta:
        unique_together = ["contributor", "agreement_id"]
        verbose_name = "agreement_signature"
        verbose_name_plural = "agreement_signatures"

    def __str__(self):
        cont = f"Contributor {self.contributor} signed"
        repo = f"{self.agreement_id[:7]} at {self.signed_at}"
        return f"{cont} {repo}"
