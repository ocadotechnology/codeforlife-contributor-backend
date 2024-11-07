"""
© Ocado Group
Created on 13/09/2024 at 12:00:41(+03:00).
"""

import typing as t

from codeforlife.request import BaseRequest
from codeforlife.serializers import BaseModelListSerializer
from django.db.models import Model

from ..models import Contributor
from ..models.session import SessionStore

AnyModel = t.TypeVar("AnyModel", bound=Model)


class ModelListSerializer(
    BaseModelListSerializer[BaseRequest[SessionStore, Contributor], AnyModel],
    t.Generic[AnyModel],
):
    """Base model list serializer."""
