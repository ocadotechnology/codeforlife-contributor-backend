"""
© Ocado Group
Created on 06/08/2024 at 14:07:24(+01:00).
"""

from codeforlife.models import AbstractBaseSession, BaseSessionStore

from .contributor import Contributor


class Session(AbstractBaseSession):
    """
    A custom session model to support querying a contributor's session.
    https://docs.djangoproject.com/en/3.2/topics/http/sessions/#example
    """

    user = AbstractBaseSession.init_user_field(Contributor)

    @classmethod
    def get_session_store_class(cls):
        return SessionStore


class SessionStore(BaseSessionStore[Session, Contributor]):
    """
    A custom session store interface to support:
    1. creating only one session per contributor;
    2. clearing a contributor's expired sessions.
    https://docs.djangoproject.com/en/3.2/topics/http/sessions/#example
    """
