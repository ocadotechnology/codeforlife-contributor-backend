"""
© Ocado Group
Created on 16/06/2025 at 13:21:01(+01:00).
"""

from codeforlife.request import BaseRequest

from .models import Contributor
from .models.session import SessionStore


class Request(BaseRequest[SessionStore, Contributor]):
    """Request instance."""
