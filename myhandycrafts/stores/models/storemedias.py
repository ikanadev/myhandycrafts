"""Store model."""

# Django
from django.db import models

# Utils
from myhandycrafts.utils.models import MyHandycraftsModel
from myhandycrafts.utils.image_helper import ImageHelper



class StoreMedia(MyHandycraftsModel):
    """Store Media model.

    Store Media model save store's images
    """
    store = models.ForeignKey("stores.Store",
                            on_delete = models.CASCADE,
                            help_text = "store's media",
                            related_name = 'storemedias'
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
            image_save = ImageHelper()
            self.img_huge = image_save.compressImage(self.img_huge, 1280, 1280, 65)
            self.img_standar = image_save.compressImage(self.img_huge, 1080, 1080, 50)
            self.img_small = image_save.compressImage(self.img_huge, 650, 650, 50)
        super(StoreMedia, self).save(*args, **kwargs)




