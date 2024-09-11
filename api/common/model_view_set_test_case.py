import typing as t

from codeforlife.tests import ModelViewSetClient as _ModelViewSetClient
from codeforlife.tests import ModelViewSetTestCase as _ModelViewSetTestCase
from codeforlife.user.models import User
from django.db.models import Model

from ..models import Contributor
from .model_view_set import ModelViewSet

AnyModel = t.TypeVar("AnyModel", bound=Model)


class ModelViewSetClient(_ModelViewSetClient, t.Generic[AnyModel]):
    def login(self, **credentials):
        # Logout current user (if any) before logging in next user.
        self.logout()

        # TODO: mock api calls
        assert super().login(
            code=""
        ), f"Failed to login with credentials: {credentials}."

        return Contributor.objects.get(session=self.session.session_key)

    def login_as(self, contributor: Contributor):
        pass  # TODO


class ModelViewSetTestCase(_ModelViewSetTestCase, t.Generic[AnyModel]):
    model_view_set_class: t.Type[ModelViewSet[AnyModel]]
    client: ModelViewSetClient[AnyModel]
    client_class: t.Type[ModelViewSetClient[AnyModel]] = ModelViewSetClient

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

    def _get_client_class(self):
        # TODO: unpack type args in index after moving to python 3.11
        # pylint: disable-next=too-few-public-methods
        class _Client(
            self.client_class[self.get_model_class()]  # type: ignore[misc]
        ):
            _test_case = self

        return _Client
