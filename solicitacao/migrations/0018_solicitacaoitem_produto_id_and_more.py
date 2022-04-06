# Generated by Django 4.0.3 on 2022-04-06 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacao', '0017_alter_solicitacaoitem_produto'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitacaoitem',
            name='produto_id',
            field=models.PositiveIntegerField(default=1, verbose_name='Produto_ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='solicitacaoitem',
            name='produto',
            field=models.CharField(max_length=255, verbose_name='Produto'),
        ),
    ]
