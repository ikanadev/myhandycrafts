"""Profile User Model."""

from django.core.validators import RegexValidator
# Django
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile

# ultilities
from myhandycrafts.utils.models import MyHandycraftsModel

#import
import time
from PIL import Image
from io import BytesIO

import sys



class Profile(MyHandycraftsModel):
    """ Profile Model.

    A profile hold a user'ps public data like biography,
    picture, and statics.
    """

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )
    biography = models.TextField(max_length=500, blank=True)

    ci = models.CharField(max_length=30, blank=True)

    birth_date = models.DateField()

    address = models.TextField(max_length=256, blank=True)

    # Category
    category = models.ForeignKey(
        'categories.Category',
        null=True,
        on_delete=models.SET_NULL,
        related_name='rubro'
    )

    # Company information
    nit = models.CharField(max_length=30, blank=True)
    nit_bussiness_name = models.CharField(max_length=512, blank=True)
    nit_is_active = models.BooleanField(default=False)

    # Contact Information User
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{6,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    website = models.CharField(max_length=128, blank=True)
    has_wattsapp = models.BooleanField(default=False)
    has_facebook = models.BooleanField(default=False)
    addres_facebook = models.TextField(max_length=512, blank=True)

    # stats
    reputation = models.FloatField(
        default=5.0,
        help_text="User's reputation based on crafts."
    )
    publications = models.PositiveIntegerField(default=0)
    requests = models.PositiveIntegerField(default=0)
    stores = models.PositiveIntegerField(default=0)
    participation_in_fairs = models.PositiveIntegerField(default=0)

    def __str__(self):
        """Return user's str representations"""
        return str(self.user)

    def save(self, *args, **kwargs):
        if str(self.picture) is not '':
                self.picture = self.compressImage(self.picture,1080,1080,50)
        super(Profile, self).save(*args, **kwargs)

    def compressImage(self, uploadedImage,width,height,quality):
        image = Image.open(uploadedImage)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        outputIoStream = BytesIO()
        image.thumbnail((width, height))
        time_stamp = int(round(time.time() * 1000))  # TIME
        image_name = "%s_%s%s" % ( time_stamp, str(round(image.size[0])) + "x" + str(round(image.size[1])), ".jpg")  # filename image
        image.save(outputIoStream, format='JPEG', quality=quality)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'FileField',image_name, 'image/jpeg',
                                             sys.getsizeof(outputIoStream), None)
        return uploadedImage
