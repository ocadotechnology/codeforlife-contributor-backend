"""
© Ocado Group
Created on 13/09/2024 at 12:00:41(+03:00).
"""

import typing as t

from codeforlife.serializers import BaseModelSerializer
from django.db.models import Model

from ..request import Request

AnyModel = t.TypeVar("AnyModel", bound=Model)

if t.TYPE_CHECKING:  # pragma: no cover
    from ..views._model_view_set import ModelViewSet


class ModelSerializer(
    BaseModelSerializer[Request, "ModelViewSet[AnyModel]", AnyModel],
    t.Generic[AnyModel],
):
    """Base model serializer."""
