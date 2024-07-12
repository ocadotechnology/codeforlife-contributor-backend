"""
© Ocado Group
Created on 12/07/2024 at 11:36:23(+01:00).
"""

from codeforlife.tests import ModelSerializerTestCase
from codeforlife.user.models import User

from ..models import Contributor
from .contributor import ContributorSerializer


class TestContributorSerializer(ModelSerializerTestCase[User, Contributor]):
    """Test the functionality of the serializers"""

    model_serializer_class = ContributorSerializer

    def setUp(self):
        self.data1 = {
            "id": 1,
            "email": "cont1@gmail.com",
            "name": "Cont One",
            "location": "London",
            "html_url": "http://github.com/cont1",
            "avatar_url": "https://testcont.github.io/gravatar-url-generator/",
        }

        self.data2 = {
            "id": 2,
            "email": "cont2@gmail.com",
            "name": "Cont Two",
            "location": "London",
            "html_url": "http://github.com/cont2",
            "avatar_url": "https://cont2.github.io/gravatar-url-generator/",
        }

    def test_create(self):
        """Create a contributor"""
        self.assert_create(validated_data=self.data1, new_data=self.data1)

    def test_create_list(self):
        """List all contributor"""
        # expected = [self.data1, self.data2]
        self.assert_create(validated_data=self.data1, new_data=self.data1)
        self.assert_create(validated_data=self.data2, new_data=self.data2)
