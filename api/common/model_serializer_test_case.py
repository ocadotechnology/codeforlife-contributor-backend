"""
© Ocado Group
Created on 13/09/2024 at 12:00:34(+03:00).
"""

import typing as t

from codeforlife.request import BaseRequest
from codeforlife.tests import BaseAPIRequestFactory
from codeforlife.tests import (
    ModelSerializerTestCase as _ModelSerializerTestCase,
)
from django.db.models import Model

from ..models import Contributor
from ..models.session import SessionStore
from .model_serializer import ModelSerializer

AnyModel = t.TypeVar("AnyModel", bound=Model)


class ModelSerializerTestCase(_ModelSerializerTestCase, t.Generic[AnyModel]):
    """Base model serializer test case."""

    model_serializer_class: t.Type[  # type: ignore[assignment]
        ModelSerializer[AnyModel]
    ]

    request_factory: BaseAPIRequestFactory[  # type: ignore[assignment]
        BaseRequest[SessionStore, Contributor], Contributor
    ]

    @classmethod
    def setUpClass(cls):
        result = super().setUpClass()

        cls.request_factory = BaseAPIRequestFactory[
            BaseRequest[SessionStore, Contributor], Contributor
        ]()

        return result

    @classmethod
    def get_request_user_class(cls) -> t.Type[AnyModel]:
        """Get the model view set's class.

        Returns:
            The model view set's class.
        """
        return Contributor  # type: ignore[return-value]

    @classmethod
    def get_model_class(cls) -> t.Type[AnyModel]:
        """Get the model view set's class.

        Returns:
            The model view set's class.
        """
        # pylint: disable-next=no-member
        return t.get_args(cls.__orig_bases__[0])[  # type: ignore[attr-defined]
            0
        ]
