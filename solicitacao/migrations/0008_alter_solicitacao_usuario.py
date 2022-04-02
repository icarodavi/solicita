# Generated by Django 4.0.3 on 2022-04-02 18:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('solicitacao', '0007_remove_solicitacaoitem_variacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacao',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]