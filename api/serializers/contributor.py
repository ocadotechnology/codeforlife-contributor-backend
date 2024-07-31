"""
© Ocado Group
Created on 12/07/2024 at 14:07:59(+01:00).
"""

import typing as t

from codeforlife.serializers import ModelSerializer
from codeforlife.user.models import User

from ..models import Contributor


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class ContributorSerializer(ModelSerializer[User, Contributor]):
    class Meta:
        model = Contributor
        fields = ["id", "email", "name", "location", "html_url", "avatar_url"]
        extra_kwargs: t.Dict[str, t.Dict[str, t.Any]] = {
            "id": {"validators": []}
        }

    def create(self, validated_data):
        try:
            # Update an existing contributor
            contributor = Contributor.objects.get(id=validated_data["id"])
            contributor.email = validated_data["email"]
            contributor.name = validated_data["name"]
            contributor.location = validated_data["location"]
            contributor.html_url = validated_data["html_url"]
            contributor.avatar_url = validated_data["avatar_url"]

            contributor.save(
                update_fields=[
                    "email",
                    "name",
                    "location",
                    "html_url",
                    "avatar_url",
                ]
            )
        except Contributor.DoesNotExist:
            # Create a new contributor
            contributor = Contributor.objects.create(**validated_data)

        return contributor
