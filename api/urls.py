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
from codeforlife.views import HealthCheckView as _HealthCheckView
from codeforlife.views.health_check import HealthCheck
from django.conf import settings


# pylint: disable-next=missing-class-docstring
class HealthCheckView(_HealthCheckView):
    def get_health_check(self, request):
        health_check = super().get_health_check(request)
        return HealthCheck(
            health_status=health_check.health_status,
            additional_info=health_check.additional_info,
            details=[
                HealthCheck.Detail(
                    name="settings_secrets_keys",
                    description=",".join(list(settings.secrets.keys())),
                    health="healthy",
                ),
                HealthCheck.Detail(
                    name="STATIC_ROOT",
                    description=str(settings.STATIC_ROOT),
                    health="healthy",
                ),
                HealthCheck.Detail(
                    name="STATIC_URL",
                    description=str(settings.STATIC_URL),
                    health="healthy",
                ),
                HealthCheck.Detail(
                    name="AWS_STORAGE_BUCKET_NAME",
                    description=str(settings.AWS_STORAGE_BUCKET_NAME),
                    health="healthy",
                ),
                HealthCheck.Detail(
                    name="AWS_S3_CUSTOM_DOMAIN",
                    description=str(settings.AWS_S3_CUSTOM_DOMAIN),
                    health="healthy",
                ),
                HealthCheck.Detail(
                    name="AWS_LOCATION",
                    description=str(settings.AWS_LOCATION),
                    health="healthy",
                ),
                HealthCheck.Detail(
                    name="AWS_DEFAULT_ACL",
                    description=str(settings.AWS_DEFAULT_ACL),
                    health="healthy",
                ),
                HealthCheck.Detail(
                    name="AWS_S3_ADDRESSING_STYLE",
                    description=str(settings.AWS_S3_ADDRESSING_STYLE),
                    health="healthy",
                ),
                HealthCheck.Detail(
                    name="AWS_S3_REGION_NAME",
                    description=str(settings.AWS_S3_REGION_NAME),
                    health="healthy",
                ),
                HealthCheck.Detail(
                    name="STATICFILES_DIRS",
                    description=str(settings.STATICFILES_DIRS),
                    health="healthy",
                ),
            ],
        )


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
