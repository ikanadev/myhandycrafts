"""UserTemporalPassword Model."""

#   Django
from django.db import models

# Utilities
from myhandycrafts.utils.models import MyHandycraftsModel


class UserTemporalPassword(MyHandycraftsModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name="Usuario")
    password = models.CharField(max_length=200, verbose_name="Temporal Password")
    canceled_date = models.DateTimeField(default=None, null=True)

    class Meta:
        verbose_name = "User Temporal Password"
        verbose_name_plural = "User Temporal Passwords"

    def __str__(self):
        return "%s %s" % (self.user, self.created_at)
