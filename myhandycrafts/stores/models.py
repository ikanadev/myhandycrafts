"""Store model."""

# Django
from django.db import models

# Utils
from myhandycrafts.utils.models import MyHandycraftsModel
from myhandycrafts.utils.image_helper import ImageHelper

# models
from myhandycrafts.users.models import User


class Store(MyHandycraftsModel):
    """Store model.

    A store model represent a store of a craftman, user can publish his
    products, that he want to sell.
    On store user can create relationship between produt's publish and store
    """
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        help_text='User is property of store',
        related_name='user'
    )

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True,max_length=1024)
    ubicacion = models.TextField(max_length=512)
    gps = models.CharField(max_length=10)

    # stats
    reputation = models.FloatField(
        default=5.0,
        help_text="Store's reputation based on crafts."
    )
    publications = models.PositiveIntegerField(default=0)
    visits = models.PositiveIntegerField(default=0)

    class Meta:
        """Class Meta"""
        verbose_name = "Store"
        verbose_name_plural = "Stores"

    def __str__(self):
        return  self.name





class StoreMedia(MyHandycraftsModel):
    """Store Media model.

    Store Media model save store's images
    """
    store = models.ForeignKey("stores.Store",
                            on_delete = models.CASCADE,
                            help_text = "store's media",
                            related_name = 'media'
                              )

    img_huge = models.ImageField("Image huge",max_length=255,default="",upload_to="img/store/huge/")
    img_standar = models.ImageField("Image standar",max_length=255,default="",upload_to="img/store/standar/")
    img_small = models.ImageField("Image small",max_length=255,default="",upload_to="img/store/small/")
    order = models.PositiveIntegerField(default=1)


    class Meta:
        """Class Meta."""
        verbose_name = "store media"
        verbose_name_plural = "store media"

    def __str__(self):
        return "media %s" % str(self.store)

    def save(self, *args, **kwargs):
        """ save image on three size."""
        if self.pk is None:
            self.img_huge = ImageHelper.compressImage(self.img_huge, 1280, 1280, 65)
            self.img_standar = ImageHelper.compressImage(self.img_huge, 1080, 1080, 50)
            self.img_small = ImageHelper.compressImage(self.img_huge, 650, 650, 50)
        super(StoreMedia, self).save(*args, **kwargs)




