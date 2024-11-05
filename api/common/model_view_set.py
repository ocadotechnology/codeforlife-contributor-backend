"""
© Ocado Group
Created on 13/09/2024 at 12:00:57(+03:00).
"""

import typing as t

from codeforlife.request import BaseRequest
from django.db.models import Model
from rest_framework.viewsets import ModelViewSet as _ModelViewSet

from ..models import Contributor
from ..models.session import SessionStore

AnyModel = t.TypeVar("AnyModel", bound=Model)

if t.TYPE_CHECKING:  # pragma: no cover
    from .model_serializer import ModelSerializer

    # NOTE: This raises an error during runtime.
    # pylint: disable-next=too-few-public-methods,invalid-name
    class __ModelViewSet(_ModelViewSet[AnyModel], t.Generic[AnyModel]):
        pass

else:
    # pylint: disable-next=too-many-ancestors,invalid-name
    class __ModelViewSet(_ModelViewSet, t.Generic[AnyModel]):
        pass


# pylint: disable-next=too-many-ancestors
class ModelViewSet(__ModelViewSet[AnyModel], t.Generic[AnyModel]):
    """Base model view set."""

    request: BaseRequest[SessionStore, Contributor]
    serializer_class: t.Optional[t.Type["ModelSerializer[AnyModel]"]]

    def initialize_request(self, request, *args, **kwargs):
        # NOTE: Call to super has side effects and is required.
        super().initialize_request(request, *args, **kwargs)

        return BaseRequest[SessionStore, Contributor](
            request=request,
            parsers=self.get_parsers(),
            authenticators=self.get_authenticators(),
            negotiator=self.get_content_negotiator(),
            parser_context=self.get_parser_context(request),
        )
