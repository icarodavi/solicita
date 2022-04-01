import os
import tempfile
from io import BytesIO
from pathlib import Path
from pprint import pprint

from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import (InMemoryUploadedFile,
                                            TemporaryUploadedFile)
from PIL import Image
from solicita.storage_backends import PublicMediaStorage


def resize_image(image_name, new_width=800):
    # tmpdir = tempfile.mkdtemp()
    img = Image.open(image_name)
    width, height = img.size
    new_height = round((new_width * height) / width)
    size = (new_width, new_height)
    img_filename = Path(image_name.name)
    # tmpfile = tmpdir + img_filename
    # print(tmpfile)
    # pprint(dir(img))
    # pprint(vars(img))
    # pprint(img.frombytes())

    # if width >= new_width:
    img.thumbnail(size)
    buffer = BytesIO()
    # file_object = File(buffer)
    # image_path = os.path.join(tempfile.mkdtemp(), str(image_name))
    img.save(buffer, format=img.format)
    # media = PublicMediaStorage()
    # media.save(name=image_name.file.name, content=buffer)
    # pprint(dir(img))
    # pprint(vars(img))
    # pprint(dir(img.getdata()))
    # pprint(vars(img.getdata()))
    # with open(image_path, "wb") as file:
    #     file.write(img.tobytes())

    # with open(image_path, "w") as f:
    #     pprint(dir(file_object))
    #     print(image_path)
    #     f.write(file_object.read())
    # image_name.save(img_filename, file_object)
    # pprint(dir(image_path))
    # pprint(vars(image_path))
    # print('--------------------------------------')
    # pprint(dir(buffer))
    # pprint(vars(buffer))
    # image_name._file.file = buffer
    # print(image_name.file.file == buffer)
    # pprint(dir(image_name))
    # pprint(vars(image_name))
    # image_name.commited = True
    # image_name.save(name=img_filename, content=image_name)
    imx = Image.open(buffer)
    imx.resize(size)
    imx.save(img_filename, format=imx.format)
    imx.close()
    img.close()
    return imx
    # else:
    #     return False
    #     # with Image.open(image_name) as im:
    #     im.save(image_path)
    # img = Image.open(image_path)
    # new_height = round((new_width * height) / width)
    # if width <= new_width:
    #     img.close()
    #     return img.filename
    # new_image = img.resize((new_width, new_height), Image.LANCZOS)
    # new_image.save(
    #     image_path,
    #     format=img.format,
    #     optimize=True,
    #     quality=50
    # )
    # img.close()
    # up_file(image_path)
    # return image_path


def resize_uploaded_image(image, max_width, *args, **kwargs):
    # size = (max_width, max_height)
    img = Image.open(image)
    # imx = Imx(image, *args, **kwargs)
    # pprint(dir(image))
    # pprint(vars(image))

    img_format = img.format
    width, height = img.size
    max_height = round((max_width * height) / width)
    size = (max_width, max_height)
    # img.close()

    # pprint(dir(image))
    pprint(vars(image._file.file))
    # return None

    # Uploaded file is in memory
    # if isinstance(image, InMemoryUploadedFile):

    ##############################################
    # memory_image = BytesIO(image.read())
    pil_image = Image.open(image)
    # img_format = os.path.splitext(image.name)[1][1:].upper()
    # img_format = 'JPEG' if img_format == 'JPG' else img_format

    if pil_image.width > max_width or pil_image.height > max_height:
        pil_image.thumbnail(size)

    new_image = BytesIO()
    pil_image.save(new_image, format=img_format)

    new_image = ContentFile(new_image.getvalue())
    x = InMemoryUploadedFile(new_image, None, image.name,
                             image.content_type, None, None)
    image._file = x
    return image
    # Uploaded file is in disk
    # elif isinstance(image, TemporaryUploadedFile):
    #     path = image.temporary_file_path()
    #     pil_image = Image.open(path)

    #     if pil_image.width > max_width or pil_image.height > max_height:
    #         pil_image.thumbnail(size)
    #         pil_image.save(path)
    #         image.size = os.stat(path).st_size

    return image


class StringReprMixin:
    def __str__(self) -> str:
        params = ', '.join(
            [f'{k}={v}' for k, v in self.__dict__.items()]
        )
        return f'{self.__class__.__name__}({params})'

    def __repr__(self) -> str:
        return self.__str__()


# class Imx(StringReprMixin, Image.Image):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)


def imx(image, max_width, max_height):
    size = (max_width, max_height)

    # Uploaded file is in memory
    if isinstance(image, InMemoryUploadedFile):
        memory_image = BytesIO(image.read())
        pil_image = PilImage.open(memory_image)
        img_format = os.path.splitext(image.name)[1][1:].upper()
        img_format = 'JPEG' if img_format == 'JPG' else img_format

        if pil_image.width > max_width or pil_image.height > max_height:
            pil_image.thumbnail(size)

        new_image = BytesIO()
        pil_image.save(new_image, format=img_format)

        new_image = ContentFile(new_image.getvalue())
        return InMemoryUploadedFile(new_image, None, image.name, image.content_type, None, None)

    # Uploaded file is in disk
    elif isinstance(image, TemporaryUploadedFile):
        path = image.temporary_file_path()
        pil_image = PilImage.open(path)

        if pil_image.width > max_width or pil_image.height > max_height:
            pil_image.thumbnail(size)
            pil_image.save(path)
            image.size = os.stat(path).st_size

    return image
