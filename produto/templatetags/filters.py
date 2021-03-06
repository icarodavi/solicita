from utils import utils
from utils.s3urls import create_presigned_url
from django.template import Library
from decouple import config
register = Library()


@register.filter
def formata_preco(val):
    return utils.formata_preco(val)


@register.filter
def cart_total_qtd(carrinho):
    return utils.cart_total_qtd(carrinho)


@register.filter
def cart_total(carrinho):
    return utils.cart_total(carrinho)


@register.filter
def s3url_static(val):
    return create_presigned_url(config('AWS_STORAGE_BUCKET_NAME'), 'static/'+val)


@register.filter
def s3url_media(val):
    url = create_presigned_url(
        config('AWS_STORAGE_BUCKET_NAME'), 'media/public/'+val)
    return url


@register.filter
def json_web(val):
    return utils.json_web(val)
