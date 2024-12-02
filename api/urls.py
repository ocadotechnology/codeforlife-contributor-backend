"""
© Ocado Group
Created on 02/07/2024 at 12:16:48(+01:00).

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from codeforlife.urls import get_urlpatterns

# pylint: disable-next=wildcard-import,unused-wildcard-import
from codeforlife.urls.handlers import *
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AgreementSignatureViewSet, ContributorViewSet, LoginView

router = DefaultRouter()

router.register(
    "agreement-signatures",
    AgreementSignatureViewSet,
    basename="agreement-signature",
)

router.register(
    "contributors",
    ContributorViewSet,
    basename="contributor",
)

# TODO: delete this after finish testing
# pylint: disable=wrong-import-position, wrong-import-order,ungrouped-imports
import logging

from codeforlife.views import HealthCheckView as _HealthCheckView
from django.conf import settings


# pylint: disable-next=missing-class-docstring
class HealthCheckView(_HealthCheckView):
    def get_health_check(self, request):
        # pylint: disable-next=logging-fstring-interpolation
        logging.warning(
            f"STATIC_ROOT: {settings.STATIC_ROOT}."
            f" STATIC_URL: {settings.STATIC_URL}."
            f" AWS_STORAGE_BUCKET_NAME: {settings.AWS_STORAGE_BUCKET_NAME}."
        )
        return super().get_health_check(request)


urlpatterns = get_urlpatterns(
    [
        *router.urls,
        path(
            "session/login/",
            LoginView.as_view(),
            name="session-login",
        ),
    ],
    health_check_view=HealthCheckView,
    include_user_urls=False,
)
