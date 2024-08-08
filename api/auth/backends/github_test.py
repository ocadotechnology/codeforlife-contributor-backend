"""
© Ocado Group
Created on 08/08/2024 at 15:46:09(+01:00).
"""

from django.test import TestCase

from ...models import Contributor
from .github import GithubBackend


# pylint: disable-next=missing-class-docstring,
class GithubBackendTest(TestCase):
    def setUp(self):
        # Set up initial test data
        self.contributor = Contributor.objects.create(
            id=10,
            email="contributor@example.com",
            name="Test contributor",
            location="Location",
            html_url="http://contributor.com/testuser",
            avatar_url="http://contributor.com/avatar.jpg",
        )
        self.auth = GithubBackend()

    def test_get_user__existing_user(self):
        """Can get the existing user"""
        user = self.auth.get_user(user_id=10)
        assert user == self.contributor

    def test_get_user__non_existing_user(self):
        """Can check if the user does not exist"""
        user = self.auth.get_user(user_id=2)
        assert not user
