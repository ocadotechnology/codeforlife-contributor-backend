"""
© Ocado Group
Created on 13/09/2024 at 12:00:34(+03:00).
"""

import typing as t

from codeforlife.request import BaseRequest
from codeforlife.tests import (
    BaseAPIRequestFactory,
    BaseModelListSerializerTestCase,
    BaseModelSerializerTestCase,
)
from django.db.models import Model

from ..models import Contributor
from ..models.session import SessionStore
from .model_serializer import ModelListSerializer, ModelSerializer

AnyModel = t.TypeVar("AnyModel", bound=Model)


class ModelSerializerTestCase(
    BaseModelSerializerTestCase[
        ModelSerializer[AnyModel],
        BaseAPIRequestFactory[
            BaseRequest[SessionStore, Contributor], Contributor
        ],
        AnyModel,
    ],
    t.Generic[AnyModel],
):
    """Base model serializer test case."""

    request_factory_class = BaseAPIRequestFactory


# pylint: disable-next=too-many-ancestors
class ModelListSerializerTestCase(
    BaseModelListSerializerTestCase[
        ModelListSerializer[AnyModel],
        ModelSerializer[AnyModel],
        BaseAPIRequestFactory[
            BaseRequest[SessionStore, Contributor], Contributor
        ],
        AnyModel,
    ],
    t.Generic[AnyModel],
):
    """Base model serializer test case."""

    request_factory_class = BaseAPIRequestFactory
