"""
© Ocado Group
Created on 12/04/2024 at 16:51:36(+01:00).
"""

import logging
import traceback

from codeforlife.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


@method_decorator(ensure_csrf_cookie, name="dispatch")
@method_decorator(csrf_exempt, name="dispatch")
class CsrfCookieView(APIView):
    """A view to get a CSRF cookie."""

    http_method_names = ["get"]
    permission_classes = [AllowAny]

    def get(self, request: Request):
        """
        Return a response which Django will auto-insert a CSRF cookie into.
        """
        return Response()

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)

        def view_wrapper(request, *args, **kwargs):
            try:
                return view(request, *args, **kwargs)
            # pylint: disable-next=broad-exception-caught
            except Exception as ex:
                logging.exception(ex)
                print(ex)
                traceback.print_exc()
                print(traceback.format_exc())
                logging.error(traceback.format_exc())
                raise ex

        return view_wrapper
