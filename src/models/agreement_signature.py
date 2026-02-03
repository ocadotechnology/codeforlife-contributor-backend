"""
© Ocado Group
Created on 08/07/2024 at 10:48:44(+01:00).
"""

import typing as t

import requests
from codeforlife.types import DataDict
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from requests.exceptions import RequestException

from .contributor import Contributor

if t.TYPE_CHECKING:
    from django_stubs_ext.db.models import TypedModelMeta  # pragma: no cover
else:
    TypedModelMeta = object


class AgreementSignature(models.Model):
    """Signature of a contributor signing the agreement"""

    contributor_id: int
    contributor = models.ForeignKey(
        Contributor,
        on_delete=models.CASCADE,
        related_name="agreement_signatures",
    )
    objects: models.Manager["AgreementSignature"]

    agreement_id = models.CharField(
        _("agreement id"),
        max_length=40,
        help_text=_("Commit ID of the contribution agreement in workspace."),
        validators=[MinLengthValidator(40)],
    )
    signed_at = models.DateTimeField(_("signed at"))

    class Meta(TypedModelMeta):
        unique_together = ["contributor", "agreement_id"]
        verbose_name = _("agreement signature")
        verbose_name_plural = _("agreement signatures")

    def __str__(self):
        cont = f"Contributor {self.contributor_id} signed"
        repo = f"{self.agreement_id[:7]} at {self.signed_at}"
        return f"{cont} {repo}"

    @staticmethod
    def get_latest_sha_from_github():
        """Get the latest agreement's commit's SHA from GitHub."""
        response = requests.get(
            # pylint: disable-next=line-too-long
            url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits",
            headers={"X-GitHub-Api-Version": "2022-11-28"},
            params=t.cast(DataDict, {"path": settings.GH_FILE, "per_page": 1}),
            timeout=5,
        )

        if not response.ok:
            raise RequestException("Failed to call GitHub API.")

        return t.cast(str, response.json()[0]["sha"])
