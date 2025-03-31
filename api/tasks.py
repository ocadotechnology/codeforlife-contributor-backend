"""
© Ocado Group
Created on 27/03/2025 at 17:11:50(+00:00).
"""

from codeforlife.tasks import shared_task
from django.core.management import call_command


@shared_task
def clear_sessions():
    """Clear expired django-sessions.

    https://docs.djangoproject.com/en/4.2/topics/http/sessions/#clearing-the-session-store
    """

    call_command("clearsessions")
