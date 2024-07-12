from codeforlife.serializers import ModelSerializer
from codeforlife.user.models import User

from ..models import AgreementSignature


class AgreementSignatureSerializer(ModelSerializer[User, AgreementSignature]):
    """ """

    class Meta:
        model = AgreementSignature
        fields = "__all__"
