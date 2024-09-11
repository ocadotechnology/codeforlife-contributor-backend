import typing as t

from django.db.models import Model
from rest_framework.viewsets import ModelViewSet as _ModelViewSet

from .request import Request

AnyModel = t.TypeVar("AnyModel", bound=Model)

if t.TYPE_CHECKING:  # pragma: no cover
    from .model_serializer import ModelSerializer

    # NOTE: This raises an error during runtime.
    # pylint: disable-next=too-few-public-methods
    class __ModelViewSet(_ModelViewSet[AnyModel], t.Generic[AnyModel]):
        pass

else:
    # pylint: disable-next=too-many-ancestors
    class __ModelViewSet(_ModelViewSet, t.Generic[AnyModel]):
        pass


class ModelViewSet(__ModelViewSet[AnyModel], t.Generic[AnyModel]):
    request: Request
    serializer_class: t.Optional[t.Type["ModelSerializer[AnyModel]"]]

    def initialize_request(self, request, *args, **kwargs):
        # NOTE: Call to super has side effects and is required.
        super().initialize_request(request, *args, **kwargs)

        return Request(
            request=request,
            parsers=self.get_parsers(),
            authenticators=self.get_authenticators(),
            negotiator=self.get_content_negotiator(),
            parser_context=self.get_parser_context(request),
        )
