"""
© Ocado Group
Created on 10/09/2024 at 17:01:39(+03:00).
"""

from codeforlife.models.signals import UpdateFields, model_receiver, pre_save
from django.db.models import signals

from ..models import ContributorEmail

contributor_email_receiver = model_receiver(ContributorEmail)

# pylint: disable=unused-argument


@contributor_email_receiver(signals.pre_save)
def contributor_email__pre_save(
    sender,
    instance: ContributorEmail,
    update_fields: UpdateFields,
    **kwargs,
):
    """Clean before saving."""
    if (
        pre_save.adding(instance)
        or update_fields is None
        or "email" in update_fields
    ):
        instance.email = instance.email.lower()
