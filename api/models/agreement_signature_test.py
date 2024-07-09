"""
© Ocado Group
Created on 09/07/2024 at 11:43:42(+01:00).
"""

from codeforlife.tests import ModelTestCase

from .agreement_signature import AgreementSignature

# from .contributor import Contributor

# from .repository import Repository


class TestAgreementSignature(ModelTestCase[AgreementSignature]):
    """Test the AgreementSignature Model"""

    fixtures = ["agreement_signatures", "contributors"]

    def setUp(self):
        self.agreement_signature = AgreementSignature.objects.get(pk=1)

    # def test_str(self):
    #     """Parsing a contributor object instance to returns its name."""
    #     commit_id = self.agreement_signature.agreement_id[:7]
    #     # time = self.agreement_signature.signed_at
    #     # contributor = self.agreement_signature.contributor.name
    #     # cont = f"Contributor {contributor} signed"
    #     # repo = f"{commit_id} at {time}"
    #     assert commit_id in str(self.agreement_signature)

    # def test_str(self):
    #     assert str(self.agreement_signature) ==
    # self.agreement_signature.agreement_id
