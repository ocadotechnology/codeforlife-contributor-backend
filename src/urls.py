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

from codeforlife.routers import default_router
from codeforlife.urls import get_urlpatterns

# pylint: disable-next=wildcard-import,unused-wildcard-import
from codeforlife.urls.handlers import *
from django.urls import path

from .views import (
    AgreementSignatureViewSet,
    ContributorEmailViewSet,
    ContributorViewSet,
    LoginView,
)

default_router.register(
    "agreement-signatures",
    AgreementSignatureViewSet,
    basename="agreement-signature",
)
default_router.register(
    "contributors/emails",
    ContributorEmailViewSet,
    basename="contributor-email",
)
default_router.register(
    "contributors",
    ContributorViewSet,
    basename="contributor",
)

urlpatterns = get_urlpatterns(
    [
        *default_router.urls,
        path(
            "session/login/",
            LoginView.as_view(),
            name="session-login",
        ),
    ],
    include_user_urls=False,
)
