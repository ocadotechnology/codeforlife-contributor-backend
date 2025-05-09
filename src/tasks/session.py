"""
© Ocado Group
Created on 27/03/2025 at 17:11:50(+00:00).
"""

import logging

from codeforlife.tasks import shared_task
from django.core.management import call_command

from ..models import Session


@shared_task
def clear():
    """Clear expired django-sessions.

    https://docs.djangoproject.com/en/4.2/topics/http/sessions/#clearing-the-session-store
    """

    before_session_count = Session.objects.count()
    logging.info("Session count before clearance: %d", before_session_count)

    call_command("clearsessions")

    after_session_count = Session.objects.count()
    logging.info("Session count after clearance: %d", after_session_count)

    session_clearance_count = before_session_count - after_session_count
    logging.info("Session clearance count: %d", session_clearance_count)
