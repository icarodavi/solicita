from django.db import models
from perfil.models import Perfil
from django.utils.translation import gettext as _


class Solicitacao(models.Model):
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    qtd_total = models.PositiveIntegerField()
    status = models.CharField(default='P', max_length=1, choices=(
        ('A', 'Aprovado'), ('C', 'Criado'), ('R', 'Reprovado'),
        ('P', 'Pendente'), ('E', 'Enviado'), ('F', 'Finalizado'),))

    def __str__(self):
        return f'Solicitação nº {self.pk}'

    class Meta:
        verbose_name = 'Solicitação'
        verbose_name_plural = 'Solicitações'


class SolicitacaoItem(models.Model):

    produto = models.CharField(_('Produto'), max_length=255)
    produto_id = models.PositiveIntegerField(_('Produto_ID'), )
    variacao = models.CharField(_('Variação'), max_length=255)
    variacao_id = models.PositiveIntegerField(_('Variação_ID'), )
    quantidade = models.PositiveIntegerField(_('Quantidade'))
    imagem = models.CharField(
        _("Imagem"), max_length=2000, blank=True, null=True)

    def __str__(self):
        return f'Item do Pedido nº {self.pedido.id}'

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
