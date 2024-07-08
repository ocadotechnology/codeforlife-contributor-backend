"""
© Ocado Group
Created on 08/07/2024 at 10:48:44(+01:00).

"""
import typing as t

from django.db import models
from django.utils.translation import gettext_lazy as _
from .contributor import Contributor

if t.TYPE_CHECKING:
    from django_stubs_ext.db.models import TypedModelMeta
else:
    TypedModelMeta = object



class AgreementSignature(models.Model):
    """ Signature of a contributor signing the agreement """
    id = models.AutoField(primary_key=True)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    agreement_id = models.CharField(max_length=40)
    signed_at = models.DateTimeField()

    def __str__(self):
        return self.id
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["contributor", "agreement_id"], name='unique_contributor_agreement')
        ]