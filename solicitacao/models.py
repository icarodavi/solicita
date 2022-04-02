from django.db import models
from django.contrib.auth.models import User
from secretaria.models import Secretaria
from django.utils.translation import gettext as _


class Solicitacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    objeto = models.TextField('Objeto', blank=True,  null=True)
    secretaria = models.ForeignKey(Secretaria, on_delete=models.DO_NOTHING)
    # qtd_total = models.PositiveIntegerField(
    #     'Quantidade Total', blank=True, null=True)
    data = models.DateField('Data')
    status = models.CharField(default='P', max_length=1, choices=(
        ('A', 'Aprovado'), ('C', 'Criado'), ('R', 'Reprovado'),
        ('P', 'Pendente'), ('E', 'Enviado'), ('F', 'Finalizado'),))

    def __str__(self):
        return f'Solicitação nº {self.pk}'

    class Meta:
        verbose_name = 'Solicitação'
        verbose_name_plural = 'Solicitações'


class SolicitacaoItem(models.Model):
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE)
    produto = models.CharField(_('Produto'), max_length=255)
    produto_id = models.PositiveIntegerField(_('Produto_ID'), )
    # variacao = models.CharField(_('Variação'), max_length=255)
    # variacao_id = models.PositiveIntegerField(_('Variação_ID'), )
    quantidade = models.PositiveIntegerField(
        _('Quantidade'), blank=True, null=True)
    imagem = models.CharField(
        _("Imagem"), max_length=2000, blank=True, null=True)

    def __str__(self):
        return f'Item da Solicitação nº {self.solicitacao.id}'

    class Meta:
        verbose_name = 'Item da Solicitação'
        verbose_name_plural = 'Itens da Solicitação'
