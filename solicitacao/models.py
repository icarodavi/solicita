from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _
from produto.models import Produto
from secretaria.models import Secretaria


class Solicitacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    objeto = models.TextField('Objeto', blank=True,  null=True)
    secretaria = models.ForeignKey(Secretaria, on_delete=models.DO_NOTHING)
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
    soliticao_item = models.ManyToManyField(
        Solicitacao, related_name='solicitacao', through='SolicitacaoQuantidade')
    produto = models.CharField(_('Produto'), max_length=255)
    produto_id = models.PositiveIntegerField(_('Produto_ID'), )
    qtd = models.PositiveIntegerField(
        _('Quantidade'), blank=True, null=True)
    imagem = models.CharField(
        _("Imagem"), max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.produto

    def get_nome(self):
        return f'{self.produto}'

    def get_unidade(self):
        unidade = Produto.objects.get(pk=self.produto_id).values('unidade')
        return f'{unidade}'

    class Meta:
        verbose_name = 'Item da Solicitação'
        verbose_name_plural = 'Itens da Solicitação'


class SolicitacaoQuantidade(models.Model):
    solicitacao = models.ForeignKey(
        Solicitacao, on_delete=models.CASCADE, related_name='quantidade')
    item_solicitacao = models.ForeignKey(
        SolicitacaoItem, on_delete=models.CASCADE, related_name='quantidade')
    # quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.solicitacaoitem.produto} - Qtd: {self.quantidade}'

    class Meta:
        verbose_name = 'Through Quantidade'
        verbose_name_plural = 'Through Quantidades'
