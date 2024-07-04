"""
© Ocado Group
Created on 02/07/2024 at 16:17:04(+01:00).
"""

from codeforlife.tests import ModelTestCase

from .fruit import Fruit


# pylint: disable-next=missing-class-docstring
class TestFruit(ModelTestCase[Fruit]):
    fixtures = ["fruits"]

    def setUp(self):
        self.apple = Fruit.objects.get(name="apple")
        self.banana = Fruit.objects.get(name="banana")

    def test_str(self):
        """Parsing a fruit object instance to string returns its name."""
        assert str(self.apple) == self.apple.name

    def test_lt(self):
        """
        Comparing if one fruit is less than another compares their expiry dates.
        """
        assert self.apple < self.banana
        assert not self.banana < self.apple
