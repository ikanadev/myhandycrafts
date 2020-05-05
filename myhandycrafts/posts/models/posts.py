"""Post model."""

# Django
from django.db import models

# Utils
from myhandycrafts.utils.models import MyHandycraftsModel


STATUS_POST_CHOICES = [
    ("AV", "Available"), # disponible
    ("SO", "Sold"),     # vendido
]

class Post(MyHandycraftsModel):
    user = models.ForeignKey('users.User',
                             on_delete=models.CASCADE,
                             verbose_name='users'
                             )
    category = models.ForeignKey('categories.Category',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 default=None,
                                 verbose_name='categories'
                                 )

    title = models.CharField(max_length=256)
    description = models.TextField()
    price = models.FloatField()
    cuantitie = models.PositiveIntegerField(null=True,default=None)
    state = models.CharField(max_length=2,
                             choices=STATUS_POST_CHOICES,
                             verbose_name='status_post_choices',
                             default='AV')

    def __str__(self):
        """Return title"""
        return self.title













