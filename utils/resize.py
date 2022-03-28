import os
from io import BytesIO
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage


def resize_image(image_name, new_width=800):
    # image_path = os.path.join(settings.MEDIA_ROOT, str(image_name))
    image_read = storage.open(image_name, "r")
    # print(image_name._file.image.__dict__)
    image = Image.open(image_read)
    width, height = image.size
    new_height = round((new_width * height) / width)
    if width <= new_width:
        img_buffer = BytesIO()

        image.save(
            img_buffer,
            format=image.format,
            optimize=True,
            quality=50
        )
        image.close()
        return image
    img_buffer = BytesIO()
    new_image = image.resize((new_width, new_height), Image.LANCZOS)
    new_image.save(
        img_buffer,
        format=image.format,
        optimize=True,
        quality=50
    )
    print(ContentFile(img_buffer.getvalue()))
    image.close()
    return new_image
