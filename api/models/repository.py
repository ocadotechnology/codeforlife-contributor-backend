"""
© Ocado Group
Created on 05/07/2024 at 16:39:14(+01:00).

"""
from django.db import models
from .contributor import Contributor

class Repository(models.Model):
    """ A repository to contribute to"""
    id = models.IntegerField(primary_key=True)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    name_choices = [
        ("portal", "portal"),
        ("rr", "rr")
    ]
    name = models.TextField(choices=name_choices)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["contributor", "name"], name='unique_contributor_repo')
        ]