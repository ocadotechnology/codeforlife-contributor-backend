"""
© Ocado Group
Created on 15/07/2024 at 12:52:50(+01:00).
"""

from codeforlife.permissions import AllowNone
from codeforlife.response import Response
from codeforlife.views import action

from ..models import ContributorEmail
from ..permissions import HasGitHubOidcToken
from ..request import Request
from ..serializers import ContributorEmailCheckSignedLatestAgreementSerializer
from ._model_view_set import ModelViewSet


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class ContributorEmailViewSet(ModelViewSet[ContributorEmail]):
    http_method_names = ["post"]
    model_class = ContributorEmail

    def get_permissions(self):
        if self.action == "check_signed_latest_agreement":
            return [HasGitHubOidcToken()]

        return [AllowNone()]

    def get_serializer_class(self):
        if self.action == "check_signed_latest_agreement":
            return ContributorEmailCheckSignedLatestAgreementSerializer

        raise NotImplementedError()

    @action(detail=False, methods=["post"])
    # pylint: disable-next=unused-argument
    def check_signed_latest_agreement(self, request: Request):
        """Check if a list of emails have signed the latest agreement."""
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
