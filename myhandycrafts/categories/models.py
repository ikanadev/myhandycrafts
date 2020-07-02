"""Categories Model."""

# Django
from django.db import models

# Utilities
from myhandycrafts.utils.models import MyHandycraftsModel
from myhandycrafts.utils.image_helper import ImageHelper

class Category(MyHandycraftsModel):
    """ Category model.

    This model represent the category of craft
    that make the craftsman.
    """

    name = models.CharField(
        'Rubro name',
        max_length=128,
        blank=False,
    )

    description = models.TextField(max_length=512, blank=True)
    image = models.ImageField(
        'image Category',

        upload_to='categories/images/',
        blank=True,
        null=True
    )

    #statitics

    count_post = models.PositiveIntegerField(default=0)
    count_craftman = models.PositiveIntegerField(default=0)


    def __str__(self):
        """ Return category name"""
        return self.name


    # def save(self, *args, **kwargs):
    #     """ save image on three size."""
    #     imagesave = ImageHelper()
    #     if str(self.image) is not '':
    #         self.image = imagesave.compressImage(self.image, 1080, 1080, 50)
    #     super(Category, self).save(*args, **kwargs)