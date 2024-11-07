"""
© Ocado Group
Created on 13/09/2024 at 12:00:50(+03:00).
"""

# pylint: disable=duplicate-code

import typing as t

from codeforlife.tests import BaseModelViewSetTestCase
from django.db.models import Model

from ._model_view_set import ModelViewSet
from ._model_view_set_client import ModelViewSetClient

AnyModel = t.TypeVar("AnyModel", bound=Model)


# pylint: disable-next=too-many-ancestors
class ModelViewSetTestCase(
    BaseModelViewSetTestCase[
        ModelViewSet[AnyModel],
        ModelViewSetClient[AnyModel],
        AnyModel,
    ],
    t.Generic[AnyModel],
):
    """Base model view set test case."""

    client_class = ModelViewSetClient

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
