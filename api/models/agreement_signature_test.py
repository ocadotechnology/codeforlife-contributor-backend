"""
© Ocado Group
Created on 09/07/2024 at 11:43:42(+01:00).
"""

from codeforlife.tests import ModelTestCase

from .agreement_signature import AgreementSignature


class TestAgreementSignature(ModelTestCase[AgreementSignature]):
    """Test the AgreementSignature Model"""

    fixtures = ["contributors", "agreement_signatures"]

    def setUp(self):
        self.agreement_signature = AgreementSignature.objects.get(pk=1)

    def test_str(self):
        """
        Parsing an agreement-signature instance to a string
        that returns the contributor's primary key,
        the first 7 characters of the agreement's commit ID
        and the timestamp of when the agreement was signed.
        """
        commit_id = self.agreement_signature.agreement_id[:7]
        time = self.agreement_signature.signed_at
        cont = f"Contributor {self.agreement_signature.contributor.pk} signed"
        repo = f"{commit_id} at {time}"
        expected_str = f"{cont} {repo}"
        assert str(self.agreement_signature) == expected_str
