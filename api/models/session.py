"""
© Ocado Group
Created on 06/08/2024 at 14:07:24(+01:00).
"""

import typing as t

from django.contrib.auth import SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.contrib.sessions.base_session import AbstractBaseSession
from django.db import models
from django.utils import timezone

from .contributor import Contributor


class Session(AbstractBaseSession):
    """
    A custom session model to support querying a contributor's session.
    https://docs.djangoproject.com/en/3.2/topics/http/sessions/#example
    """

    contributor = models.OneToOneField(
        Contributor,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    @property
    def is_expired(self):
        """Whether or not this session has expired."""
        return self.expire_date < timezone.now()

    @property
    def store(self):
        """A store instance for this session."""
        return self.get_session_store_class()(self.session_key)

    @classmethod
    def get_session_store_class(cls):
        return SessionStore


class SessionStore(DBStore):
    """
    A custom session store interface to support:
    1. creating only one session per contributor;
    2. clearing a contributor's expired sessions.
    https://docs.djangoproject.com/en/3.2/topics/http/sessions/#example
    """

    @classmethod
    def get_model_class(cls):
        return Session

    def create_model_instance(self, data):
        try:
            contributor_id = int(data.get(SESSION_KEY))
        except (ValueError, TypeError):
            # Create an anon session.
            return super().create_model_instance(data)

        model_class = self.get_model_class()

        try:
            session = model_class.objects.get(contributor_id=contributor_id)
        except model_class.DoesNotExist:
            # Associate session to contributor.
            session = model_class.objects.get(session_key=self.session_key)
            session.contributor = Contributor.objects.get(id=contributor_id)

        session.session_data = self.encode(data)

        return session

    @classmethod
    def clear_expired(cls, contributor_id: t.Optional[int] = None):
        session_query = cls.get_model_class().objects.filter(
            expire_date__lt=timezone.now()
        )
        if contributor_id:
            session_query = session_query.filter(contributor_id=contributor_id)
        session_query.delete()
