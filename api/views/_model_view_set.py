"""
© Ocado Group
Created on 13/09/2024 at 12:00:57(+03:00).
"""

import typing as t

from codeforlife.request import BaseRequest
from codeforlife.views import BaseModelViewSet
from django.db.models import Model

from ..models import Contributor
from ..models.session import SessionStore

AnyModel = t.TypeVar("AnyModel", bound=Model)

if t.TYPE_CHECKING:  # pragma: no cover
    from ..serializers._model_serializer import ModelSerializer


# pylint: disable-next=too-many-ancestors
class ModelViewSet(
    BaseModelViewSet[BaseRequest[SessionStore, Contributor], AnyModel],
    t.Generic[AnyModel],
):
    """Base model view set."""

    request_class = BaseRequest[SessionStore, Contributor]
    serializer_class: t.Optional[t.Type["ModelSerializer[AnyModel]"]]
