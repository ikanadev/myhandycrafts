"""Fair model."""

# Django
from django.db import models

# Utils
from myhandycrafts.utils.models import MyHandycraftsModel
from myhandycrafts.utils.image_helper import ImageHelper



class FairMedia(MyHandycraftsModel):
    """Fair Media model.

    Fair Media model save fair's images
    """
    fair = models.ForeignKey("fairs.Fair",
                            on_delete = models.CASCADE,
                            help_text = "fair's media",
                            related_name = 'fairmedias'
                            )

    img_huge = models.ImageField("Image huge",max_length=255,default="",upload_to="img/fair/huge/")
    img_standar = models.ImageField("Image standar",max_length=255,default="",upload_to="img/fair/standar/")
    img_small = models.ImageField("Image small",max_length=255,default="",upload_to="img/fair/small/")
    order = models.PositiveIntegerField(default=1)


    class Meta:
        """Class Meta."""
        verbose_name = "fair media"
        verbose_name_plural = "fair media"

    def __str__(self):
        return "media %s" % str(self.fair)

    def save(self, *args, **kwargs):
        """ save image on three size."""
        imagesave = ImageHelper()
        if self.pk is None:
            self.img_huge = imagesave.compressImage(self.img_huge, 1280, 1280, 65)
            self.img_standar = imagesave.compressImage(self.img_huge, 1080, 1080, 50)
            self.img_small = imagesave.compressImage(self.img_huge, 650, 650, 50)
        super(FairMedia, self).save(*args, **kwargs)


