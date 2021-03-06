from pprint import pprint
import json


def formata_preco(val):
    return f'R$ {val:0,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.')


def cart_total_qtd(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])


def cart_total(carrinho):
    return sum([
        item.get('preco_quantitativo_promocional')
        if item.get('preco_quantitativo_promocional')
        else item.get('preco_quantitativo') for item in carrinho.values()
    ])


def json_web(item):
    pprint(dir(item))
    # pprint(vars(item))
    return json.dumps(item)
