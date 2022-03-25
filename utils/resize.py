import os
from PIL import Image
from django.conf import settings


def resize_image(image_name, new_width=800):
    image_path = os.path.join(settings.MEDIA_ROOT, str(image_name))
    # print(image_name._file.image.__dict__)
    image = Image.open(image_path)
    width, height = image.size
    new_height = round((new_width * height) / width)
    if width <= new_width:
        image.save(
            image_path,
            optimize=True,
            quality=50
        )
        image.close()
        return image

    new_image = image.resize((new_width, new_height), Image.LANCZOS)
    new_image.save(
        image_path,
        optimize=True,
        quality=50
    )
    return new_image
