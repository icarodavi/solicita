from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
import re
from utils.validacpf import valida_cpf


class Perfil(models.Model):
    usuario = models.OneToOneField(
        User, verbose_name=_("Usuário"), on_delete=models.CASCADE)
    data_nascimento = models.DateField(
        _("Data de Nascimento"), auto_now=False, auto_now_add=False)
    cpf = models.CharField(_("CPF"), max_length=15)
    endereco = models.CharField(_("Endereço"), max_length=255)
    numero = models.CharField(_("Número"), max_length=5)
    complemento = models.CharField(_("Complemento"), max_length=30)
    bairro = models.CharField(_("Bairro"), max_length=30)
    cep = models.CharField(_("CEP"), max_length=10)
    cidade = models.CharField(_("Cidade"), max_length=30)
    estado = models.CharField(_("Estado"), max_length=2, choices=(
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'),
        ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),))
    ativo = models.BooleanField()

    def __str__(self):
        nome = f'{self.usuario.first_name} {self.usuario.last_name}' if self.usuario.first_name != '' else f'{self.usuario}'
        return nome

    def clean(self):
        error_messages = {}

        cpf_enviado = self.cpf or None
        cpf_salvo = None
        perfil = Perfil.objects.filter(cpf=cpf_enviado).first()

        if perfil:
            cpf_salvo = perfil.cpf

            if cpf_salvo is not None and self.pk != perfil.pk:
                error_messages['cpf_unico'] = 'CPF já cadastrado'

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cep'] = 'Cep Inválido, digite os 8 dígitos do CEP.'

        if error_messages:
            raise ValidationError(error_messages)

        return super().clean()

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
