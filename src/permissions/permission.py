"""
© Ocado Group
Created on 19/06/2025 at 11:30:00(+00:00).
"""

import typing as t

from codeforlife.permissions import BasePermission
from codeforlife.tests import TestCase
from codeforlife.tests.api_request_factory import BaseAPIRequestFactory
from rest_framework.request import Request
from rest_framework.views import APIView


class PermissionTestCase(TestCase):
    """Base test case for all permission test cases to inherit."""

    permission_class: t.Type[BasePermission]
    request_factory: BaseAPIRequestFactory = BaseAPIRequestFactory()

    REQUIRED_ATTRS: t.Set[str] = {"permission_class"}

    @classmethod
    def setUpClass(cls):
        for attr in cls.REQUIRED_ATTRS:
            assert hasattr(cls, attr), f'Attribute "{attr}" must be set.'

        return super().setUpClass()

    def assert_has_permission(
        self,
        has_permission: bool,
        request: Request,
        *args,
        view: APIView = APIView(),
        **kwargs,
    ):
        # pylint: disable=line-too-long
        """Assert whether or not the request has permission to call the view.

        Args:
            has_permission: A flag designating whether the request has permission.
            request: The request to grant permission to.
            view: The view to grant permission to.
        """
        # pylint: enable=line-too-long
        permission = self.permission_class(*args, **kwargs)
        assert has_permission == permission.has_permission(request, view)
