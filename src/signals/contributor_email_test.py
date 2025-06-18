"""
© Ocado Group
Created on 10/09/2024 at 17:01:39(+03:00).
"""

from django.test import TestCase

from ..models import ContributorEmail

# pylint: disable=unused-argument


# pylint: disable-next=missing-class-docstring
class TestContributorEmail(TestCase):
    fixtures = ["contributors"]

    def test_pre_save__email(self):
        """Creating or updating a contributor-email lowers the email."""
        email = "EXAMPLE1@GMAIL.COM"
        contributor_email = ContributorEmail.objects.create(
            contributor_id=1, email=email, is_primary=False, is_public=True
        )
        assert contributor_email.email == email.lower()

        email = "EXAMPLE2@GMAIL.COM"
        contributor_email.email = email
        contributor_email.save()
        assert contributor_email.email == email.lower()

        email = "EXAMPLE3@GMAIL.COM"
        contributor_email.email = email
        contributor_email.save(update_fields=["email"])
        assert contributor_email.email == email.lower()
