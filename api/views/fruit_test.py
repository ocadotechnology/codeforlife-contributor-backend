"""
© Ocado Group
Created on 02/07/2024 at 16:38:57(+01:00).
"""

from codeforlife.tests import ModelViewSetTestCase
from codeforlife.user.models import User

from ..models import Fruit
from .fruit import FruitViewSet


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class TestFruitViewSet(ModelViewSetTestCase[User, Fruit]):
    basename = "fruit"
    model_view_set_class = FruitViewSet
    fixtures = ["fruits"]

    def setUp(self):
        self.apple = Fruit.objects.get(name="apple")
        self.banana = Fruit.objects.get(name="banana")
        self.orange = Fruit.objects.get(name="orange")

    def test_list(self):
        """Can list all fruits."""
        self.client.list(models=[self.apple, self.banana, self.orange])

    def test_retrieve(self):
        """Can retrieve a single fruit."""
        self.client.retrieve(model=self.apple)

    def test_create(self):
        """Can create a fruit."""
        self.client.create(data={"name": "kiwi", "is_citrus": False})
