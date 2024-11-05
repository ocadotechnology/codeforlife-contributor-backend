"""
© Ocado Group
Created on 13/09/2024 at 12:00:25(+03:00).
"""

import typing as t

from codeforlife.request import BaseRequest
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.parsers import (
    FileUploadParser,
    FormParser,
    JSONParser,
    MultiPartParser,
)
from rest_framework.test import APIRequestFactory as _APIRequestFactory

from ..models import Contributor
from ..models.session import SessionStore


class APIRequestFactory(_APIRequestFactory):
    """Custom API request factory that returns DRF's Request object."""

    def request(self, user: t.Optional[Contributor] = None, **kwargs):
        wsgi_request = t.cast(WSGIRequest, super().request(**kwargs))

        request = BaseRequest[SessionStore, Contributor](
            wsgi_request,
            parsers=[
                JSONParser(),
                FormParser(),
                MultiPartParser(),
                FileUploadParser(),
            ],
        )

        if user:
            # pylint: disable-next=attribute-defined-outside-init
            request.user = user

        return request

    # pylint: disable-next=too-many-arguments
    def generic(
        self,
        method: str,
        path: t.Optional[str] = None,
        data: t.Optional[str] = None,
        content_type: t.Optional[str] = None,
        secure: bool = True,
        user: t.Optional[Contributor] = None,
        **extra
    ):
        return t.cast(
            BaseRequest[SessionStore, Contributor],
            super().generic(
                method,
                path or "/",
                data or "",
                content_type or "application/json",
                secure,
                user=user,
                **extra,
            ),
        )

    def get(  # type: ignore[override]
        self,
        path: t.Optional[str] = None,
        data: t.Any = None,
        user: t.Optional[Contributor] = None,
        **extra
    ):
        return t.cast(
            BaseRequest[SessionStore, Contributor],
            super().get(
                path or "/",
                data,
                user=user,
                **extra,
            ),
        )

    # pylint: disable-next=too-many-arguments
    def post(  # type: ignore[override]
        self,
        path: t.Optional[str] = None,
        data: t.Any = None,
        # pylint: disable-next=redefined-builtin
        format: t.Optional[str] = None,
        content_type: t.Optional[str] = None,
        user: t.Optional[Contributor] = None,
        **extra
    ):
        if format is None and content_type is None:
            format = "json"

        return t.cast(
            BaseRequest[SessionStore, Contributor],
            super().post(
                path or "/",
                data,
                format,
                content_type,
                user=user,
                **extra,
            ),
        )

    # pylint: disable-next=too-many-arguments
    def put(  # type: ignore[override]
        self,
        path: t.Optional[str] = None,
        data: t.Any = None,
        # pylint: disable-next=redefined-builtin
        format: t.Optional[str] = None,
        content_type: t.Optional[str] = None,
        user: t.Optional[Contributor] = None,
        **extra
    ):
        if format is None and content_type is None:
            format = "json"

        return t.cast(
            BaseRequest[SessionStore, Contributor],
            super().put(
                path or "/",
                data,
                format,
                content_type,
                user=user,
                **extra,
            ),
        )

    # pylint: disable-next=too-many-arguments
    def patch(  # type: ignore[override]
        self,
        path: t.Optional[str] = None,
        data: t.Any = None,
        # pylint: disable-next=redefined-builtin
        format: t.Optional[str] = None,
        content_type: t.Optional[str] = None,
        user: t.Optional[Contributor] = None,
        **extra
    ):
        if format is None and content_type is None:
            format = "json"

        return t.cast(
            BaseRequest[SessionStore, Contributor],
            super().patch(
                path or "/",
                data,
                format,
                content_type,
                user=user,
                **extra,
            ),
        )

    # pylint: disable-next=too-many-arguments
    def delete(  # type: ignore[override]
        self,
        path: t.Optional[str] = None,
        data: t.Any = None,
        # pylint: disable-next=redefined-builtin
        format: t.Optional[str] = None,
        content_type: t.Optional[str] = None,
        user: t.Optional[Contributor] = None,
        **extra
    ):
        if format is None and content_type is None:
            format = "json"

        return t.cast(
            BaseRequest[SessionStore, Contributor],
            super().delete(
                path or "/",
                data,
                format,
                content_type,
                user=user,
                **extra,
            ),
        )

    # pylint: disable-next=too-many-arguments
    def options(  # type: ignore[override]
        self,
        path: t.Optional[str] = None,
        data: t.Optional[t.Union[t.Dict[str, str], str]] = None,
        # pylint: disable-next=redefined-builtin
        format: t.Optional[str] = None,
        content_type: t.Optional[str] = None,
        user: t.Optional[Contributor] = None,
        **extra
    ):
        if format is None and content_type is None:
            format = "json"

        return t.cast(
            BaseRequest[SessionStore, Contributor],
            super().options(
                path or "/",
                data or {},
                format,
                content_type,
                user=user,
                **extra,
            ),
        )
