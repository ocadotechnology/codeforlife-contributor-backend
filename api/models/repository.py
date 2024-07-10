"""
© Ocado Group
Created on 05/07/2024 at 16:39:14(+01:00).
"""

from django.db import models

from .contributor import Contributor


class Repository(models.Model):
    """A repository to contribute to"""

    id = models.IntegerField(primary_key=True)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    NAME_CHOICES = [("portal", "portal"), ("rr", "rr")]
    name = models.TextField(choices=NAME_CHOICES)
    points = models.IntegerField(default=0)

    class Meta:
        unique_together = ["contributor", "name"]
        verbose_name = "repository"
        verbose_name_plural = "repositories"

    def __str__(self):
        return self.name
