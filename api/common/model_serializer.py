"""
© Ocado Group
Created on 13/09/2024 at 12:00:41(+03:00).
"""

import typing as t

from codeforlife.types import DataDict
from django.db.models import Model
from rest_framework.serializers import ModelSerializer as _ModelSerializer

from .request import Request

AnyModel = t.TypeVar("AnyModel", bound=Model)


class ModelSerializer(_ModelSerializer[AnyModel], t.Generic[AnyModel]):
    """Base model serializer."""

    @property
    def request(self):
        """The HTTP request that triggered the view."""

        return t.cast(Request, self.context["request"])

    @property
    def view(self):
        """The view that instantiated this serializer."""
        # NOTE: import outside top-level to avoid circular imports.
        # pylint: disable-next=import-outside-toplevel
        from .model_view_set import ModelViewSet

        return t.cast(ModelViewSet[AnyModel], self.context["view"])

    @property
    def non_none_instance(self):
        """Casts the instance to not None."""
        return t.cast(AnyModel, self.instance)

    # pylint: disable-next=useless-parent-delegation
    def update(self, instance: AnyModel, validated_data: DataDict) -> AnyModel:
        return super().update(instance, validated_data)

    # pylint: disable-next=useless-parent-delegation
    def create(self, validated_data: DataDict) -> AnyModel:
        return super().create(validated_data)

    def validate(self, attrs: DataDict):
        return attrs

    # pylint: disable-next=useless-parent-delegation
    def to_representation(self, instance: AnyModel) -> DataDict:
        return super().to_representation(instance)
