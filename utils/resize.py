import os
import tempfile
from pprint import pprint
from typing import Any
from utils.s3save import up_file

from PIL import Image

# from solicita.storage_backends import PublicMediaStorage


def resize_image(image_name, new_width=800) -> Any:
    image_path = os.path.join(tempfile.mkdtemp(), str(image_name))
    with Image.open(image_name) as im:
        im.save(image_path)
    img = Image.open(image_path)
    width, height = img.size
    new_height = round((new_width * height) / width)
    if width <= new_width:
        img.close()
        return img.filename
    new_image = img.resize((new_width, new_height), Image.LANCZOS)
    new_image.save(
        image_path,
        format=img.format,
        optimize=True,
        quality=50
    )
    img.close()
    up_file(image_path)
    return image_path
