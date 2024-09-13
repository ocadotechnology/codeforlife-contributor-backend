import typing as t

from codeforlife.tests import (
    ModelSerializerTestCase as _ModelSerializerTestCase,
)
from django.db.models import Model

from ..models import Contributor
from .api_request_factory import APIRequestFactory
from .model_serializer import ModelSerializer

AnyModel = t.TypeVar("AnyModel", bound=Model)


class ModelSerializerTestCase(_ModelSerializerTestCase, t.Generic[AnyModel]):
    model_serializer_class: t.Type[  # type: ignore[assignment]
        ModelSerializer[AnyModel]
    ]

    request_factory: APIRequestFactory  # type: ignore[assignment]

    @classmethod
    def setUpClass(cls):
        result = super().setUpClass()

        cls.request_factory = APIRequestFactory()

        return result

    @classmethod
    def get_request_user_class(cls) -> t.Type[AnyModel]:
        """Get the model view set's class.

        Returns:
            The model view set's class.
        """
        return Contributor # type: ignore[return-value]

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
