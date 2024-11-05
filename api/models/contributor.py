"""
© Ocado Group
Created on 05/07/2024 at 16:18:48(+01:00).
"""

import sys
import typing as t

import requests
from codeforlife.types import JsonDict
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from requests.exceptions import RequestException

if t.TYPE_CHECKING:
    from django_stubs_ext.db.models import TypedModelMeta  # pragma: no cover

    from .agreement_signature import AgreementSignature
    from .contributor_email import ContributorEmail
    from .repository import Repository
    from .session import Session
else:
    TypedModelMeta = object


class Contributor(AbstractBaseUser):
    """A contributor that contributes to a repo"""

    USERNAME_FIELD = "id"

    agreement_signatures: QuerySet["AgreementSignature"]
    emails: QuerySet["ContributorEmail"]
    repositories: QuerySet["Repository"]
    session: "Session"

    # Contributors log in with their GitHub account.
    password = None  # type: ignore[assignment]

    pk: int
    id = models.IntegerField(
        primary_key=True, help_text=_("The contributor's GitHub user-ID.")
    )
    name = models.TextField(_("name"))
    location = models.TextField(_("location"), null=True)
    html_url = models.TextField(_("html url"))
    avatar_url = models.TextField(_("avatar url"))

    class Meta(TypedModelMeta):
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")

    def __str__(self):
        return f"{self.name} <{self.primary_email}>"

    @property
    def is_authenticated(self):
        """A flag designating if this contributor has authenticated."""
        # pylint: disable-next=import-outside-toplevel
        from .session import Session

        # Avoid initial migration error where session table is not created yet
        if (
            sys.argv
            and "manage.py" in sys.argv[0]
            and "runserver" not in sys.argv
        ):
            return True

        return Session.objects.filter(
            contributor=self,
            expire_date__gt=timezone.now(),
        ).exists()

    @property
    def primary_email(self):
        """The primary email of this contributor, if they have one."""
        # pylint: disable-next=import-outside-toplevel
        from .contributor_email import ContributorEmail

        try:
            return self.emails.get(is_primary=True)
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
                "Authorization": auth,
            },
            timeout=5,
        )

        if not response.ok:
            raise RequestException("Failed to call GitHub API.")

        return t.cast(JsonDict, response.json())

    @classmethod
    def sync_with_github(cls, auth: str):
        # pylint: disable=line-too-long
        """Sync a contributor with GitHub.

        Args:
            auth: The auth header used to access the user's data.

        Returns:
            The synced contributor.
        """
        # pylint: enable=line-too-long
        # pylint: disable-next=import-outside-toplevel
        from .contributor_email import ContributorEmail

        github_user = cls.get_github_user(auth)

        try:
            contributor = Contributor.objects.get(id=github_user["id"])
        except Contributor.DoesNotExist:
            contributor = Contributor(id=github_user["id"])

        contributor.name = github_user["name"]
        contributor.location = github_user.get("location")
        contributor.html_url = github_user["html_url"]
        contributor.avatar_url = github_user["avatar_url"]
        contributor.save()

        ContributorEmail.sync_with_github(contributor, auth)

        return contributor
