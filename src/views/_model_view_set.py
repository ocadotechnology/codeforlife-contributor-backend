"""
© Ocado Group
Created on 13/09/2024 at 12:00:57(+03:00).
"""

import typing as t

from codeforlife.views import BaseModelViewSet
from django.db.models import Model

from ..request import Request

AnyModel = t.TypeVar("AnyModel", bound=Model)

if t.TYPE_CHECKING:  # pragma: no cover
    from ..serializers._model_serializer import ModelSerializer


# pylint: disable-next=too-many-ancestors
class ModelViewSet(
    BaseModelViewSet[Request, "ModelSerializer[AnyModel]", AnyModel],
    t.Generic[AnyModel],
):
    """Base model view set."""

    request_class = Request
