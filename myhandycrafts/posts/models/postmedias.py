"""Post model."""

# Django
from django.db import models

# Utils
from myhandycrafts.utils.models import MyHandycraftsModel
from myhandycrafts.utils.image_helper import ImageHelper



class PostMedia(MyHandycraftsModel):
    """Post Media model.

    Post Media model save post's images
    """
    post = models.ForeignKey("posts.Post",
                            on_delete = models.CASCADE,
                            help_text = "post's media",
                            related_name = 'postmedias'
                            )

    img_huge = models.ImageField("Image huge",max_length=255,default="",upload_to="img/post/huge/")
    img_standar = models.ImageField("Image standar",max_length=255,default="",upload_to="img/post/standar/")
    img_small = models.ImageField("Image small",max_length=255,default="",upload_to="img/post/small/")
    img_thumbnail = models.ImageField("Image thumbnail",max_length=255,default="",upload_to="img/post/thumbnail/")
    order = models.PositiveIntegerField(default=1)


    class Meta:
        """Class Meta."""
        verbose_name = "post media"
        verbose_name_plural = "post media"

    def __str__(self):
        return "media %s" % str(self.post)

    def save(self, *args, **kwargs):
        """ save image on three size."""
        imagesave = ImageHelper()
        if self.pk is None:
            self.img_huge = imagesave.compressImage(self.img_huge, 1280, 1280, 65)
            self.img_standar = imagesave.compressImage(self.img_huge, 1080, 1080, 50)
            self.img_small = imagesave.compressImage(self.img_huge, 650, 650, 50)
            self.img_thumbnail = imagesave.compressImage(self.img_huge, 100, 100, 50)
        super(PostMedia, self).save(*args, **kwargs)


