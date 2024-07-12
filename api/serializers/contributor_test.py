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
        """Set up data to be used for testing"""
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
        # Create multiple Contributors
        self.assert_create(validated_data=self.data1, new_data=self.data1)
        self.assert_create(validated_data=self.data2, new_data=self.data2)

        # Compare results
        queryset = Contributor.objects.all()
        assert len(queryset) == 2

    def test_get_first(self):
        """Retrieve the first object"""
        # Create multiple Contributors
        self.assert_create(validated_data=self.data1, new_data=self.data1)
        self.assert_create(validated_data=self.data2, new_data=self.data2)

        # Retrieve the first and compare
        cont = Contributor.objects.first()
        serializer = ContributorSerializer(cont)
        assert serializer.data["id"] == self.data1["id"]

    def test_get_any(self):
        """ " Retrieve any object using its id"""
        # Create multiple Contributors
        self.assert_create(validated_data=self.data1, new_data=self.data1)
        self.assert_create(validated_data=self.data2, new_data=self.data2)

        # Retrieve by id and compare
        cont = Contributor.objects.get(id=2)
        serializer = ContributorSerializer(cont)
        assert serializer.data["id"] == self.data2["id"]

    def test_update(self):
        """Updating a single contributor"""
        # Create a new contributor
        cont = Contributor.objects.create(
            id=1,
            email="cont1@gmail.com",
            name="Cont One",
            location="London",
            html_url="http://github.com/cont1",
            avatar_url="https://testcont.github.io/gravatar-url-generator/",
        )

        # Expected Results
        new_data = {"email": "new_email@gmail.com", "name": "New Name"}
        expected = {
            "id": 1,
            "email": "new_email@gmail.com",
            "name": "New Name",
            "location": "London",
            "html_url": "http://github.com/cont1",
            "avatar_url": "https://testcont.github.io/gravatar-url-generator/",
        }
        self.assert_update(
            instance=cont, validated_data=new_data, new_data=expected
        )
