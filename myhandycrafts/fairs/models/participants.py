"""Fair model."""

# Django
from django.db import models

# Utils
from myhandycrafts.utils.models import MyHandycraftsModel
from myhandycrafts.utils.image_helper import ImageHelper

# models
from myhandycrafts.users.models import User


STATUS_PARTICIPANT_CHOICES = [
    ("AA", "Accepted"), # aceptado
    ("PP", "Pending"),  # pendiente
    ("RR", "Denied"),   # Rechazado
    ("DD", "Declined")  # Declinado
]

class Participant(MyHandycraftsModel):
    user = models.ForeignKey('users.User',
                             on_delete=models.CASCADE,
                             related_name='user'
                             )
    admin = models.ForeignKey('users.User',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='admin')

    fair = models.ForeignKey('fairs.Fair',on_delete=models.CASCADE)
    user_description = models.TextField(blank=True,max_length=2048)
    admin_description = models.TextField(blank=True,max_length=2048)
    state = models.CharField(max_length=2,
                             choices=STATUS_PARTICIPANT_CHOICES,
                             verbose_name='status_participant_choices',
                             default='PP')

    def __str__(self):
        """Return name of user and fair"""
        return "{} at fair: {}".format(
            str(self.user),
            str(self.fair),
        )













