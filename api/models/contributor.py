"""
© Ocado Group
Created on 05/07/2024 at 16:18:48(+01:00).
"""

import typing as t

import requests
from codeforlife.types import JsonDict
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

if t.TYPE_CHECKING:
    from django_stubs_ext.db.models import TypedModelMeta  # pragma: no cover

    from .agreement_signature import AgreementSignature
    from .contributor_email import ContributorEmail
    from .repository import Repository
    from .session import Session
else:
    TypedModelMeta = object


class Contributor(models.Model):
    """A contributor that contributes to a repo"""

    agreement_signatures: QuerySet["AgreementSignature"]
    emails: QuerySet["ContributorEmail"]
    repositories: QuerySet["Repository"]
    session: "Session"

    is_active = True

    pk: int
    id = models.IntegerField(
        primary_key=True, help_text=_("The contributor's GitHub user-ID.")
    )
    name = models.TextField(_("name"))
    location = models.TextField(_("location"), null=True)
    html_url = models.TextField(_("html url"))
    avatar_url = models.TextField(_("avatar url"))
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    class Meta(TypedModelMeta):
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")

    def __str__(self):
        primary_email = self.primary_email
        return f"{self.name} <{primary_email}>" if primary_email else self.name

    @property
    def primary_email(self):
        """The primary email of this contributor, if they have one."""
        from .contributor_email import ContributorEmail

        try:
            return self.emails.get(is_primary=True).email
        except ContributorEmail.DoesNotExist:
            return None

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

    @staticmethod
    def get_github_user(auth: str):
        # pylint: disable=line-too-long
        """Get the authenticated GitHub user.

        https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#get-the-authenticated-user

        Args:
            auth: The auth header used to access the user's data.

        Raises:
            Exception: If API does not respond with an OK status code.

        Returns:
            The authenticated GitHub user
        """
        # pylint: enable=line-too-long
        response = requests.get(
            url="https://api.github.com/user",
            headers={
                "Accept": "application/json",
                "X-GitHub-Api-Version": "2022-11-28",
                # pylint: disable-next=line-too-long
                "Authorization": auth,
            },
            timeout=5,
        )

        if not response.ok:
            raise Exception("Failed to call GitHub API.")

        return t.cast(JsonDict, response.json())

    def sync_with_github(
        self, auth: str, github_user: t.Optional[JsonDict] = None
    ):
        # pylint: disable=line-too-long
        """Sync a contributor with GitHub.

        Args:
            auth: The auth header used to access the user's data.
            github_user: The github-user to sync. If not provided, it will be retrieved from GitHub.
        """
        # pylint: enable=line-too-long
        from .contributor_email import ContributorEmail

        github_user = github_user or self.get_github_user(auth)

        self.name = github_user["name"]
        self.location = github_user.get("location")
        self.html_url = github_user["html_url"]
        self.avatar_url = github_user["avatar_url"]
        self.save()

        ContributorEmail.sync_with_github(self, auth)
