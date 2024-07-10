"""
© Ocado Group
Created on 09/07/2024 at 11:43:42(+01:00).
"""

from codeforlife.tests import ModelTestCase
from django.db import IntegrityError

from .agreement_signature import AgreementSignature
from .contributor import Contributor


class TestAgreementSignature(ModelTestCase[AgreementSignature]):
    """Test the AgreementSignature Model"""

    fixtures = ["contributors", "agreement_signatures"]

    def setUp(self):
        self.agreement_signature = AgreementSignature.objects.get(pk=1)
        self.contributor1 = Contributor.objects.get(pk=111111)

    def test_str(self):
        """Parsing a contributor object instance to returns its name."""
        commit_id = self.agreement_signature.agreement_id[:7]
        time = self.agreement_signature.signed_at
        cont = f"Contributor {self.agreement_signature.contributor} signed"
        repo = f"{commit_id} at {time}"
        expected_str = f"{cont} {repo}"
        assert str(self.agreement_signature) == expected_str

    def test_unique_fields(self):
        """Test the unique fields functionality"""
        new_contributor = Contributor.objects.create(
            id=738237,
            email="newcontributor@gmail.com",
            name="new contributor",
            location="london",
            html_url="https://github.com/newcontributor",
            avatar_url="https://contributornew.github.io/",
        )
        AgreementSignature.objects.create(
            contributor=new_contributor,
            agreement_id="g3d3d3s8dg2342c37",
            signed_at="2024-01-02T12:00:00Z",
        )

        with self.assertRaises(IntegrityError):
            AgreementSignature.objects.create(
                contributor=self.contributor1,
                agreement_id="g3d3d3s8dgd3vc37",
                signed_at="2024-01-02T12:00:00Z",
            )
