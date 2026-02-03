"""
© Ocado Group
Created on 10/09/2024 at 17:01:39(+03:00).
"""

import typing as t

import requests
from codeforlife.types import JsonDict
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils.translation import gettext_lazy as _
from requests.exceptions import RequestException

from .contributor import Contributor

if t.TYPE_CHECKING:
    from django_stubs_ext.db.models import TypedModelMeta  # pragma: no cover
else:
    TypedModelMeta = object


class ContributorEmail(models.Model):
    """A contributor's verified email address."""

    contributor_id: int
    contributor = models.ForeignKey(
        Contributor,
        on_delete=models.CASCADE,
        related_name="emails",
    )
    objects: models.Manager["ContributorEmail"]

    email = models.EmailField(_("email"), unique=True)
    is_primary = models.BooleanField(_("is primary"))
    is_public = models.BooleanField(_("is public"))

    class Meta(TypedModelMeta):
        verbose_name = _("contributor email")
        verbose_name_plural = _("contributor emails")
        constraints = [
            UniqueConstraint(
                fields=["contributor"],
                condition=Q(is_primary=True),
                name="contributor__is_primary",
            )
        ]

    def __str__(self):
        return self.email

    @staticmethod
    def get_github_emails(auth: str):
        # pylint: disable=line-too-long
        """Get the authenticated GitHub user's emails.

        https://docs.github.com/en/rest/users/emails?apiVersion=2022-11-28#list-email-addresses-for-the-authenticated-user

        Args:
            auth: The auth header used to access the user's data.

        Raises:
            Exception: If API does not respond with an OK status code.

        Returns:
            The authenticated GitHub user's emails.
        """
        # pylint: enable=line-too-long
        response = requests.get(
            url="https://api.github.com/user/emails",
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Authorization": auth,
            },
            params={"per_page": 100},
            timeout=5,
        )

        if not response.ok:
            raise RequestException("Failed to call GitHub API.")

        return t.cast(t.List[JsonDict], response.json())

    @classmethod
    def sync_with_github(cls, contributor: Contributor, auth: str):
        # pylint: disable=line-too-long
        """Sync a contributor's emails with GitHub.

        Args:
            contributor: The contributor to sync.
            auth: The auth header used to access the user's data.

        Returns:
            The synced contributor's emails.
        """
        # pylint: enable=line-too-long
        github_emails = cls.get_github_emails(auth)
        github_emails = [email for email in github_emails if email["verified"]]

        contributor.emails.all().delete()

        return cls.objects.bulk_create(
            [
                cls(
                    contributor=contributor,
                    email=email["email"],
                    is_primary=email["primary"],
                    is_public=email["visibility"] == "public",
                )
                for email in github_emails
            ]
        )
