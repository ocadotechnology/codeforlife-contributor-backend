"""
© Ocado Group
Created on 15/07/2024 at 12:52:50(+01:00).
"""

from codeforlife.response import Response
from codeforlife.views import action

from ..models import AgreementSignature
from ..serializers import AgreementSignatureSerializer
from ._model_view_set import ModelViewSet


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class AgreementSignatureViewSet(ModelViewSet[AgreementSignature]):
    http_method_names = ["get", "post"]
    serializer_class = AgreementSignatureSerializer

    def get_queryset(self):
        return AgreementSignature.objects.filter(
            contributor=self.request.auth_user
        ).order_by("signed_at")

    @action(detail=False, methods=["get"])
    # pylint: disable-next=unused-argument
    def check_signed_latest(self, _):
        """Check if a contributor has signed the latest agreement."""
        latest_commit_id = AgreementSignature.get_latest_sha_from_github()
        last_signature = self.get_queryset().last()

        is_signed, reason = True, ""
        if not last_signature:
            is_signed, reason = False, "no_agreement_signatures"
        elif latest_commit_id != last_signature.agreement_id:
            is_signed, reason = False, "old_agreement_signatures"

        return Response(
            {
                "latest_commit_id": latest_commit_id,
                "is_signed": is_signed,
                "reason": reason,
            }
        )
