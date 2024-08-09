"""
© Ocado Group
Created on 08/08/2024 at 15:46:09(+01:00).
"""

from codeforlife.tests import TestCase

from ...models import Contributor
from .github import GitHubBackend


# pylint: disable-next=missing-class-docstring,
class GitHubBackendTest(TestCase):
    fixtures = ["contributors"]

    def setUp(self):
        # Set up initial test data
        self.contributor1 = Contributor.objects.get(id=1)
        self.backend = GitHubBackend()

    def test_get_user__existing_user(self):
        """Can get the existing user"""
        contributor = self.backend.get_user(contributor_id=1)
        assert contributor == self.contributor1

    def test_get_user__non_existing_user(self):
        """Can check if the user does not exist"""
        contributor = self.backend.get_user(contributor_id=999)
        assert not contributor
