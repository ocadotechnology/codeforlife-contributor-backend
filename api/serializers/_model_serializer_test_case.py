"""
© Ocado Group
Created on 13/09/2024 at 12:00:34(+03:00).
"""

import typing as t

from codeforlife.request import BaseRequest
from codeforlife.tests import BaseAPIRequestFactory, BaseModelSerializerTestCase
from django.db.models import Model

from ..models import Contributor
from ..models.session import SessionStore
from ._model_serializer import ModelSerializer

AnyModel = t.TypeVar("AnyModel", bound=Model)


class ModelSerializerTestCase(
    # pylint: disable=duplicate-code
    BaseModelSerializerTestCase[
        ModelSerializer[AnyModel],
        BaseAPIRequestFactory[
            BaseRequest[SessionStore, Contributor], Contributor
        ],
        AnyModel,
    ],
    t.Generic[AnyModel],
    # pylint: enable=duplicate-code
):
    """Base model serializer test case."""

    request_factory_class = BaseAPIRequestFactory
