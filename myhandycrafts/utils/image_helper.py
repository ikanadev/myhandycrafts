""" Image Helper."""

# PIL
from PIL import Image

# IO
from io import BytesIO

# Django
from django.core.files.uploadedfile import InMemoryUploadedFile


#import
import sys
import time

class ImageHelper:

    def compressImage(self,uploadedImage, width, height, quality ):
        image = Image.open(uploadedImage)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        outputIoStream = BytesIO()
        image.thumbnail((width, height))
        time_stamp = int(round(time.time() * 1000))  # TIME
        image_name = "%s_%s%s" % (
        time_stamp, str(round(image.size[0])) + "x" + str(round(image.size[1])), ".jpg")  # filename image
        image.save(outputIoStream, format='JPEG', quality=quality)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'FileField', image_name, 'image/jpeg',
                                             sys.getsizeof(outputIoStream), None)
        return uploadedImage