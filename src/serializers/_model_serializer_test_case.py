"""
© Ocado Group
Created on 13/09/2024 at 12:00:34(+03:00).
"""

import typing as t

from codeforlife.tests import BaseAPIRequestFactory, BaseModelSerializerTestCase
from django.db.models import Model

from ..models import Contributor
from ..request import Request
from ._model_serializer import ModelSerializer

AnyModel = t.TypeVar("AnyModel", bound=Model)


class ModelSerializerTestCase(
    # pylint: disable=duplicate-code
    BaseModelSerializerTestCase[
        ModelSerializer[AnyModel],
        BaseAPIRequestFactory[Request, Contributor],
        AnyModel,
    ],
    t.Generic[AnyModel],
    # pylint: enable=duplicate-code
):
    """Base model serializer test case."""

    request_factory_class = BaseAPIRequestFactory
