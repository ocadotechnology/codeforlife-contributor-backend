"""
© Ocado Group
Created on 05/07/2024 at 16:18:48(+01:00).
"""

from django.db import models


class Contributor(models.Model):
    """A contributor that contributes to a repo"""

    id = models.IntegerField(primary_key=True)
    email = models.TextField()
    name = models.TextField()
    location = models.TextField()
    html_url = models.TextField()
    avatar_url = models.TextField()

    class Meta:
        verbose_name = "contributor"
        verbose_name_plural = "contributors"

    def __str__(self):
        return self.name
